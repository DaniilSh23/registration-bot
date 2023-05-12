from pyrogram import Client, emoji

from bot_objects.calculator_objects import CalcOptions
from filters.calculator_filters import start_calculate_filter, cancel_calc_filter, ind_pred_tax_system_filter, \
    ask_patent_numbers_filter, plus_patent_filter, minus_patent_filter, move_to_business_filter, \
    without_mix_tax_systm_filter, ooo_tax_system_filter, choice_employees_number_filter, plus_employee_filter, \
    minus_employee_filter, source_docs_fst_step_filter, \
    input_numb_docs_for_prod_acc_filter, minus_prod_doc_filter, plus_prod_doc_filter, need_product_reporting_filter, \
    show_buh_result_filter, calculate_cost_filter, write_source_docs_and_ask_control_it_filter, \
    need_prod_accounting_filter, work_on_mp_filter, change_mp_choice_filter, need_prod_accounting_after_mp_filter
from keyboards.bot_keyboards import LEGAL_FORM_KBRD, CANCEL_CALCULATE_KBRD, IND_PRED_TAX_SYSTEM_KBRD, \
    change_patent_numbs_keyboard, IS_RUNNING_BUSINESS, OOO_TAX_SYSTEM_KBRD, change_employees_numb_keyboard, \
    SOURCE_DOCUMENTS_NUMB_KBRD, PRODUCT_ACCOUNTING_KBRD, change_product_docs_keyboard, PRODUCT_REPORTING_KBRD, \
    SHOW_BUH_OPTIONS_KBRD, SRC_DOCS_CONTROL_KBRD, WORK_ON_MP_KBRD, form_choice_mp_kbrd
from secondary_functions.different_functions import make_text_for_buh_result
from secondary_functions.req_to_bot_api import post_for_add_products_in_deal_btrx, get_for_create_docs_in_btrx, \
    post_send_msg_to_open_line
from settings.config import USER_DATA_STORAGE
from loguru import logger


@Client.on_callback_query(cancel_calc_filter)
async def cancel_calc(client, callback_query):
    """Хэндлеры на кнопку отмены в калькуляторе."""

    await callback_query.edit_message_text(
        text=f'<b>📒Вы отменили выбор опций бух.сопровождения</b>.\n\n'
             f'⏳К чему тратить время на сомнения?\n'
             f'🪶<code>"Делегирование полномочий — ключ к успешному управлению..."</code>\n\n'
             f'Доверьте эту работу <b>нашим профессионалам!</b>👩‍💻{emoji.THUMBS_UP}',
        reply_markup=CANCEL_CALCULATE_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Клиент отменил выбор опций бух.сопровождения. Ему предложено всё-таки это сделать.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_callback_query(start_calculate_filter)
async def choice_of_legal_form(client, callback_query):
    """Хэндлер старта калькулятора. Выбор правовой формы ИП или ООО."""

    await callback_query.answer('🤖Выбор правовой формы')
    await callback_query.edit_message_text(
        text=f'📎Пожалуйста, выберете <b>правовую форму</b>.',
        reply_markup=LEGAL_FORM_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Клиент начал выбор опций бух.сопровождения. Запрашиваем у него правовую форму.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_callback_query(ind_pred_tax_system_filter)
async def ind_pred_tax_system(client, callback_query):
    """Выбор системы налогообложения для ИП"""

    await callback_query.answer('🤖Выбор системы налогообложения')
    calc_obj = CalcOptions(tlg_id=callback_query.from_user.id, legal_form='ИП')
    USER_DATA_STORAGE[callback_query.from_user.id]['calculator'] = calc_obj
    await callback_query.edit_message_text(
        text=f'📎Выберете <b>систему налогообложения</b>.',
        reply_markup=IND_PRED_TAX_SYSTEM_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Запрос системы налогообложения',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_callback_query(ask_patent_numbers_filter)
async def ask_patent_numbers(client, callback_query):
    """Запись системы налогооблаж. и запрос количества патентов, в случае, если был микс патент+что-то ещё."""

    await callback_query.answer('🤖Выбор кол-ва патентов')
    calc_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('calculator')
    await calc_obj.set_tax_system(value=callback_query.data.split()[1])  # Запись сис-мы налогооблож.
    calc_obj.patent_numbers = 1
    inline_keyboard = await change_patent_numbs_keyboard(patent_numbs=calc_obj.patent_numbers)
    await callback_query.edit_message_text(
        text=f'📎Укажите <b>количество <u>дополнительных</u> патентов</b>.\n\n'
             f'<i>Текущее количество патентов: {calc_obj.patent_numbers}</i>',
        reply_markup=inline_keyboard
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Клиент выбрал комбинацию патент + иная форма налогооблож. Запрашиваем кол-во патентов.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_callback_query(plus_patent_filter)
async def plus_patent(client, callback_query):
    """Прибавляем один патент к общему количеству пользователя."""

    await callback_query.answer('🤖Плюс 1 патент')
    calc_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('calculator')
    calc_obj.patent_numbers += 1
    inline_keyboard = await change_patent_numbs_keyboard(patent_numbs=calc_obj.patent_numbers)
    await callback_query.edit_message_text(
        text=f'📎Укажите <b>количество <u>дополнительных</u> патентов</b>.\n\n'
             f'<i>Текущее количество патентов: {calc_obj.patent_numbers}</i>',
        reply_markup=inline_keyboard
    )


@Client.on_callback_query(minus_patent_filter)
async def minus_patent(client, callback_query):
    """Отнимаем один патент от общего количества пользователя"""

    await callback_query.answer('🤖Минус 1 патент')
    calc_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('calculator')
    calc_obj.patent_numbers -= 1
    text_for_message = f'📎Укажите <b>количество <u>дополнительных</u> патентов</b>.\n\n' \
                       f'<i>Текущее количество патентов: {calc_obj.patent_numbers}</i>'
    if calc_obj.patent_numbers < 1:
        calc_obj.patent_numbers = 1
        text_for_message = f'📎Укажите <b>количество патентов</b>.\n\n' \
                           f'<i>Текущее количество патентов: {calc_obj.patent_numbers}</i>\n' \
                           f'❗<b>Минимум 1 патент.</b>'
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            msg_text=f'Клиент пытается выбрать меньше 1 дополнительного патента.',
            last_name=callback_query.from_user.last_name,
            name=callback_query.from_user.first_name
        )
    inline_keyboard = await change_patent_numbs_keyboard(patent_numbs=calc_obj.patent_numbers)
    try:
        await callback_query.edit_message_text(
            text=text_for_message,
            reply_markup=inline_keyboard
        )
    except Exception:
        logger.info(f'Кто-то наивно убеждён, что может сделать себе меньше одного патента. '
                    f'\n\tTG ID {callback_query.from_user.id}')


@Client.on_callback_query(ooo_tax_system_filter)
async def ooo_tax_system(client, callback_query):
    """Выбор системы налогообложения для ООО."""

    await callback_query.answer('🤖Выбор системы налогообложения для ООО')
    calc_obj = CalcOptions(tlg_id=callback_query.from_user.id, legal_form='ООО')
    USER_DATA_STORAGE[callback_query.from_user.id]['calculator'] = calc_obj
    text_for_message = '📎Выберете систему налогообложения?'
    await callback_query.edit_message_text(
        text=text_for_message,
        reply_markup=OOO_TAX_SYSTEM_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Предложено выбрать систему налогообложения для ООО',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_callback_query(move_to_business_filter | without_mix_tax_systm_filter)
async def move_to_business(client, callback_query):
    """Запрос осуществления / не осуществления деятельности"""

    await callback_query.answer('🤖Осуществление деятельности бизнесом')
    calc_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('calculator')
    split_call_data = callback_query.data.split()
    if len(split_call_data) == 2 and split_call_data[0] == 'do_bsns':
        await calc_obj.set_tax_system(value=split_call_data[1])  # Запись сис-мы налогооблож.
    text_for_message = '📎Осуществляет ли бизнес деятельность?'
    await callback_query.edit_message_text(
        text=text_for_message,
        reply_markup=IS_RUNNING_BUSINESS
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Спрашиваем осуществляет ли бизнес деятельность.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


''' БИЗНЕС ОСУЩЕСТВЛЯЕТ ВЕДЕНИЕ ДЕЯТЕЛЬНОСТИ (НАЧАЛО) '''


@Client.on_callback_query(choice_employees_number_filter)
async def choice_employees_number(client, callback_query):
    """Выбор количества сотрудников"""

    await callback_query.answer('🤖Выбор количества сотрудников')
    calc_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('calculator')
    # Запись аттрибута осуществления деятельности бизнесом
    calc_obj.do_business = True
    calc_obj.employees_number = 1
    # Для ИП стартовое значение сотрудников изменим на 0
    if calc_obj.legal_form == 'ИП':
        calc_obj.employees_number = 0
    text_for_message = f'📎Укажите количество сотрудников'
    inline_keyboard = await change_employees_numb_keyboard(employees_numb=calc_obj.employees_number)
    await callback_query.edit_message_text(
        text=text_for_message,
        reply_markup=inline_keyboard
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        msg_text=f'Просим выбрать кол-во сотрудников.',
        last_name=callback_query.from_user.last_name,
        name=callback_query.from_user.first_name
    )


@Client.on_callback_query(plus_employee_filter)
async def plus_employee(client, callback_query):
    """Хэндлер для кнопки плюс сотрудник"""

    await callback_query.answer('🤖Плюс сотрудник(и)')
    employee_numb = callback_query.data.split()[1]
    calc_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('calculator')
    calc_obj.employees_number += int(employee_numb)
    text_for_message = f'📎Укажите количество сотрудников\n\n' \
                       f'<i>👥Текущее количество сотрудников <b>{calc_obj.employees_number}</b></i>'
    inline_keyboard = await change_employees_numb_keyboard(employees_numb=calc_obj.employees_number)
    await callback_query.edit_message_text(
        text=text_for_message,
        reply_markup=inline_keyboard
    )


@Client.on_callback_query(minus_employee_filter)
async def minus_employee(client, callback_query):
    """Хэндлер для кнопки минус сотрудник"""

    await callback_query.answer('🤖Минус сотрудник(и)')
    employee_numb = callback_query.data.split()[1]
    calc_obj = USER_DATA_STORAGE[callback_query.from_user.id].get('calculator')
    calc_obj.employees_number -= int(employee_numb)
    text_for_message = f'📎Укажите количество сотрудников\n\n' \
                       f'<i>👥Текущее количество сотрудников <b>{calc_obj.employees_number}</b></i>'
    if calc_obj.employees_number < 1 and calc_obj.legal_form == 'ООО':
        calc_obj.employees_number = 1
        text_for_message = f'📎Укажите количество сотрудников\n\n' \
                           f'❗<b>Минимум 1 сотрудник.</b>\n' \
                           f'<i>👥Текущее количество сотрудников <b>{calc_obj.employees_number}</b></i>'
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            msg_text=f'Клиент пытается выбрать меньше 1 сотрудника. Но для ООО минимум 1.',
            last_name=callback_query.from_user.last_name,
            name=callback_query.from_user.first_name
        )
    elif calc_obj.employees_number < 0 and calc_obj.legal_form == 'ИП':
        calc_obj.employees_number = 0
        text_for_message = f'📎Укажите количество сотрудников\n\n' \
                           f'❗<b>Минимум 0 сотрудников.</b>\n' \
                           f'<i>👥Текущее количество сотрудников <b>{calc_obj.employees_number}</b></i>'
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            msg_text=f'Клиент пытается выбрать меньше 0 сотрудника. Но так не бывает, для ИП минимум 1.',
            last_name=callback_query.from_user.last_name,
            name=callback_query.from_user.first_name
        )
    inline_keyboard = await change_employees_numb_keyboard(employees_numb=calc_obj.employees_number)
    try:
        await callback_query.edit_message_text(
            text=text_for_message,
            reply_markup=inline_keyboard
        )
    except Exception:
        logger.info(f'Кто-то наивно убеждён, что может сделать себе меньше одного сотрудника. '
                    f'\n\tTG ID {callback_query.from_user.id}')


@Client.on_callback_query(source_docs_fst_step_filter)
async def source_docs_fst_step(client, callback):
    """
    Первый шаг из двух в отношении первичных документов. Выбор кол-ва доков для ведения первичного документооборота.
    :param client: объект клиента pyrogram
    :param callback: апдейт в виде колбэка(раньше я писал callback_query. Устал :) так много писать)
    :return: None
    """
    await callback.answer('🤖Выбор кол-ва документов.')
    text_for_message = f'📎<b>Ведение первичного документооборота</b>\n\n' \
                       f'📄Выберете какое количество документов необходимо вести.'
    await callback.edit_message_text(
        text=text_for_message,
        reply_markup=SOURCE_DOCUMENTS_NUMB_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Клиенту предложено выбрать кол-во документов для первичного документооборота.',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )


@Client.on_callback_query(write_source_docs_and_ask_control_it_filter)
async def write_source_docs_and_ask_control_it(client, callback):
    """Запись кол-ва первичных документов и запрос необходимости контроля первичных док."""

    await callback.answer('🤖Необходим ли контроль первичных документов?')
    # Запись кол-ва первичных док-в в класс
    split_callback = callback.data.split()
    calc_obj = USER_DATA_STORAGE[callback.from_user.id].get('calculator')
    if split_callback[1] == '0':
        calc_obj.source_docs_num = '0'
    elif split_callback[1] == '100':
        calc_obj.source_docs_num = 'До 100'
    elif split_callback[1] == '999':
        calc_obj.source_docs_num = 'от 100 до 1000'
    elif split_callback[1] == '1000':
        calc_obj.source_docs_num = 'свыше 1000'
    # Запрос необходимости контроля первичных документов
    text_for_message = f'📎<b>Необходим ли Вам контроль первичных документов?</b>📃\n'
    await callback.edit_message_text(
        text=text_for_message,
        reply_markup=SRC_DOCS_CONTROL_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Спрашиваем необходим ли контроль первичных документов.',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )


@Client.on_callback_query(need_prod_accounting_filter)  # TODO: надо бы переименовать фильтр
async def write_control_src_docs_and_ask_prod_accounting(client, callback):
    """Запись необходимости контроля перв. док-в и запрос необх. ведение тов. учёта."""

    await callback.answer('🤖Работаете ли на маркетплейсах?')
    # Запись необходимости контроля первичных док-в в класс
    split_callback = callback.data.split()
    calc_obj = USER_DATA_STORAGE[callback.from_user.id].get('calculator')
    if split_callback[1] == 'yes':
        calc_obj.need_control_source_docs = 'Да'
    # Спрашиваем работает ли клиент на маркетплейсах
    text_for_message = f'📎<b>Работаете ли Вы на маркетплейсах?🛍</b>\n'
    await callback.edit_message_text(
        text=text_for_message,
        reply_markup=WORK_ON_MP_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Спрашиваем работает ли клиент на маркетплейсах.',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )

    '''клиент работает на маркетплейсах'''


@Client.on_callback_query(work_on_mp_filter)
async def work_on_mp(client, callback):
    """Клиент работает на маркетплейсах"""

    await callback.answer('🤖Выберете маркетплейсы?')
    # Запрос на каких именно МП работает
    text_for_message = f'📎<b>Отметьте маркетплейсы, на которых Вы ведёте бизнес.🛍</b>\n'
    await callback.edit_message_text(
        text=text_for_message,
        reply_markup=await form_choice_mp_kbrd(tlg_id=callback.from_user.id)
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Клиент работает на МП, спрашиваем на каких.',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )


@Client.on_callback_query(change_mp_choice_filter)
async def change_mp_choice(client, callback):
    """Хэндлер для изменения выбора маркетплейсов"""

    await callback.answer('🤖Выбор маркетплейсов')
    # Достаём объект калькулятора для данного пользователя бота
    calc_obj = USER_DATA_STORAGE[callback.from_user.id].get('calculator')
    if callback.data.split()[2] == 'unchoiced':
        # Отмечаем маркетплейс как выбранный
        choice_mp_flag = True
        fst_part_of_text = 'выбран➕'
    else:
        # Отмечаем маркетплейс как невыбранный
        choice_mp_flag = False
        fst_part_of_text = 'снят➖'
    # Выбираем и отмечаем нужный маркетплейс
    if callback.data.split()[1] == 'yandex_market':
        calc_obj.yandex_market = choice_mp_flag
        sec_part_of_text = f'<b>Яндекс Маркет</b>'
    elif callback.data.split()[1] == 'wildber':
        calc_obj.wildber = choice_mp_flag
        sec_part_of_text = f'<b>Wildberries</b>'
    elif callback.data.split()[1] == 'ozon':
        calc_obj.ozon = choice_mp_flag
        sec_part_of_text = f'<b>OZON</b>'
    else:
        calc_obj.other_mp = choice_mp_flag
        sec_part_of_text = f'<b>Другой маркетплейс</b>'
    # Изменяем сообщение и клавиатуру
    text_for_message = f'👌Окей.\n\n🛍{sec_part_of_text} {fst_part_of_text}'
    await callback.edit_message_text(
        text=text_for_message,
        reply_markup=await form_choice_mp_kbrd(tlg_id=callback.from_user.id)
    )


@Client.on_callback_query(need_prod_accounting_after_mp_filter)
async def need_prod_accounting(client, callback):
    """Спрашиваем необходимость товарного учёта"""

    await callback.answer('🤖Необходим ли товарный учёт')
    await callback.edit_message_text(
        text=f'📎Необходим ли Вам <b>товарный учёт</b>?🛒',
        reply_markup=PRODUCT_ACCOUNTING_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Спрашиваем необходим ли клиенту товарный учёт.',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )
    # TODO: проверить это дело
    calc_obj = USER_DATA_STORAGE[callback.from_user.id].get('calculator')
    mp_write_rslt = await calc_obj.send_marketplaces_to_btrx(tlg_id=callback.from_user.id)
    if not mp_write_rslt:
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback.from_user.id,
            username=callback.from_user.username,
            msg_text=f'Не удалось выполнить запрос для записи маркетплейсов в сделку!',
            last_name=callback.from_user.last_name,
            name=callback.from_user.first_name
        )

    '''товарный учёт нужен (начало)'''


@Client.on_callback_query(input_numb_docs_for_prod_acc_filter)
async def input_numb_docs_for_prod_acc(client, callback):
    """Хэндлер для выбора кол-ва док-в для товарного учёта"""

    await callback.answer('🤖Выбор кол-ва док-в для товарного учёта')
    # Запись в класс данных о необходимости товарного учёта
    calc_obj = USER_DATA_STORAGE[callback.from_user.id].get('calculator')
    calc_obj.need_prod_accounting = 'Да'
    # Запрос количества документов для тов. учёта
    calc_obj.prod_accounting_docs_numb = 1
    text_for_message = f'📎Выберете <b>количество документов для товарного учёта</b>'
    inline_keyboard = await change_product_docs_keyboard(prod_docs_numb=calc_obj.prod_accounting_docs_numb)
    await callback.edit_message_text(
        text=text_for_message,
        reply_markup=inline_keyboard
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Предложено выбрать кол-во документов для товарного учёта.',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )


@Client.on_callback_query(minus_prod_doc_filter)
async def minus_prod_doc(client, callback):
    """Хэндлер на кнопку минус документа товарного учёта."""

    await callback.answer('🤖Минус документ товарного учёта')
    prod_docs_numb = int(callback.data.split()[1])
    calc_obj = USER_DATA_STORAGE[callback.from_user.id].get('calculator')
    calc_obj.prod_accounting_docs_numb -= prod_docs_numb
    text_for_message = f'📎Выберете <b>количество документов для товарного учёта</b>\n\n' \
                       f'📄<i>Текущее количество документов: {calc_obj.prod_accounting_docs_numb}</i>'
    if calc_obj.prod_accounting_docs_numb < 1:
        calc_obj.prod_accounting_docs_numb = 1
        text_for_message = f'📎Выберете <b>количество документов для товарного учёта</b>\n\n' \
                           f'❗<b>Минимум 1 документ.</b>\n' \
                           f'📄<i>Текущее количество документов: {calc_obj.prod_accounting_docs_numb}</i>'
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback.from_user.id,
            username=callback.from_user.username,
            msg_text=f'Клиент пытается выбрать меньше одного документа для товарного учёта. Минимум 1 документ.',
            last_name=callback.from_user.last_name,
            name=callback.from_user.first_name
        )
    inline_keyboard = await change_product_docs_keyboard(prod_docs_numb=calc_obj.prod_accounting_docs_numb)
    try:
        await callback.edit_message_text(
            text=text_for_message,
            reply_markup=inline_keyboard
        )
    except Exception:
        logger.info(f'Кто-то наивно убеждён, что может сделать себе меньше одного документа. '
                    f'\n\tTG ID {callback.from_user.id}')


@Client.on_callback_query(plus_prod_doc_filter)
async def plus_prod_doc(client, callback):
    """Хэндлер на кнопку плюс документа товарного учёта."""

    await callback.answer('🤖Плюс документ товарного учёта')
    prod_docs_numb = int(callback.data.split()[1])
    calc_obj = USER_DATA_STORAGE[callback.from_user.id].get('calculator')
    calc_obj.prod_accounting_docs_numb += prod_docs_numb
    text_for_message = f'📎Выберете <b>количество документов для товарного учёта</b>\n\n' \
                       f'📄<i>Текущее количество документов: {calc_obj.prod_accounting_docs_numb}</i>'
    inline_keyboard = await change_product_docs_keyboard(prod_docs_numb=calc_obj.prod_accounting_docs_numb)
    await callback.edit_message_text(
        text=text_for_message,
        reply_markup=inline_keyboard
    )


@Client.on_callback_query(need_product_reporting_filter)
async def need_product_reporting(client, callback):
    """Хэндлер, в котором запрашиваем необходимость учёта и отчётности по товарам, требующим маркировку."""

    await callback.answer('🤖Учёт и отчётность по товарам, треб. маркировку')
    text_for_message = f'📎Необходимо ли <b>ведение учёта и отчётности по товарам, требующим маркировку?</b>🏷️'
    await callback.edit_message_text(
        text=text_for_message,
        reply_markup=PRODUCT_REPORTING_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Запрашиваем необходимость учёта и отчётности по товарам, требующим маркировку.',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )

    '''товарный учёт нужен (конец)'''


''' БИЗНЕС ОСУЩЕСТВЛЯЕТ ВЕДЕНИЕ ДЕЯТЕЛЬНОСТИ (КОНЕЦ) '''


@Client.on_callback_query(show_buh_result_filter)
async def show_buh_result(client, callback):
    """Хэндлер отображения выбранных клиентом опций бух. сопровождения"""

    await callback.answer('🤖Отображаю выбранные опции')
    # Сперва запись по товарам треб. маркировку
    calc_obj = USER_DATA_STORAGE[callback.from_user.id].get('calculator')
    if len(callback.data.split()) == 2 and callback.data.split()[1] == 'need_report':
        calc_obj.prod_requiring_labeling = 'Да'
    # Отображение выбранных опций
    text_for_message = await make_text_for_buh_result(user_id=callback.from_user.id)
    await callback.edit_message_text(
        text=text_for_message,
        reply_markup=SHOW_BUH_OPTIONS_KBRD
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Отображаем выбранные клиентом опции и предлагаем рассчитать стоимость или отменить выбор.',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )


@Client.on_callback_query(calculate_cost_filter)
async def calculate_cost(client, callback):
    """Хэндлер дня кнопки расчёта стоимости опций бух. сопровождения."""

    await callback.answer('🤖Расчёт стоимости опций')
    calc_obj = USER_DATA_STORAGE[callback.from_user.id].get('calculator')
    await callback.edit_message_text(
        text='<b>Ваши данные успешно записаны</b>\n\n'
             f'📑Я пришлю Вам скоро счëт и договор.'
    )
    # Отправка сообщения в чат битрикса
    await post_send_msg_to_open_line(
        tlg_id=callback.from_user.id,
        username=callback.from_user.username,
        msg_text=f'Клиент нажал "Рассчитать стоимость". Уведомляем его о том, что скоро пришлём счёт и договор.',
        last_name=callback.from_user.last_name,
        name=callback.from_user.first_name
    )
    await calc_obj.set_product_id()  # Установка товаров под выбранные клиентом опции бух.сопровожд.
    if calc_obj.product_id.find('over_1000') != -1:     # Если среди продуктов выбрано "свыше 1000 док-в"
        await callback.edit_message_text(
            text='<b>📑Выбрано свыше 1000 документов для учёта</b>\n\n'
                 f'Наш менеджер свяжется с Вами.\n<b>Спасибо за уделённое время.</b>'
        )
        return

    # Добавление товаров в сделку Битрикса
    add_prodcts_rslt = await post_for_add_products_in_deal_btrx(
        products=calc_obj.product_id,
        tlg_id=callback.from_user.id
    )
    if add_prodcts_rslt:  # Если запрос на добавление товаров был успешным
        # Выполняем запрос для генерации документов в Битриксе
        gen_docs_rslt = await get_for_create_docs_in_btrx(tlg_id=callback.from_user.id)
        if not gen_docs_rslt:  # Если запрос для генерации документов вернул False
            await callback.edit_message_text(
                text='🛠У бота что-то неисправно. Мы уже разбираемся. Пожалуйста, повторите позже.'
            )
            # Отправка сообщения в чат битрикса
            await post_send_msg_to_open_line(
                tlg_id=callback.from_user.id,
                username=callback.from_user.username,
                msg_text=f'Не удалось сгенерировать документы! Клиенту было предложено повторить выбор опций позже.',
                last_name=callback.from_user.last_name,
                name=callback.from_user.first_name
            )
    else:  # Если запрос на добавление товаров не был успешным
        await callback.edit_message_text(
            text='🛠У бота что-то неисправно. Мы уже разбираемся. Пожалуйста, повторите позже.'
        )
        # Отправка сообщения в чат битрикса
        await post_send_msg_to_open_line(
            tlg_id=callback.from_user.id,
            username=callback.from_user.username,
            msg_text=f'Не удалось добавить товары в сделку! Клиенту было предложено повторить позже.',
            last_name=callback.from_user.last_name,
            name=callback.from_user.first_name
        )
