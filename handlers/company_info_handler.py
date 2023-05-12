from pyrogram import Client, emoji, filters

from bot_objects.user_data_objects import Company
from filters.company_info_filters import input_company_name_filter, cancel_company_input_filter, write_comp_name_filter, \
    confirm_comp_data_filter, reject_comp_by_name_filter, write_inn_filter, reject_comp_data_by_inn_filter, \
    write_ogrn_filter, write_telephone_filter, write_email_filter, write_address_filter, \
    write_top_management_post_filter, write_top_management_name_filter, write_telephone_again_filter, \
    write_email_again_filter
from keyboards.bot_keyboards import CANCEL_INPUT_COMPANY_DATA, START_FIRST_MEETING, confirm_or_reject_company_keyboard, \
    AFTER_ADD_COMPANY_DATA_KEYBOARD
from secondary_functions.dadata_helper import DadataHelper
from secondary_functions.req_to_bot_api import post_send_msg_to_open_line
from settings.config import USER_DATA_STORAGE, TEMPORARY_STORAGE


@Client.on_callback_query(confirm_comp_data_filter)
async def confirm_comp_data(client, callback_data):
    """Обработчик нажатия кнопки подтверждения данных компании"""

    # Записываем данные в класс, некоторые аттрибуты засаживаем напрямую, без сеттеров.
    company_data = TEMPORARY_STORAGE.get(callback_data.from_user.id)
    company_obj = USER_DATA_STORAGE[callback_data.from_user.id]['company']
    company_obj.comp_name = company_data.get("company_name")
    company_obj.address = company_data.get("company_address")
    company_obj.ogrn = company_data.get("company_ogrn")
    company_obj.inn = company_data.get("company_inn")
    company_obj.top_management_post = company_data.get("top_management_post")
    company_obj.top_management_name = company_data.get("top_management_name")
    # отправляем запрос на сервер,
    result = await company_obj.write_company_data()
    if result:
        await callback_data.edit_message_text(
            text=f'📱Введите контактный номер телефона.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        company_obj.state_name = 'input_telephone_again'
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback_data.from_user.id,
            username=callback_data.from_user.username,
            msg_text=f'Клиент подтвердил данные компании. Запрашиваем контактный телефон.',
            last_name=callback_data.from_user.last_name,
            name=callback_data.from_user.first_name
        )
    else:
        await callback_data.edit_message_text(
            text=f'🛠Не удалось сохранить данные о компании. Мы уже решаем эту проблему.\n'
                 f'Попробуйте повторить позже.',
            reply_markup=START_FIRST_MEETING
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback_data.from_user.id,
            username=callback_data.from_user.username,
            msg_text=f'Не удалось сохранить данные о компании! Клиенту было предложено повторить ввод позже.',
            last_name=callback_data.from_user.last_name,
            name=callback_data.from_user.first_name
        )
    # дальше нужно ещё запросить телефон и тд.
    # TODO: было бы лучше сперва спрашивать контактный телефон и мыло, а потом всё, что касается компании.
    #  Но я начал сперва по-другому и сейчас придётся переписать много кода, чтобы всё было красиво.
    #  Поэтому сейчас от этого хэндлера пойдёт, так сказать, линия дублирующих запросов телефона и мыла.
    #  На будущее надо это поправить.


"""ВСЁ, ЧТО НИЖЕ НАДО БУДЕТ УБРАТЬ"""


@Client.on_message(filters.private & write_telephone_again_filter)
async def write_telephone_again(client, message):
    """Хэндлер записи контактного телефона...ещё один."""

    user_obj = USER_DATA_STORAGE[message.from_user.id]['user']
    company_obj = USER_DATA_STORAGE[message.from_user.id]['company']
    write_result = await user_obj.set_telephone(telephone=message.text)
    if write_result:
        await message.reply_text(
            text=f'📧Введите контактный EMAIL.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        user_obj.state_name = 'input_email_again'
        # Не забываем сбросить состояние по объекту Company, чтобы не попадать в ненужные хэндлеры
        company_obj.state_name = None
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Сохранение номера телефона. Запрос контактного EMAIL',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
    else:
        await message.reply_text(
            text='❕<b>Пожалуйста, введите корректный номер телефона</b>\n\n'
                 f'📱Введённый Вами номер телефона <code>{message.text}</code> не соответствует формату.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Клиент ввёл телефон неверного формата. Запрос контактного телефона ещё раз.\n'
                     f'Вот, что ввёл клиент:\n\t{message.text}',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


@Client.on_message(filters.private & write_email_again_filter)
async def write_email_again(client, message):
    """Хэндлер для записи мыла...ещё один."""

    user_obj = USER_DATA_STORAGE[message.from_user.id]['user']
    write_result = await user_obj.set_email(email=message.text)

    if write_result:  # В случае успешной записи мыла
        user_obj.state_name = None
        # Отправляем данные пользователя для записи в БД
        result_user = await user_obj.write_user_in_db()
        if result_user:
            await message.reply_text(
                text=f'🏢<b>Спасибо, информация о компании записана.</b>\n\n'
                     f'🏦Готовы ли Вы внести реквизиты банка?',
                reply_markup=AFTER_ADD_COMPANY_DATA_KEYBOARD
            )
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=message.from_user.id,
                username=message.from_user.username,
                msg_text=f'Клиенту предложено приступить к заполнению реквизитов банка',
                last_name=message.from_user.last_name,
                name=message.from_user.first_name
            )
        else:
            await message.reply_text(
                text=f'🛠Не удалось записать данные, мы уже решаем эту проблему.\n'
                     f'Попробуйте повторить позже.',
                reply_markup=START_FIRST_MEETING
            )
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=message.from_user.id,
                username=message.from_user.username,
                msg_text=f'Не удалось записать данные о компании клиента! Ему предложено повторить ввод позже.',
                last_name=message.from_user.last_name,
                name=message.from_user.first_name
            )

    else:  # Если мыло не прошло валидацию
        await message.reply_text(
            text='❕<b>Пожалуйста, введите корректный EMAIL</b>\n\n'
                 f'📧Введённый Вами EMAIL <code>{message.text}</code> не соответствует формату.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Введён неверный EMAIL. Запрос ещё раз.\nВот, что ввёл клиент:\n\t{message.text}',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


"""ВСЁ, ЧТО ВЫШЕ НАДО БУДЕТ УБРАТЬ"""


@Client.on_callback_query(cancel_company_input_filter)
async def cancel_company_input(client, callback_query):
    """Хэндлер для отмены ввода данных компании."""

    await callback_query.edit_message_text(
        text=f'{emoji.CROSS_MARK}<b>Ввод данных отменён.</b>\n\n'
             f'{emoji.DOWN_ARROW}Чтобы начать сначала, нажмите на кнопку ниже.',
        reply_markup=START_FIRST_MEETING
    )
    # очищаем состояние
    company_obj = USER_DATA_STORAGE[callback_query.from_user.id]['company']
    company_obj.state_name = None
    user_obj = USER_DATA_STORAGE[callback_query.from_user.id]['user']
    user_obj.state_name = None
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Клиент отменил ввод данных компании',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_callback_query(input_company_name_filter)
async def input_company_name(client, callback_query):
    """Хэндлер после нажатия кнопки готовности ввести данные. Запрашиваем название компании."""

    await callback_query.edit_message_text(
        text=f'{emoji.OFFICE_BUILDING}Пожалуйста, введите название компании.',
        reply_markup=CANCEL_INPUT_COMPANY_DATA
    )
    # Создаём объект класса Company и сохраняем его в словарь. Здесь же установка состояния на ввод назв.компании.
    USER_DATA_STORAGE[callback_query.from_user.id]['company'] = Company(
        user_tlg_id=callback_query.from_user.id,
        state_name='input_company_name'
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Клиент приступил к заполнению данных о компании.\nЗапрос названия компании.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_message(filters.private & write_comp_name_filter)
async def write_company_name(client, message):
    """Записываем название компании, ищем через DaData другие данные."""

    company_obj = USER_DATA_STORAGE[message.from_user.id]['company']
    company_obj.comp_name = message.text
    # Проверить в Дадата наличие данных о компании
    company_data = DadataHelper.find_company_data_by_name(company_obj.comp_name)
    if company_data:
        # Сохраняем данные из ответа ДаДата для следующего хэндлера
        TEMPORARY_STORAGE[message.from_user.id] = company_data
        # Если что-то нашлось, то даём клиенту на подтверждение
        inline_keyboard = await confirm_or_reject_company_keyboard(reject_step='comp_name')
        await message.reply_text(
            text=f'{emoji.CARD_INDEX_DIVIDERS}<b>Пожалуйста, проверьте данные компании, которые мне удалось найти.</b>\n\n'
                 f'■ <b>Название компании</b>: {company_data.get("company_name")}\n'
                 f'■ <b>Должность управляющего</b>: {company_data.get("top_management_post")}\n'
                 f'■ <b>Ф.И.О. управляющего</b>: {company_data.get("top_management_name")}\n'
                 f'■ <b>ОГРН</b>: {company_data.get("company_ogrn")}\n'
                 f'■ <b>ИНН</b>: {company_data.get("company_inn")}\n'
                 f'■ <b>Адрес компании</b>: {company_data.get("company_address")}\n',
            reply_markup=inline_keyboard
        )
        # Сбрасываем состояние
        company_obj.state_name = None
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Найдены данные о компании клиента. Отправлено предложение их подтвердить.',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
    # Если ничего нет, то спросить ИНН
    else:
        company_obj.state_name = 'input_inn'
        await message.reply_text(
            text=f'📍Введите ИНН организации',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Не найдена информация о компании клиента по названию. Запрашиваем у клиента ИНН.',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


@Client.on_callback_query(reject_comp_by_name_filter)
async def reject_comp_by_name(client, callback_query):
    """Хэндлер на нажатие кнопки отклонения правильности данных компании, после запроса данных по её названию"""

    TEMPORARY_STORAGE.pop(callback_query.from_user.id)
    company_obj = USER_DATA_STORAGE[callback_query.from_user.id]['company']
    company_obj.state_name = 'input_inn'
    await callback_query.edit_message_text(
        text=f'📍Введите ИНН организации',
        reply_markup=CANCEL_INPUT_COMPANY_DATA
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Клиент отклонил данные компании, найденные по названию. Запрашиваем у клиента ИНН.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_message(filters.private & write_inn_filter)
async def write_inn(client, message):
    """Хэндлер для записи ИНН и запрос по нему данных компании через DaData"""

    company_obj = USER_DATA_STORAGE[message.from_user.id]['company']
    write_result = await company_obj.set_inn(inn=message.text.replace(' ', ''))
    if write_result:

        # Подтягиваем инфу через DaData
        company_data = DadataHelper.find_company_data_by_inn(company_obj.inn)
        if company_data:
            TEMPORARY_STORAGE[message.from_user.id] = company_data
            # Если DaData дала результат
            inline_keyboard = await confirm_or_reject_company_keyboard(reject_step='inn')
            await message.reply_text(
                text=f'{emoji.CARD_INDEX_DIVIDERS}<b>Пожалуйста, проверьте данные компании, которые мне удалось найти.</b>\n\n'
                     f'■ <b>Название компании</b>: {company_data.get("company_name")}\n'
                     f'■ <b>Должность управляющего</b>: {company_data.get("top_management_post")}\n'
                     f'■ <b>Ф.И.О. управляющего</b>: {company_data.get("top_management_name")}\n'
                     f'■ <b>ОГРН</b>: {company_data.get("company_ogrn")}\n'
                     f'■ <b>ИНН</b>: {company_data.get("company_inn")}\n'
                     f'■ <b>Адрес компании</b>: {company_data.get("company_address")}\n',
                reply_markup=inline_keyboard
            )
            # Сбрасываем состояние
            company_obj.state_name = None
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=message.from_user.id,
                username=message.from_user.username,
                msg_text=f'Найдены данные о компании по ИНН. Клиенту отправлено предложение их подтвердить.',
                last_name=message.from_user.last_name,
                name=message.from_user.first_name
            )
        else:
            company_obj.state_name = 'input_ogrn'
            await message.reply_text(
                text=f'📍Введите ОГРН организации',
                reply_markup=CANCEL_INPUT_COMPANY_DATA
            )
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=message.from_user.id,
                username=message.from_user.username,
                msg_text=f'НЕ найдены данные о компании по ИНН. Запрос ОГРН.',
                last_name=message.from_user.last_name,
                name=message.from_user.first_name
            )

    else:
        await message.reply_text(
            text='❕<b>Пожалуйста, введите корректный ИНН</b>\n\n'
                 f'📍Введённый Вами ИНН <code>{message.text}</code> не соответствует формату.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Клиент ввёл ИНН неверного формата. Запрашиваем повторно.\nВот, что ввёл клиент:\n\t{message.text}',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


@Client.on_callback_query(reject_comp_data_by_inn_filter)
async def reject_comp_data_by_inn(client, callback_query):
    """Обработчик на нажатие кнопки отмены подтверждения данных компании после запроса по ИНН"""

    TEMPORARY_STORAGE.pop(callback_query.from_user.id)
    company_obj = USER_DATA_STORAGE[callback_query.from_user.id]['company']
    company_obj.state_name = 'input_ogrn'
    await callback_query.edit_message_text(
        text=f'📍Введите ОГРН организации',
        reply_markup=CANCEL_INPUT_COMPANY_DATA
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Клиент не подтвердил данные его компании, найденные по ИНН. Запрашиваем ОГРН.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_message(filters.private & write_ogrn_filter)
async def write_ogrn(client, message):
    """Обработчик для записи ОГРН, поиска компании по нему в ДаДата и сопутствующая этому логика."""

    company_obj = USER_DATA_STORAGE[message.from_user.id]['company']
    write_result = await company_obj.set_ogrn(ogrn=message.text.replace(' ', ''))
    if write_result:
        # Если ОГРН успешно записан, запрашиваем контактный телефон
        await message.reply_text(
            text=f'📱Введите контактный номер телефона.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        company_obj.state_name = 'input_telephone'
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Запись ОГРН клиента и запрос номера телефона',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
    else:
        await message.reply_text(
            text='❕<b>Пожалуйста, введите корректный ОГРН</b>\n\n'
                 f'📍Введённый Вами ОГРН <code>{message.text}</code> не соответствует формату.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Клиент ввёл некорректный ОГРН. Запрашиваем повторно.\nВот, что ввёл клиент:\n\t{message.text}',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


@Client.on_message(filters.private & write_telephone_filter)
async def write_telephone(client, message):
    """Обработчик для записи контактного телефона."""

    user_obj = USER_DATA_STORAGE[message.from_user.id]['user']
    company_obj = USER_DATA_STORAGE[message.from_user.id]['company']
    write_result = await user_obj.set_telephone(telephone=message.text)
    if write_result:
        await message.reply_text(
            text=f'📧Введите контактный EMAIL.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        user_obj.state_name = 'input_email'
        # Не забываем сбросить состояние по объекту Company, чтобы не попадать в ненужные хэндлеры
        company_obj.state_name = None
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Сохраняем контактный телефон клиента и запрашиваем EMAIL.',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
    else:
        await message.reply_text(
            text='❕<b>Пожалуйста, введите корректный номер телефона</b>\n\n'
                 f'📱Введённый Вами номер телефона <code>{message.text}</code> не соответствует формату.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Клиент ввёл номер телефона неверного формата. Запрашиваем повторно.\n'
                     f'Вот, что ввёл клиент:\n\t{message.text}',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


@Client.on_message(filters.private & write_email_filter)
async def write_email(client, message):
    """Обработчик для записи контактного мыла."""

    user_obj = USER_DATA_STORAGE[message.from_user.id]['user']
    write_result = await user_obj.set_email(email=message.text)
    if write_result:
        await message.reply_text(
            text=f'🗺Введите адрес компании.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        user_obj.state_name = 'input_address'
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Записываем EMAIL клиента и запрашиваем адрес компании.',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
    else:
        await message.reply_text(
            text='❕<b>Пожалуйста, введите корректный EMAIL</b>\n\n'
                 f'📧Введённый Вами EMAIL <code>{message.text}</code> не соответствует формату.',
            reply_markup=CANCEL_INPUT_COMPANY_DATA
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Клиент ввёл некорректный EMAIL. Запрашиваем повторно.\nВот, что ввёл клиент:\n\t{message.text}',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


@Client.on_message(filters.private & write_address_filter)
async def write_address(client, message):
    """Хэндлер для записи адреса компании"""

    user_obj = USER_DATA_STORAGE[message.from_user.id]['user']
    company_obj = USER_DATA_STORAGE[message.from_user.id]['company']
    company_obj.address = message.text
    company_obj.state_name = 'input_top_manage_post'
    user_obj.state_name = None  # Сбрасываем состояние по объекту пользователя
    await message.reply_text(
        text=f'💼Введите название должности главного управляющего лица (Директор, Управляющий и т. д.)',
        reply_markup=CANCEL_INPUT_COMPANY_DATA
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=message.from_user.id,
        username=message.from_user.username,
        msg_text=f'Записываем адрес компании и запрашиваем наименование должности управляющего лица компании.',
        last_name=message.from_user.last_name,
        name=message.from_user.first_name
    )


@Client.on_message(filters.private & write_top_management_post_filter)
async def write_top_management_post(client, message):
    """Хэндлера для записи должности главного управленца компании"""

    company_obj = USER_DATA_STORAGE[message.from_user.id]['company']
    company_obj.top_management_post = message.text
    company_obj.state_name = 'input_top_manage_name'
    await message.reply_text(
        text=f'🧔Введите ФИО главного управляющего компании.',
        reply_markup=CANCEL_INPUT_COMPANY_DATA
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=message.from_user.id,
        username=message.from_user.username,
        msg_text=f'Записываем должность управляющего лица компании и запрашиваем его ФИО.',
        last_name=message.from_user.last_name,
        name=message.from_user.first_name
    )


@Client.on_message(filters.private & write_top_management_name_filter)
async def write_top_management_name(client, message):
    """Хэндлер для записи ФИО главного управленца компании"""

    company_obj = USER_DATA_STORAGE[message.from_user.id]['company']
    user_obj = USER_DATA_STORAGE[message.from_user.id]['user']
    company_obj.top_management_name = message.text
    company_obj.state_name = None
    # Отправляем данные компании и пользователя для записи в БД
    result_comp = await company_obj.write_company_data()
    result_user = await user_obj.write_user_in_db()
    if result_comp and result_user:
        await message.reply_text(
            text=f'🏢<b>Спасибо, информация о компании записана.</b>\n\n'
                 f'🏦Готовы ли Вы внести реквизиты банка?',
            reply_markup=AFTER_ADD_COMPANY_DATA_KEYBOARD
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Предлагаем клиенту ввести реквизиты банка.',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
    else:
        await message.reply_text(
            text=f'🛠Не удалось записать данные, мы уже решаем эту проблему.\n'
                 f'Попробуйте повторить позже.',
            reply_markup=START_FIRST_MEETING
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Ошибка при записи данных о компании клиента! Клиенту предложено повторить ввод позже.',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
