from pyrogram import emoji
from pyrogram.types import InlineKeyboardButton, WebAppInfo

from settings.config import PERS_DATA_POLICY_URL

BUTTONS_DCT = {
    'FIRST_MEETING': InlineKeyboardButton(
        text=f'{emoji.PEN}Приступить к заполнению',
        callback_data='start_input'
    ),
    'CANCEL_COMPANY_INPUT': InlineKeyboardButton(
        text=f'{emoji.CROSS_MARK}Отменить ввод данных',
        callback_data='cancel_comp_input'
    ),
    'CONFIRM_COMPANY': InlineKeyboardButton(
        text=f'{emoji.CHECK_MARK_BUTTON}Да, всё верно.',
        callback_data='confirm_comp'
    ),
    'REJECT_COMPANY_BY_NAME': InlineKeyboardButton(
        text=f'{emoji.CROSS_MARK}Это не то.',
        callback_data='reject_comp_by_name'
    ),
    'REJECT_COMPANY_BY_INN': InlineKeyboardButton(
        text=f'{emoji.CROSS_MARK}Это не то.',
        callback_data='reject_comp_by_inn'
    ),
    'COMPANY_INFO': InlineKeyboardButton(
        text=f'🏢Инфо о компании',
        callback_data='info_about_comp'
    ),
    # Раздел про банковские реквизиты
    'INPUT_BANK_DETAIL': InlineKeyboardButton(
        text=f'{emoji.BANK}Внести реквизиты банка',
        callback_data='input_bank_detail'
    ),
    'CANCEL_INPUT_BANK_DETAIL': InlineKeyboardButton(
        text=f'{emoji.CROSS_MARK}Отменить ввод реквизитов',
        callback_data='cancel_inpt_bank'
    ),
    'REJECT_BANK_BY_BIK': InlineKeyboardButton(
        text=f'{emoji.CROSS_MARK}Нет',
        callback_data='reject_bank_by_bik'
    ),
    'CONFIRM_BANK': InlineKeyboardButton(
        text=f'{emoji.CHECK_MARK_BUTTON}Да, всё верно.',
        callback_data='conf_bank'
    ),
    'BANK_INFO': InlineKeyboardButton(
        text=f'{emoji.BANK}Реквизиты банка',
        callback_data='info_about_bank'
    ),
    # Раздел калькулятора
    'START_CALCULATE': InlineKeyboardButton(
        text=f'📒Выбрать опции бух. сопровождения',
        callback_data='start_calc'
    ),
    'CANCEL_CALCULATE': InlineKeyboardButton(
        text=f'{emoji.CROSS_MARK}Отменить выбор опций',
        callback_data='cancel_calc'
    ),
    'IND_PRED': InlineKeyboardButton(
        text=f'🔹ИП',
        callback_data='ind_pred_form'
    ),
    'OOO': InlineKeyboardButton(
        text=f'🔹ООО',
        callback_data='ooo_form'
    ),
    'USN_DOH': InlineKeyboardButton(
        text=f'🔹УСН(дох.)',
        callback_data='do_bsns usn_doh_tax_systm'
    ),
    'USN_DOH_RASH': InlineKeyboardButton(
        text=f'🔹УСН(дох.-расх.)',
        callback_data='do_bsns usn_doh_rash_tax_systm'
    ),
    'OSNO': InlineKeyboardButton(
        text=f'🔹ОСНО',
        callback_data='do_bsns osno_tax_systm'
    ),
    'ESHN': InlineKeyboardButton(
        text=f'🔹ЕСХН',
        callback_data='do_bsns eshn_tax_systm'
    ),
    'PATENT': InlineKeyboardButton(
        text=f'🔹Патент',
        callback_data='do_bsns patent_tax_systm'
    ),
    'USN_DOH_PATENT': InlineKeyboardButton(
        text=f'🔹УСН(дох.)+Патент',
        callback_data='is_pat usn_doh_pat_tax_systm'
    ),
    'USN_DOH_RASH_PATENT': InlineKeyboardButton(
        text=f'🔹УСН(дох.-расх.)+Патент',
        callback_data='is_pat usn_doh_rash_pat_tax_systm'
    ),
    'OSNO_PATENT': InlineKeyboardButton(
        text=f'🔹ОСНО+Патент',
        callback_data='is_pat osno_pat_tax_systm'
    ),
    'PLUS_PATENT': InlineKeyboardButton(
        text=f'➕',
        callback_data='plus_patent'
    ),
    'MINUS_PATENT': InlineKeyboardButton(
        text=f'➖',
        callback_data='minus_patent'
    ),
    'MOVE_TO_BUSINESS': InlineKeyboardButton(
        text=f'➡Следующий шаг',
        callback_data='move_to_bsns'
    ),
    'BUSINESS_IS_RUNNING': InlineKeyboardButton(
        text=f'✔Осуществляет',
        callback_data='bsns_rnng'
    ),
    'BUSINESS_NOT_RUNNING': InlineKeyboardButton(
        text=f'✖Не осуществляет',
        callback_data='show_reslt _'
    ),
    'MINUS_EMPLOYEE': InlineKeyboardButton(
        text=f'➖',
        callback_data='mns_empl 1'
    ),
    'PLUS_EMPLOYEE': InlineKeyboardButton(
        text=f'➕',
        callback_data='pls_empl 1'
    ),
    'MINUS_10_EMPLOYEE': InlineKeyboardButton(
        text=f'➖10',
        callback_data='mns_empl 10'
    ),
    'PLUS_10_EMPLOYEE': InlineKeyboardButton(
        text=f'➕10',
        callback_data='pls_empl 10'
    ),
    'MINUS_100_EMPLOYEE': InlineKeyboardButton(
        text=f'➖100',
        callback_data='mns_empl 100'
    ),
    'PLUS_100_EMPLOYEE': InlineKeyboardButton(
        text=f'➕100',
        callback_data='pls_empl 100'
    ),
    'TO_SOURCE_DOCUMENTS': InlineKeyboardButton(
        text=f'➡Следующий шаг',
        callback_data='to_source_docs'
    ),
    'NO_NEED_SRC_DCS': InlineKeyboardButton(
        text=f'📄✘Не нужно, спасибо.',
        callback_data='source_docs 0'
    ),
    'UP_TO_100_DOCS': InlineKeyboardButton(
        text=f'📄До 100 док-ов',
        callback_data='source_docs 100'
    ),
    '100_1000_DOCS': InlineKeyboardButton(
        text=f'📄От 100 до 1000 док-ов',
        callback_data='source_docs 999'
    ),
    'OVER_1000_DOCS': InlineKeyboardButton(
        text=f'📄Свыше 1000 док-ов',
        callback_data='source_docs 1000'
    ),
    'NEED_PRODUCT_ACCOUNTING': InlineKeyboardButton(
        text=f'✔Нужен тов.учёт',
        callback_data='need_prod_acc'
    ),
    'NOT_NEED_PRODUCT_ACCOUNTING': InlineKeyboardButton(
        text=f'✖Не нужен тов.учёт',
        callback_data='not_need_prod_acc'
    ),
    'MINUS_PROD_DOC': InlineKeyboardButton(
        text=f'➖',
        callback_data='mns_prod_doc 1'
    ),
    'PLUS_PROD_DOC': InlineKeyboardButton(
        text=f'➕',
        callback_data='pls_prod_doc 1'
    ),
    'MINUS_10_PROD_DOC': InlineKeyboardButton(
        text=f'➖10',
        callback_data='mns_prod_doc 10'
    ),
    'PLUS_10_PROD_DOC': InlineKeyboardButton(
        text=f'➕10',
        callback_data='pls_prod_doc 10'
    ),
    'MINUS_100_PROD_DOC': InlineKeyboardButton(
        text=f'➖100',
        callback_data='mns_prod_doc 100'
    ),
    'PLUS_100_PROD_DOC': InlineKeyboardButton(
        text=f'➕100',
        callback_data='pls_prod_doc 100'
    ),
    'TO_NEED_PROD_REPORTING': InlineKeyboardButton(
        text=f'➡Следующий шаг',
        callback_data='to_need_prod_report'
    ),
    'NEED_PROD_REPORTING': InlineKeyboardButton(
        text=f'✔Нужно',
        callback_data='show_reslt need_report'
    ),
    'NOT_NEED_PROD_REPORTING': InlineKeyboardButton(
        text=f'✖Не нужно',
        callback_data='show_reslt not_need_report'
    ),
    'CALCULATE_COST': InlineKeyboardButton(
        text=f'🧮Расчитать стоимость',
        callback_data='calc_cost'
    ),
    'NEED_CONTR_SRC_DCS': InlineKeyboardButton(
        text=f'✔Да',
        callback_data='nd_control_scr_dcs yes'
    ),
    'NOT_NEED_CONTR_SRC_DCS': InlineKeyboardButton(
        text=f'✖Нет, спасибо',
        callback_data='nd_control_scr_dcs no'
    ),
    'I_PAID': InlineKeyboardButton(
        text=f'✅Я оплатил',
        callback_data='i_paid'
    ),
    # Оценка бота
    '5_STARS': InlineKeyboardButton(
        text=f'⭐️⭐️⭐️⭐️⭐️',
        callback_data='rate_bot 5'
    ),
    '4_STARS': InlineKeyboardButton(
        text=f'⭐️⭐️⭐️⭐️',
        callback_data='rate_bot 4'
    ),
    '3_STARS': InlineKeyboardButton(
        text=f'⭐️⭐️⭐️',
        callback_data='rate_bot 3'
    ),
    '2_STARS': InlineKeyboardButton(
        text=f'⭐️⭐️',
        callback_data='rate_bot 2'
    ),
    '1_STARS': InlineKeyboardButton(
        text=f'⭐️',
        callback_data='rate_bot 1'
    ),
    'NO_RATING_COMMENTS': InlineKeyboardButton(
        text=f'🙅‍♂️Без комментариев',
        callback_data='no_rating_comments'
    ),
    # Кнопки для раздела персональных данных
    'START_PERS_DATA': InlineKeyboardButton(    # TODO: Скорее всего удалить
        text=f'🖊Заполнить персональные данные',
        callback_data='start_write_pers_data'
    ),
    'PERS_DATA_POLICY': InlineKeyboardButton(
        text=f'🪪Политика конфиденциальности',
        url=PERS_DATA_POLICY_URL
    ),
    'CNCL_WRT_PERS_DATA': InlineKeyboardButton(     # TODO: Скорее всего удалить
        text=f'❌Отменить ввод персональных данных',
        callback_data=f'cncl_wrt_pers_data'
    ),
    'I_SIGNED': InlineKeyboardButton(
        text=f'✅Я подписал',
        callback_data='i_signed'
    ),
    # Работа на маркетплейсах
    'WORK_ON_MP': InlineKeyboardButton(
        text=f'✔Да',
        callback_data='work_on_mp',
    ),
    'NOT_WORK_ON_MP': InlineKeyboardButton(
        text=f'✖️️Нет',
        callback_data='not_work_on_mp',
    ),
    'YANDEX_MARKET_UNCHOICED': InlineKeyboardButton(
        text='➖ Яндекс Маркет',
        callback_data='marketplace yandex_market unchoiced',
    ),
    'YANDEX_MARKET_CHOICED': InlineKeyboardButton(
        text='➕ Яндекс Маркет',
        callback_data='marketplace yandex_market choiced',
    ),
    'WILDBER_UNCHOICED': InlineKeyboardButton(
        text='➖ Wildberries',
        callback_data='marketplace wildber unchoiced',
    ),
    'WILDBER_CHOICED': InlineKeyboardButton(
        text='➕ Wildberries',
        callback_data='marketplace wildber choiced',
    ),
    'OZON_UNCHOICED': InlineKeyboardButton(
        text='➖ OZON',
        callback_data='marketplace ozon unchoiced',
    ),
    'OZON_CHOICED': InlineKeyboardButton(
        text='➕ OZON',
        callback_data='marketplace ozon choiced',
    ),
    'OTHER_MP_UNCHOICED': InlineKeyboardButton(
        text='➖ Другое',
        callback_data='marketplace other_mp unchoiced',
    ),
    'OTHER_MP_CHOICED': InlineKeyboardButton(
        text='➕ Другое',
        callback_data='marketplace other_mp choiced',
    ),
    'MOVE_TO_CHOICE_NEED_PROD_ACC': InlineKeyboardButton(
        text='➡Следующий шаг',
        callback_data='move_to_choice_need_prod_accounting'
    )
}
