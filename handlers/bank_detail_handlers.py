from pyrogram import Client, emoji, filters

from bot_objects.user_data_objects import BankDetail
from filters.bank_detail_filters import start_input_bank_detail_filter, cancel_bank_detail_input_filter, \
    write_bik_filter, write_cor_a_filter, write_bank_name_filter, write_rs_filter, confirm_bank_data_filter, \
    reject_bank_data_filter
from keyboards.bot_keyboards import CANCEL_INPUT_BANK_DETAIL_KBRD, AFTER_ADD_COMPANY_DATA_KEYBOARD, \
    confirm_or_reject_bank_keyboard, BEFORE_CALCULATE_KEYBOARD
from secondary_functions.dadata_helper import DadataHelper
from secondary_functions.different_functions import get_company_data_from_storage_or_req
from secondary_functions.req_to_bot_api import get_for_crt_comp_and_bank_dtail_in_btrx, post_send_msg_to_open_line
from settings.config import USER_DATA_STORAGE, TEMPORARY_STORAGE


@Client.on_callback_query(cancel_bank_detail_input_filter)
async def cancel_bank_detail_input(client, callback_query):
    """Хэндлер для кнопки отмены ввода банковских реквизитов."""
    bank_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('bank')
    bank_obj.state_name = None
    await callback_query.edit_message_text(
        text=f'{emoji.CROSS_MARK}Вы отменили ввод реквизитов банка{emoji.BANK}',
        reply_markup=AFTER_ADD_COMPANY_DATA_KEYBOARD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text='Клиент отменил ввод банковских реквизитов',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_callback_query(start_input_bank_detail_filter)
async def start_input_bank_detail(client, callback_query):
    """Хэндлер старта сбора реквизитов банка. Запросим БИК"""

    # Создаём инстанс класса BankDetail
    comp_obj = await get_company_data_from_storage_or_req(user_id=callback_query.from_user.id)
    bank_obj = BankDetail(inn_comp=comp_obj.inn)
    bank_obj.state_name = 'bik_input'
    USER_DATA_STORAGE[callback_query.from_user.id]['bank'] = bank_obj
    await callback_query.edit_message_text(
        text=f'📎Введите, пожалуйста, <b>БИК</b> Вашего банка',
        reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text='Начат сбор банковских реквизитов. Запрошен БИК.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_message(filters.private & write_bik_filter)
async def write_bik(client, message):
    """Хэндлер для записи БИК, поиск по нему реквизитов банка."""

    bank_obj = USER_DATA_STORAGE[message.from_user.id].get('bank')
    write_result = await bank_obj.set_bik(bik=message.text.replace(' ', ''))
    if write_result:    # Если пользовательский БИК прошёл валидацию и был успешно записан в класс
        bank_data = DadataHelper.find_bank_data_by_bik(bik=bank_obj.bik)
        if bank_data:   # Если ДаДата дала нам результат
            TEMPORARY_STORAGE[message.from_user.id] = bank_data
            bank_obj.state_name = None
            inline_keyboard = await confirm_or_reject_bank_keyboard()
            await message.reply_text(
                text=f'<b>Вот, что мне удалось найти. Проверьте, пожалуйста, верны ли реквизиты.</b>\n\n'
                     f'<b>Название банка:</b> {bank_data.get("bank_name")}\n'
                     f'<b>Корресп. счёт:</b> {bank_data.get("bank_ca")}\n'
                     f'<b>БИК банка:</b> {bank_data.get("bank_bik")}\n',
                reply_markup=inline_keyboard
            )
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=message.from_user.id,
                username=message.from_user.username,
                msg_text='Найден банк по БИК. Клиентe предложено его подтвердить',
                last_name=message.from_user.last_name,
                name=message.from_user.first_name
            )
        else:   # Если ДаДата не вернула ничего
            bank_obj.state_name = 'input_cor_a'
            await message.reply_text(
                text=f'📎Введите <b>Кор. счет:</b>',
                reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
            )
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=message.from_user.id,
                username=message.from_user.username,
                msg_text='Банк клиента НЕ БЫЛ НАЙДЕН по БИК. Запрашиваем кор.счёт.',
                last_name=message.from_user.last_name,
                name=message.from_user.first_name
            )

    else:   # Если пользовательский БИК не прошёл валидацию
        await message.reply_text(
            text=f'❕ Пожалуйста, введите корректный <b>БИК</b>.\n\n'
                 f'✖ Значение <code>{message.text}</code> не соответствует формату.',
            reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Клиент ввёл БИК, который не соответствует формату.\nВот, что прислал клиент:\n\t{message.text}',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


@Client.on_callback_query(confirm_bank_data_filter)
async def confirm_bank_data(client, callback_query):
    """Хэндлер на кнопку подтверждения банковских данных из ДаДата."""

    bank_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('bank')
    bank_data = TEMPORARY_STORAGE[callback_query.from_user.id]
    bank_obj.bik = bank_data.get("bank_bik")
    bank_obj.cor_a = bank_data.get("bank_ca")
    bank_obj.bank_name = bank_data.get("bank_name")
    # Запрашиваем РС
    bank_obj.state_name = 'input_rs'
    await callback_query.edit_message_text(
        text=f'📎Введите <b>расчётный счёт</b>',
        reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Клиент подтвердил найденные реквизиты банка. Запрашиваем расчётный счёт.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_callback_query(reject_bank_data_filter)
async def reject_bank_data(client, callback_query):
    """Хэндлер на кнопку НЕ подтверждения банковских данных из ДаДата."""

    bank_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('bank')
    bank_obj.state_name = 'input_cor_a'
    await callback_query.edit_message_text(
        text=f'📎Введите <b>Кор. счет:</b>',
        reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Клиент НЕ подтвердил найденные реквизиты банка. Запрашиваем кор.счёт.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_message(filters.private & write_cor_a_filter)
async def write_cor_a(client, message):
    """Хэндлер для записи кор.счёта."""

    bank_obj = USER_DATA_STORAGE[message.from_user.id].get('bank')
    write_result = await bank_obj.set_cor_a(cor_a=message.text.replace(' ', ''))
    if write_result:
        bank_obj.state_name = 'input_bank_name'
        await message.reply_text(
            text=f'📎Введите <b>название банка</b>',
            reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Записываем кор.счёт. Запрашиваем название банка.',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
    else:
        await message.reply_text(
            text=f'❕ Пожалуйста, введите корректный <b>кор.счёт</b>.\n\n'
                 f'✖ Значение <code>{message.text}</code> не соответствует формату.',
            reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Клиент ввёл некорректный кор.счёт. Запрашиваем повторно.\nВот, что ввёл клиент:\n\t{message.text}',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


@Client.on_message(filters.private & write_bank_name_filter)
async def write_bank_name(client, message):
    """Хэндлер для записи названия банка."""

    bank_obj = USER_DATA_STORAGE[message.from_user.id].get('bank')
    bank_obj.bank_name = message.text
    bank_obj.state_name = 'input_rs'
    await message.reply_text(
        text=f'📎Введите <b>расчётный счёт</b>',
        reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=message.from_user.id,
        username=message.from_user.username,
        msg_text=f'Записываем название банка клиента. Запрашиваем расчётный счёт.',
        last_name=message.from_user.last_name,
        name=message.from_user.first_name
    )


@Client.on_message(filters.private & write_rs_filter)
async def write_rs(client, message):
    """Хэндлер для записи расчётного счёта."""

    bank_obj = USER_DATA_STORAGE[message.from_user.id].get('bank')
    write_result = await bank_obj.set_rs(rs=message.text.replace(' ', ''))
    if write_result:
        # Сперва предлагаем следующий шаг, затем выполняем запросы в Битрикс и обрабатываем ответы. Чтобы клиент не ждал
        bank_obj.state_name = None
        this_msg = await message.reply_text(
            text=f'{emoji.BANK}<b>Спасибо, реквизиты банка записаны</b>\n\n'
                 f'📒Вы можете приступить к выбору опций бухгалтерского сопровождения.',
            reply_markup=BEFORE_CALCULATE_KEYBOARD
        )
        response = await bank_obj.write_company_bank_details()
        add_to_btrx_rslt = await get_for_crt_comp_and_bank_dtail_in_btrx(tlg_id=message.from_user.id)
        if not response and not add_to_btrx_rslt:   # Если неудачные запросы
            await this_msg.edit_text(   # Изменяем ранее отправленное сообщение
                text=f'🛠Не удалось записать Ваши данные. Мы уже решаем эту проблему.\n'
                     f'Пожалуйста, попробуйте повторить ввод позже.',
                reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
            )
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=message.from_user.id,
                username=message.from_user.username,
                msg_text=f'Не удалось записать реквизиты банка клиента! Ему было предложено повторить ввод позже.',
                last_name=message.from_user.last_name,
                name=message.from_user.first_name
            )
        else:   # В случае успешной записи данных клиента
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=message.from_user.id,
                username=message.from_user.username,
                msg_text=f'Реквизиты банка клиента успешно записаны! Отправлено предложение выбрать опции бух.сопров.',
                last_name=message.from_user.last_name,
                name=message.from_user.first_name
            )
    else:
        await message.reply_text(
            text=f'❕ Пожалуйста, введите корректный <b>расчёстный счёт</b>.\n\n'
                 f'✖ Значение <code>{message.text}</code> не соответствует формату.',
            reply_markup=CANCEL_INPUT_BANK_DETAIL_KBRD
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.from_user.id,
            username=message.from_user.username,
            msg_text=f'Клиент ввёл некорректный расчётный счёт. Запрашиваем повторно. '
                     f'Вот, что ввёл клиент:\n\t{message.text}',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
