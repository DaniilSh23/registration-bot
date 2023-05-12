import aiohttp
from pyrogram import Client, filters, emoji

from bot_objects.user_data_objects import User
from filters.main_filters import display_bank_data_filter, display_company_data_filter, plug_handler_filter, \
    i_paid_filter, rate_bot_filter, filter_input_rating, filter_rating_without_comment
from keyboards.bot_keyboards import START_FIRST_MEETING, BEFORE_CALCULATE_KEYBOARD, RESTART_BOT_KBRD, \
    INPUT_BANK_DETAIL_KBRD, INFO_ABOUT_BANK_KBRD, INFO_ABOUT_COMPANY_KBRD, I_PAID_KBRD, \
    I_SIGNED_KBRD, form_webapp_kbrd, NO_RATING_COMMENTS_KBRD, RATE_BOT_KBRD
from secondary_functions.different_functions import get_instance_from_storage_or_req, get_bank_data_from_storage_or_req, \
    get_company_data_from_storage_or_req
from secondary_functions.req_to_bot_api import post_send_msg_to_open_line, get_open_line_create, \
    post_for_add_bot_rating, get_form_link_for_pers_data, get_for_add_task_to_lawyer, get_for_manage_reminds
from settings.config import USER_DATA_STORAGE, ABOUT_MCHD_URL, TEMPORARY_STORAGE
from loguru import logger


@Client.on_message(filters.private & filters.bot & filters.document)
async def send_paid_btn_after_documents(client, message):
    """
    Отправка кнопки Я ОПЛАТИЛ после того, как от лица бота сырым запросом отправим ДОГОВОР.
    """
    if message.caption == '📄 Ваш договор.':
        await message.reply_text(
            text=f'<b>Спасибо что выбрали компанию ЦФУ.</b>\n\n'
                 f'Ознакомьтесь с договором, оплатите счет, ожидайте документы по ЭДО(поступят на электронную почту).'
                 f'\n\n<b>После оплаты нажмите кнопку \n<u>Я ОПЛАТИЛ</u></b>',
            reply_markup=I_PAID_KBRD
        )
        # Создаём отложенную задачу для напоминания о необходимости оплаты
        await get_for_manage_reminds(tlg_id=message.chat.id, reminder_type='p', act='add')
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.chat.id,
            username=message.from_user.username,
            msg_text='СЧЁТ и ДОГОВОР отправлены клиенту.',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )


@Client.on_message(filters.private & filters.bot)
async def handling_own_updates(client, message):
    """
    Хэндлер для обработки собственных апдейтов бота, когда они прилетают из вне.
    """

    # Обработка сообщения - триггера о заполнении перс.данных. клиентом в Битриксе
    if message.text == '*_successful_recording_of_personal_data_*':
        logger.info('Получен триггер о заполнении перс.данных клиентом.')
        await message.delete()
        # Достаём из хранилища старое сообщение с кнопкой на веб-форму и удаляем его
        msg_id_for_del = TEMPORARY_STORAGE[message.chat.id].get('msg_for_del')
        user_obj = USER_DATA_STORAGE[message.chat.id]['user']
        await client.delete_messages(chat_id=message.chat.id, message_ids=msg_id_for_del)

        # Отправляем следующий шаг
        # TODO: раскоментить текст сообщения и отправку фотки с клавиатурой "Я ПОДПИСАЛ", когда они разродятся
        # text_for_message = f'📧Спасибо, на вашу <b>почту (<code>{user_obj.email}</code> придет письмо со ссылкой на МЧД</b>\n(пример письма на фото).' \
        #                    f'\n\n✍Подписание производится <b>с компьютера</b>, не забудьте <b>вставить ЭЦП</b>.'
        # await message.reply_photo(
        #     photo='mail_example.jpeg',
        #     caption=text_for_message,
        #     reply_markup=I_SIGNED_KBRD,
        #     disable_notification=True
        # )
        # TODO: когда разродятся, отправку сообщения ниже и предложение поставить оценку нужно будет удалить
        text_for_message = f'Спасибо.\n' \
                           f'📞Для <b>подписания МЧД Вам позвонит наш специалист</b>.\n' \
                           f'💻Подписание <b>будет производиться с Вашего компьютера</b>, не забудьте вставить ЭЦП.'
        await message.reply_text(
            text=text_for_message,
        )
        await message.reply_text(
            text=f'Благодарим Вас за уделённое время.\n\n'
                 f'⭐️Оцените взаимодействие с ботом.',
            reply_markup=RATE_BOT_KBRD
        )

        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=message.chat.id,
            username=message.from_user.username,
            msg_text='Клиент заполнил персональные данные. '
                     'Сообщаем ему о том, что на почту придёт письмо со ссылкой на МЧД',
            last_name=message.from_user.last_name,
            name=message.from_user.first_name
        )
        # TODO: раскоментить постановку задачи юристу и создания задачи для напоминания потом, когда они разродятся.
        # # Постановка задачи (тип 2 - МЧД) юристу
        # await get_for_add_task_to_lawyer(tlg_id=message.chat.id, task_type=2)
        # # Cоздаём отложенную задачу для напоминания о необходимости подписи
        # await get_for_manage_reminds(tlg_id=message.chat.id, reminder_type='s', act='add')

    else:  # Игнорируем все иные апдейты
        logger.info(f'Бот отправляет сообщение в чат с ID {message.chat.id}')


@Client.on_message(filters.command(['start']))
async def start_handler(client, message):
    """
    Хэндлер на команду /start.
    Команда должна выполняться с параметром, который является ID сделки из Битрикса.
    Без параметра бот проверяет есть ли пользователь в БД и, если нет, то запрашивает ID сделки.
    """

    if len(message.command) < 2:
        # Вызвать функцию, которая проверит словарь бота или БД на наличие данных об этом пользователе
        result_obj = await get_instance_from_storage_or_req(user_id=message.from_user.id)
        if not result_obj:  # Если не получен объект пользователя
            logger.warning(f'При перезапуске бота пользователем TG ID == {message.from_user.id} '
                           f'не удалось получить или создать объект пользователя. '
                           f'Скорее всего не получен ответ от API веб-приложения')
        else:   # Объект пользователя получен
            result_obj.state_name = None
            company_obj = await get_company_data_from_storage_or_req(user_id=message.from_user.id)
            if not company_obj:     # Если не получен объект компании
                logger.warning(f'При перезапуске бота пользователем TG ID == {message.from_user.id} '
                               f'не удалось получить или создать объект компании пользователя. '
                               f'Скорее всего не получен ответ от API веб-приложения')
            else:   # Объект компании получен
                company_obj.state_name = None  # Очищаем состояние компании пользователя
                bank_obj = await get_bank_data_from_storage_or_req(user_id=message.from_user.id)
                if not bank_obj:    # Если не получен объект банка
                    logger.warning(f'При перезапуске бота пользователем TG ID == {message.from_user.id} '
                                   f'не удалось получить или создать объект банк.данных пользователя. '
                                   f'Скорее всего не получен ответ от API веб-приложения')
                else:   # Объект банка получен
                    bank_obj.state_name = None  # Очищаем состояние банка пользователя
        if result_obj:
            await message.reply_text(
                text=f'{emoji.CYCLONE}<b>Вы перезапустили бота.</b>\n\n'
                     f'<b>Вы можете:</b>\n'
                # f'📒<u>Выбрать опции бух.сопровождения</u>\n'
                # f'{emoji.BANK}Посмотреть реквизиты банка\n'
                # f'{emoji.OFFICE_BUILDING}Посмотреть данные компании\n'
                     f'{emoji.PEN}Заново внести данные компании и банка\n',
                reply_markup=RESTART_BOT_KBRD
            )
            USER_DATA_STORAGE[message.from_user.id] = {'user': result_obj}
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=message.from_user.id,
                username=message.from_user.username,
                msg_text='Перезапуск бота',
                last_name=message.from_user.last_name,
                name=message.from_user.first_name
            )
        else:
            # Если данных нет, то проинформируем, что для работы нужен ID сделки. Админам будем давать специальную ссылку
            await message.reply_text(
                text=f'{emoji.PERSON_SHRUGGING}К сожалению, я не могу предоставить Вам доступ.\n\n'
                     f'{emoji.TECHNOLOGIST_LIGHT_SKIN_TONE}Пожалуйста, обратитесь к менеджеру для получения персональной ссылки.'
            )
    else:  # Если пользователь стартует бота, перейдя по спец. ссылке
        # Вытаскиваем ID сделки
        deal_id = message.command[1]
        # Создаём инстанс класса User и добавляем его в словарь - хранилище
        user_obj = User(tlg_id=message.from_user.id, deal_id=deal_id, tlg_username=message.from_user.username)
        USER_DATA_STORAGE[message.from_user.id] = {
            'user': user_obj
        }
        # Создаём или обновляем в БД запись о пользователе (ключ tlg_id)
        result = await user_obj.write_user_in_db()
        if not result:
            await message.reply_text(
                text=f'{emoji.HAMMER_AND_WRENCH}Ведутся технические работы. Мы скоро закончим',
                # reply_markup=START_FIRST_MEETING
            )
        else:
            # Приветственное сообщение, предложение ввести данные компании
            await message.reply_text(
                text=f'{emoji.HANDSHAKE}Здравствуйте.\n'
                     f'Я бот-регистратор от компании <b>"ЦЕНТР ФИНАНСОВОГО УПРАВЛЕНИЯ"</b>\n\n'
                     f'{emoji.CLIPBOARD}Моя основная задача - автоматизация сбора информации для дальнейшего сотрудничества.'
                     f'\n\n{emoji.PEN}Если Вы готовы, то давайте приступим.',
                reply_markup=START_FIRST_MEETING
            )
            # Создаём чат для записи в нём действий с ботом
            req_rslt = await get_open_line_create(tlg_id=message.from_user.id)
            if req_rslt:
                logger.success(f'Успешное создание чата в Битриксе для сделки с ID {message.command[1]}')
            else:
                logger.critical(f'Создание чате в Битриксе для сделки ID {message.command[1]} НЕ УДАЛОСЬ!')


@Client.on_callback_query(display_bank_data_filter)
async def display_bank_data(client, callback_query):
    """Отображаем банковские реквизиты клиента"""

    bank_obj = await get_bank_data_from_storage_or_req(user_id=callback_query.from_user.id)
    if bank_obj and bank_obj.bik:
        text_for_message = f'{emoji.BANK} <b>Реквизиты Вашего банка:</b>\n\n' \
                           f'■ <b>Наименование банка:</b> <code>{bank_obj.bank_name}</code>\n' \
                           f'■ <b>БИК:</b> <code>{bank_obj.bik}</code>\n' \
                           f'■ <b>Расч.счёт:</b> <code>{bank_obj.rs}</code>\n' \
                           f'■ <b>Кор.счёт:</b> <code>{bank_obj.cor_a}</code>\n'
        await callback_query.edit_message_text(
            text=text_for_message,
            reply_markup=INFO_ABOUT_BANK_KBRD
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            msg_text='Получены реквизиты банка клиента, отправлено предложение их подтвердить.',
            last_name=callback_query.from_user.last_name,
            name=callback_query.from_user.first_name
        )
    else:
        await callback_query.edit_message_text(
            text=f'🤷Реквизиты банка не найдены.\n'
                 f'Предлагаю их заполнить.',
            reply_markup=INPUT_BANK_DETAIL_KBRD
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            msg_text='Реквизиты банка клиента не найдены. Предложено их заполнить.',
            last_name=callback_query.from_user.last_name,
            name=callback_query.from_user.first_name
        )


@Client.on_callback_query(display_company_data_filter)
async def display_company_data(client, callback_query):     # TODO: возможно эту хрень надо убрать
    """Отображаем данные о компании клиента"""

    comp_obj = await get_company_data_from_storage_or_req(user_id=callback_query.from_user.id)
    if comp_obj:
        text_for_message = f'{emoji.OFFICE_BUILDING} <b>Данные компании:</b>\n\n' \
                           f'■ <b>Название компании:</b> {comp_obj.comp_name}\n' \
                           f'■ <b>Адрес компании:</b> {comp_obj.address}\n' \
                           f'■ <b>ОГРН:</b> {comp_obj.ogrn}\n' \
                           f'■ <b>ИНН:</b> {comp_obj.inn}\n' \
                           f'■ <b>Должность управляющего лица:</b> {comp_obj.top_management_post}\n' \
                           f'■ <b>ФИО управляющего лица:</b> {comp_obj.top_management_name}\n'
        await callback_query.edit_message_text(
            text=text_for_message,
            reply_markup=INFO_ABOUT_COMPANY_KBRD
        )
    else:
        await callback_query.edit_message_text(
            text=f'🛠Неудачный запрос. Мы уже решаем эту проблему.\n'
                 f'Пожалуйста, попробуйте позже.',
            reply_markup=BEFORE_CALCULATE_KEYBOARD
        )


@Client.on_callback_query(i_paid_filter)
async def i_paid_handler(client, callback_query):
    """
    Хэндлер для кнопки Я ОПЛАТИЛ.
    """
    await callback_query.answer('Обработка кнопки оплаты')

    form_link = await get_form_link_for_pers_data(tlg_id=callback_query.from_user.id)

    if form_link.get("form_link"):   # Если ссылка на форму была успешно получена
        inline_kbrd = await form_webapp_kbrd(form_link=form_link.get("form_link"))
        # Предложение приступить к заполнению персональных данных
        edited_message = await callback_query.edit_message_text(
            text='🧾Спасибо что оплатили.\n\n<b>Для дальнейшего взаимодействия</b> в ИФНС от Вашего лица, '
                 'необходимо заполнить <b>машиночитаемую доверенность</b>.\n'
                 f'Подробнее о МЧД можно прочитать <a href="{ABOUT_MCHD_URL}">здесь</a>.\n\n'
                 f'☝<i>Нажимая на кнопку <b>"Заполнить персональные данные"</b>, Вы даете свое согласие на '
                 f'обработку и хранение персональных данных.</i>\n\n'
                 f'🌐<i>Если Вы используете <b>браузерную версию Telegram, то '
                 f'<a href="{form_link.get("form_link")}">'
                 f'ваша форма сбора персональных данных находится здесь</a></b></b></i>',
            reply_markup=inline_kbrd,
            disable_web_page_preview=True
        )
        # Сохраним ID этого сообщения, чтобы его удалить, когда будут заполнены персональные данные
        TEMPORARY_STORAGE[callback_query.from_user.id] = {'msg_for_del': edited_message.id}
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            msg_text='Нажата кнопка Я ОПЛАТИЛ, предложено внести персональные данные. Отправлена кнопка с формой',
            last_name=callback_query.from_user.last_name,
            name=callback_query.from_user.first_name
        )
    else:   # Ссылка на форму не получена
        await callback_query.edit_message_text(
            text=f'🛠Не удалось получить данные для следующего шага регистрации. Мы уже решаем эту проблему.\n'
                 f'Пожалуйста, попробуйте нажать кнопку "Я ОПЛАТИЛ" позже.',
        )
        await post_send_msg_to_open_line(
            tlg_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            msg_text='Нажата кнопка Я ОПЛАТИЛ.\nНе удалось получить ссылку на форму сбора персональных данных. '
                     'Клиенту было предложено повторить заполнение позже.',
            last_name=callback_query.from_user.last_name,
            name=callback_query.from_user.first_name
        )
    # Постановка задачи (тип 1 - ЭДО) юристу
    await get_for_add_task_to_lawyer(tlg_id=callback_query.from_user.id, task_type=1)
    # Удаляем отложенную задачу для напоминания о необходимости оплаты
    await get_for_manage_reminds(tlg_id=callback_query.from_user.id, reminder_type='p', act='del')


@Client.on_callback_query(rate_bot_filter)
async def rate_bot_handler(client, callback):
    """Хэндлер получения оценки бота"""

    if callback.data.split()[1] != '5':     # Если оценка ниже 5, то запрашиваем коммент
        msg_fr_dlt = await callback.edit_message_text(
            text=f'⭐️<b>Спасибо, Ваша оценка принята.</b>\n\n'
                 f'❔Расскажите, что нам нужно улучшить',
            reply_markup=NO_RATING_COMMENTS_KBRD
        )
        # Сохраняем сообщение, чтобы потом его удалить, когда будет записан коммент клиента
        TEMPORARY_STORAGE[callback.from_user.id] = {'msg_fr_dlt': msg_fr_dlt}
        user_obj = USER_DATA_STORAGE[callback.from_user.id]['user']
        user_obj.state_name = 'input_rating_comment'
    else:   # Иначе не запрашиваем коммент
        await callback.edit_message_text(
            text=f'⭐️<b>Спасибо, Ваша оценка принята.</b>'
        )

    # Отправка запроса к Джанго для сохранения оценки пользователя
    req_rslt = await post_for_add_bot_rating(tlg_id=callback.from_user.id, rating=callback.data.split()[1])
    if req_rslt:
        wrt_rslt_txt = 'Оценка сохранена в админ-панели.'
    else:
        wrt_rslt_txt = 'Оценка НЕ сохранена в админ-панели.'

    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Поставлена оценка боту - {callback.data.split()[1]}. {wrt_rslt_txt}',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )


@Client.on_message(filters.private & filter_input_rating)
async def input_rating_handler(client, message):
    """Хэндлер приёма коммента к оценке клиента."""

    await message.reply_text(
        text=f'☑️Ваш отзыв записан.\n\n<b>Спасибо. Нам очень важно Ваше мнение.</b>',
    )
    # Отправка запроса к Джанго для сохранения оценки пользователя
    req_rslt = await post_for_add_bot_rating(tlg_id=message.from_user.id, comment=message.text)
    if req_rslt:
        wrt_rslt_txt = 'Комментарий сохранен в админ-панели.'
    else:
        wrt_rslt_txt = 'Комментарий НЕ сохранен в админ-панели.'
    # Удаляем сообщение, где предлагали ввести коммент, чтобы оно не висело с кнопкой
    await TEMPORARY_STORAGE[message.from_user.id]['msg_fr_dlt'].delete()
    # Очищаем состояние ожидания ввода коммента к оценке
    user_obj = USER_DATA_STORAGE[message.from_user.id]['user']
    user_obj.state_name = None
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=message.from_user.id,
        username=message.from_user.username,
        msg_text=f'Клиент прокомментировал оценку бота. {wrt_rslt_txt}\nТекст комментария:\n{message.text}.',
        last_name=message.from_user.last_name,
        name=message.from_user.first_name
    )


@Client.on_callback_query(filter_rating_without_comment)
async def rating_without_comment(client, callback):
    """Хэндлер для кнопки БЕЗ КОММЕНТАРИЕВ."""
    await callback.answer(text='Оценка без комментария')
    await callback.edit_message_text(text=f'<b>Спасибо, что выбрали ЦФУ</b>')
    # Очищаем состояние ожидания ввода коммента к оценке
    user_obj = USER_DATA_STORAGE[callback.from_user.id]['user']
    user_obj.state_name = None


@Client.on_callback_query(plug_handler_filter)
async def plug_handler(client, callback_query):
    """
    Хэндлер - заглушка.
    Для инлайн кнопок, которые несут чисто информ. функцию, без выполнения каких-либо действий
    """
    await callback_query.answer('...')


@Client.on_message(filters.command(['test']))
async def web_app_test(client, message):
    """Тест всякого"""

    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url='http://127.0.0.1:8000/reg_bot/cmn_btrx/?id=86920', data={}) as response:
    #         if response.status == 200:
    #             logger.success(f'ПОСТ запрос на коммон битрикс отправлен')
    #         else:
    #             logger.warning(f'ПОСТ запрос на коммон битрикс отправлен')

    await message.reply_text(
        text='отправка пост запроса на свою же приложуху',
        # reply_markup=await form_webapp_kbrd(form_link=link)
    )
