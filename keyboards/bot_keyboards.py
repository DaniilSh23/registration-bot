from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from keyboards.bot_buttons import BUTTONS_DCT
from settings.config import USER_DATA_STORAGE

START_FIRST_MEETING = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['FIRST_MEETING']
    ]
])

CANCEL_INPUT_COMPANY_DATA = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['CANCEL_COMPANY_INPUT']
    ]
])

CANCEL_INPUT_BANK_DETAIL_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['CANCEL_INPUT_BANK_DETAIL']
    ]
])

AFTER_ADD_COMPANY_DATA_KEYBOARD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['INPUT_BANK_DETAIL'],
        # BUTTONS_DCT['COMPANY_INFO']
    ]
])

INPUT_BANK_DETAIL_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['INPUT_BANK_DETAIL'],
    ],
])

BEFORE_CALCULATE_KEYBOARD = InlineKeyboardMarkup([
    # [
    #     BUTTONS_DCT["BANK_INFO"],
    #     BUTTONS_DCT["COMPANY_INFO"]
    # ],
    [
        BUTTONS_DCT["START_CALCULATE"]
    ]
])

RESTART_BOT_KBRD = InlineKeyboardMarkup([
    # [
    #     BUTTONS_DCT["START_CALCULATE"]
    # ],
    # [
    #     BUTTONS_DCT["BANK_INFO"],
    #     BUTTONS_DCT["COMPANY_INFO"]
    # ],
    [
        BUTTONS_DCT['FIRST_MEETING']
    ]
])

INFO_ABOUT_BANK_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["START_CALCULATE"],
    ],
    [
        BUTTONS_DCT["COMPANY_INFO"]
    ]
])

INFO_ABOUT_COMPANY_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["START_CALCULATE"],
    ],
    [
        BUTTONS_DCT["BANK_INFO"]
    ]
])

# Клавиатуры калькулятора
LEGAL_FORM_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['IND_PRED'],  # ind_pred_form
        BUTTONS_DCT['OOO'],  # ooo_form
    ],
    [
        BUTTONS_DCT['CANCEL_CALCULATE']  # cancel_calc
    ],
])

CANCEL_CALCULATE_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["START_CALCULATE"]
    ],
    # [
    #     BUTTONS_DCT["BANK_INFO"],
    #     BUTTONS_DCT["COMPANY_INFO"]
    # ],
])

IND_PRED_TAX_SYSTEM_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["OSNO"],  # osno_tax_systm
        BUTTONS_DCT["PATENT"],  # patent_tax_systm
        BUTTONS_DCT["USN_DOH"],     # usn_doh_tax_systm
    ],
    [
        BUTTONS_DCT["USN_DOH_RASH"],    # usn_doh_rash_tax_systm
        BUTTONS_DCT["OSNO_PATENT"],     # osno_pat_tax_systm
    ],
    [
        BUTTONS_DCT["USN_DOH_PATENT"],  # usn_doh_pat_tax_systm
    ],
    [
        BUTTONS_DCT["USN_DOH_RASH_PATENT"]  # usn_doh_rash_pat_tax_systm
    ],
    [
        BUTTONS_DCT["CANCEL_CALCULATE"]
    ]
])

OOO_TAX_SYSTEM_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["USN_DOH"],
        BUTTONS_DCT["USN_DOH_RASH"],
    ],
    [
        BUTTONS_DCT["OSNO"],
        BUTTONS_DCT["ESHN"],
    ],
    [
        BUTTONS_DCT["CANCEL_CALCULATE"]
    ]
])

IS_RUNNING_BUSINESS = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["BUSINESS_IS_RUNNING"],
        BUTTONS_DCT["BUSINESS_NOT_RUNNING"],
    ],
    [
        BUTTONS_DCT["CANCEL_CALCULATE"]
    ]
])

SOURCE_DOCUMENTS_NUMB_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["NO_NEED_SRC_DCS"]
    ],
    [
        BUTTONS_DCT["UP_TO_100_DOCS"]
    ],
    [
        BUTTONS_DCT["100_1000_DOCS"]
    ],
    # [
    #     BUTTONS_DCT["OVER_1000_DOCS"]
    # ],
    [
        BUTTONS_DCT["CANCEL_CALCULATE"]
    ]
])

PRODUCT_ACCOUNTING_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["NEED_PRODUCT_ACCOUNTING"],     # need_prod_acc
        BUTTONS_DCT["NOT_NEED_PRODUCT_ACCOUNTING"],     # not_need_prod_acc
    ],
    [
        BUTTONS_DCT["CANCEL_CALCULATE"]
    ]
])

SRC_DOCS_CONTROL_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["NEED_CONTR_SRC_DCS"],     # nd_control_scr_dcs yes
        BUTTONS_DCT["NOT_NEED_CONTR_SRC_DCS"],     # nd_control_scr_dcs no
    ],
    [
        BUTTONS_DCT["CANCEL_CALCULATE"]
    ]
])

PRODUCT_REPORTING_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["NEED_PROD_REPORTING"],     # need_prod_report
        BUTTONS_DCT["NOT_NEED_PROD_REPORTING"],     # not_need_prod_report
    ],
    [
        BUTTONS_DCT["CANCEL_CALCULATE"]
    ]
])

SHOW_BUH_OPTIONS_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["CALCULATE_COST"],
        BUTTONS_DCT["CANCEL_CALCULATE"]
    ]
])

I_PAID_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT["I_PAID"]
    ]
])

RATE_BOT_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['5_STARS']
    ],
    [
        BUTTONS_DCT['4_STARS']
    ],
    [
        BUTTONS_DCT['3_STARS']
    ],
    [
        BUTTONS_DCT['2_STARS']
    ],
    [
        BUTTONS_DCT['1_STARS']
    ],
])

START_PERS_DATA_KBRD = InlineKeyboardMarkup([   # TODO: Скорее всего удалить
    [
        BUTTONS_DCT['START_PERS_DATA']
    ],
    [
        BUTTONS_DCT['PERS_DATA_POLICY']
    ]
])

CNCL_WRT_PERS_DATA_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['CNCL_WRT_PERS_DATA']   # cncl_wrt_pers_data
    ]
])

I_SIGNED_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['I_SIGNED']     # i_signed
    ]
])

NO_RATING_COMMENTS_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['NO_RATING_COMMENTS']   # no_rating_comments
    ]
])


WORK_ON_MP_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['WORK_ON_MP'],  # work_on_mp
        BUTTONS_DCT['NOT_WORK_ON_MP'],  # not_work_on_mp
    ],
])


async def form_choice_mp_kbrd(tlg_id):
    """
    Формирование клавиатуры на шаге выбора маркетплейсов.
    """
    calc_obj = USER_DATA_STORAGE[tlg_id].get('calculator')
    mp_lst = [calc_obj.yandex_market, calc_obj.wildber, calc_obj.ozon, calc_obj.other_mp]   # порядок важен для цикла ниже
    button_lst = []
    buttons_row = []
    for i_elem in range(1, 5):     # Создаём кнопки для каждого МП(ставим отмеченными или нет) по 2 в строку
        if i_elem == 1 and mp_lst[i_elem - 1]:
            buttons_row.append(BUTTONS_DCT['YANDEX_MARKET_CHOICED'])
        elif i_elem == 1 and not mp_lst[i_elem - 1]:
            buttons_row.append(BUTTONS_DCT['YANDEX_MARKET_UNCHOICED'])
        elif i_elem == 2 and mp_lst[i_elem - 1]:
            buttons_row.append(BUTTONS_DCT['WILDBER_CHOICED'])
        elif i_elem == 2 and not mp_lst[i_elem - 1]:
            buttons_row.append(BUTTONS_DCT['WILDBER_UNCHOICED'])
        elif i_elem == 3 and mp_lst[i_elem - 1]:
            buttons_row.append(BUTTONS_DCT['OZON_CHOICED'])
        elif i_elem == 3 and not mp_lst[i_elem - 1]:
            buttons_row.append(BUTTONS_DCT['OZON_UNCHOICED'])
        elif i_elem == 4 and mp_lst[i_elem - 1]:
            buttons_row.append(BUTTONS_DCT['OTHER_MP_CHOICED'])
        else:
            buttons_row.append(BUTTONS_DCT['OTHER_MP_UNCHOICED'])

        if i_elem % 2 == 0:     # Переходим на следующую строку кнопок
            button_lst.append(buttons_row)
            buttons_row = []
    else:   # В конце цикла добавляем две кнопки снизу (след.шаг и отмена)
        button_lst.append([BUTTONS_DCT['MOVE_TO_CHOICE_NEED_PROD_ACC']])
        button_lst.append([BUTTONS_DCT['CANCEL_CALCULATE']])

    return InlineKeyboardMarkup(button_lst)


async def form_webapp_kbrd(form_link):
    """
    Формирование клавиатуры для перехода к форме, которая реализована через веб-приложение.
    :param form_link: ссылка на веб-форму.
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text='🖊Заполнить персональные данные',
                web_app=WebAppInfo(url=form_link)
            )
        ],
        [
            BUTTONS_DCT['PERS_DATA_POLICY']
        ],
    ])


async def confirm_or_reject_company_keyboard(reject_step):
    """
    Формирование клавиатуры для кнопок подтверждения или отклонения данных компании
    """
    if reject_step == 'comp_name':
        reject_button = BUTTONS_DCT['REJECT_COMPANY_BY_NAME']
    elif reject_step == 'inn':
        reject_button = BUTTONS_DCT['REJECT_COMPANY_BY_INN']
    else:
        return
    return InlineKeyboardMarkup([
        [
            BUTTONS_DCT['CONFIRM_COMPANY'],
            reject_button
        ]
    ])


async def confirm_or_reject_bank_keyboard(reject_step='bik'):
    """
    Формирование клавиатуры для кнопок подтверждения или отклонения банковских реквизитов.
    """
    if reject_step == 'bik':
        reject_button = BUTTONS_DCT['REJECT_BANK_BY_BIK']
    else:
        return
    return InlineKeyboardMarkup([
        [
            BUTTONS_DCT['CONFIRM_BANK'],
            reject_button
        ]
    ])


async def change_patent_numbs_keyboard(patent_numbs):
    """
    Формируем клавиатуру для редактирования количества патентов.
    """
    return InlineKeyboardMarkup([
        [
            BUTTONS_DCT["MINUS_PATENT"],
            InlineKeyboardButton(
                text=f'{patent_numbs}',
                callback_data='plug'
            ),
            BUTTONS_DCT["PLUS_PATENT"],
        ],
        [
            BUTTONS_DCT["MOVE_TO_BUSINESS"]
        ],
        [
            BUTTONS_DCT["CANCEL_CALCULATE"]
        ]
    ])


async def change_employees_numb_keyboard(employees_numb):
    """
    Формируем клавиатуру для изменения количества сотрудников.
    """
    return InlineKeyboardMarkup([
        [
            BUTTONS_DCT["MINUS_EMPLOYEE"],
            InlineKeyboardButton(
                text=f'{employees_numb}',
                callback_data='plug'
            ),
            BUTTONS_DCT["PLUS_EMPLOYEE"]
        ],
        [
            BUTTONS_DCT["MINUS_10_EMPLOYEE"],
            BUTTONS_DCT["PLUS_10_EMPLOYEE"],
        ],
        [
            BUTTONS_DCT["MINUS_100_EMPLOYEE"],
            BUTTONS_DCT["PLUS_100_EMPLOYEE"],
        ],
        [
            BUTTONS_DCT["TO_SOURCE_DOCUMENTS"]
        ],
        [
            BUTTONS_DCT["CANCEL_CALCULATE"]
        ]
    ])


async def change_product_docs_keyboard(prod_docs_numb):
    """Клавиатура для изменения количества документов по продуктам"""

    return InlineKeyboardMarkup([
        [
            BUTTONS_DCT["MINUS_PROD_DOC"],
            InlineKeyboardButton(
                text=f'{prod_docs_numb}',
                callback_data='plug'
            ),
            BUTTONS_DCT["PLUS_PROD_DOC"]
        ],
        [
            BUTTONS_DCT["MINUS_10_PROD_DOC"],
            BUTTONS_DCT["PLUS_10_PROD_DOC"],
        ],
        [
            BUTTONS_DCT["MINUS_100_PROD_DOC"],
            BUTTONS_DCT["PLUS_100_PROD_DOC"],
        ],
        [
            BUTTONS_DCT["TO_NEED_PROD_REPORTING"]
        ],
        [
            BUTTONS_DCT["CANCEL_CALCULATE"]
        ]
    ])