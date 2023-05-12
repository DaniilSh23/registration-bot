from loguru import logger

from secondary_functions.req_to_bot_api import post_for_add_marketplaces_in_deal


class CalcOptions:
    """Пользовательские опции калькулятора"""

    def __init__(self, tlg_id, legal_form, tax_system=None):
        self.tlg_id = tlg_id
        self.legal_form = legal_form
        self.tax_system = tax_system
        self.do_business = False
        self.patent_numbers = None
        self.employees_number = None
        self.source_docs_num = None
        self.need_control_source_docs = None
        self.need_prod_accounting = None
        self.prod_accounting_docs_numb = None
        self.prod_requiring_labeling = None
        self.product_id = None
        # Выбранные маркетплейсы
        self.yandex_market = False
        self.wildber = False
        self.ozon = False
        self.other_mp = False
        self.yandex_market_id = 13268
        self.wildber_id = 13270
        self.ozon_id = 13272
        self.other_mp_id = 13274

    async def set_tax_system(self, value):
        """Установка системы налогообложения"""

        if value == 'osno_tax_systm':
            self.tax_system = 'ОСНО'
        elif value == 'patent_tax_systm':
            self.tax_system = 'Патент'
        elif value == 'usn_doh_tax_systm':
            self.tax_system = 'УСН(доходы)'
        elif value == 'usn_doh_rash_tax_systm':
            self.tax_system = 'УСН(доходы-расходы)'
        elif value == 'osno_pat_tax_systm':
            self.tax_system = 'ОСНО + Патент'
        elif value == 'usn_doh_pat_tax_systm':
            self.tax_system = 'УСН(доходы) + Патент'
        elif value == 'usn_doh_rash_pat_tax_systm':
            self.tax_system = 'УСН(доходы-расходы) + Патент'
        elif value == 'eshn_tax_systm':
            self.tax_system = 'ЕСХН'

    async def set_product_id(self):
        """
        Установка ID продукта.
        Тут ебунячие условия, которые хрен проссышь, поэтому рекомендую не загоняться, а читать комменты.
        """

        # ИП на патенте (без сотрудников и первичного документооборота)
        if self.legal_form == 'ИП' and self.tax_system == 'Патент' and self.do_business:
            self.product_id = '1474:1'
        # ИП или ООО, деятельность не осущ.
        elif not self.do_business:
            self.product_id = '1470:1'
        # ИП или ООО на ОСНО без сотрудн. и перв.документооборота
        elif (self.legal_form == 'ИП' or self.legal_form == 'ООО') and self.tax_system == 'ОСНО':
            # Дальше есть расхождение: для ИП минимум 0 сотрудников, ООО минимум 1
            self.product_id = '1478:1'
        # ИП или ООО на УСН(доходы-расходы) или ЕСХН, без сотрудников и первичного документооборота
        elif (self.legal_form == 'ИП' or self.legal_form == 'ООО') and \
                (self.tax_system == 'УСН(доходы-расходы)' or self.tax_system == 'ЕСХН'):
            self.product_id = '1476:1'
        # ИП или ООО на УСН (доходы) (без сотрудников и первичного документооборота)
        elif (self.legal_form == 'ИП' or self.legal_form == 'ООО') and self.tax_system == 'УСН(доходы)':
            self.product_id = '1472:1'
        # ИП на ОСНО + неск. патентов без сотрудников и перв.документооборота
        elif self.legal_form == 'ИП' and self.tax_system == 'ОСНО + Патент' and self.patent_numbers is not None:
            self.product_id = f'1478:1,34304:{int(self.patent_numbers)}'
        # ИП на УСН(дох) + неск. патентов без сотрудников и перв.документооборота
        elif self.legal_form == 'ИП' and self.tax_system == 'УСН(доходы) + Патент' and self.patent_numbers is not None:
            self.product_id = f'1472:1,34304:{int(self.patent_numbers)}'
        # ИП на УСН(дох-расх.) + неск. патентов без сотрудников и перв.документооборота
        elif self.legal_form == 'ИП' and self.tax_system == 'УСН(доходы-расходы) + Патент' and self.patent_numbers is not None:
            self.product_id = f'1476:1,34304:{int(self.patent_numbers)}'

        # Дальше накидываем допы
        # Кадровый учёт сотрудников (если ИП, то их должно быть >0, а если ООО, то >1)
        if self.do_business and self.legal_form == 'ИП' and self.employees_number is not None and self.employees_number > 0:
            self.product_id = ','.join([self.product_id, f'1498:{self.employees_number}'])
        elif self.do_business and self.legal_form == 'ООО' and self.employees_number is not None and self.employees_number > 1:
            self.product_id = ','.join([self.product_id, f'1498:{self.employees_number - 1}'])

        # Ведение первичного документооборота до 100 док-в в месяц
        if self.source_docs_num == 'До 100':
            self.product_id = ','.join([self.product_id, f'1482:1'])
        elif self.source_docs_num == 'от 100 до 1000':
            self.product_id = ','.join([self.product_id, f'34280:1'])
        elif self.source_docs_num == 'свыше 1000':
            # over_1000 - моё условное обозначение для доков >1000
            self.product_id = ','.join([self.product_id, f'over_1000:1'])

        # Контроль первичных документов
        if self.need_control_source_docs == 'Да':
            self.product_id = ','.join([self.product_id, f'1486:1'])

        # Товарный учёт (до 100 документов, а также свыше 100 тоже будет добавляться, так как свыше 100 цена идёт допом)
        if self.need_prod_accounting == 'Да':
            self.product_id = ','.join([self.product_id, f'34284:1'])

        # Товарный учёт за каждые 100 документов, свыше 100
        if self.prod_accounting_docs_numb is not None and self.prod_accounting_docs_numb > 100:
            from math import ceil as m_ceil_round
            numb = m_ceil_round(self.prod_accounting_docs_numb / 100 - 1)
            self.product_id = ','.join([self.product_id, f'34288:{numb}'])

        # Ведение учёта и отчётности по товарам, требующим маркировку
        if self.prod_requiring_labeling == 'Да':
            self.product_id = ','.join([self.product_id, f'34296:1'])

        # Устанавливаем обязательный товар - подключение к эл. отчётности
        self.product_id = ','.join([self.product_id, f'1500:1'])

    async def send_marketplaces_to_btrx(self, tlg_id):
        """Метод для отправки ID маркетплейсов в сделку Bitrix"""

        mp_dct = {
            self.yandex_market_id: self.yandex_market,
            self.wildber_id: self.wildber,
            self.ozon_id: self.ozon,
            self.other_mp_id: self.other_mp,
        }
        rslt_for_send = []
        for i_mp_key, i_mp_value in mp_dct.items():
            if i_mp_value:
                rslt_for_send.append(str(i_mp_key))
        if len(rslt_for_send) == 0:
            logger.info('Маркетплейсы для записи в сделку не выбраны.')
            return None
        return await post_for_add_marketplaces_in_deal(tlg_id=tlg_id, marketplaces_id=' '.join(rslt_for_send))
