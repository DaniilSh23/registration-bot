import re

from secondary_functions.req_to_bot_api import post_user_data, post_company_data, post_bank_data, \
    post_for_write_pers_data


class User:
    """Класс пользователя бота"""

    def __init__(self, tlg_id, deal_id, tlg_username, is_staff=False,
                 telephone=None, email=None, state_name=None, passport_data=None, snils=None,
                 passport_issued_by=None,
                 ):
        """
        Конструктор класса пользователя бота
        :param tlg_id: int - Telegram ID пользователя
        :param deal_id: int - ID сделки, с которым пользователь запустил бота
        :param tlg_username: str - Telegram username пользователя бота
        :param is_staff: bool - Флаг, является ли пользователь персоналом(на перспективу)
        :param telephone: str - Контактный номер телефона клиента
        :param email: str - Контактный email клиента
        """
        self.tlg_id = tlg_id
        self.deal_id = deal_id
        self.tlg_username = tlg_username
        self.is_staff = is_staff
        self.telephone = telephone
        self.email = email
        self.state_name = state_name

    async def get_telephone(self):
        """Геттер для аттрибута telephone"""
        return self.telephone

    async def set_telephone(self, telephone):
        """
        Сеттер для аттрибута telephone.
        Проверяет на соответствие регулярке и возвращает True/False.
        :param telephone: str - Номер телефона
        :return: bool
        """

        reg = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
        if re.match(reg, telephone):
            self.telephone = telephone
            return True
        else:
            return False

    async def get_email(self):
        """Геттер для email"""
        return self.email

    async def set_email(self, email):
        """
        Сеттер для email. Проверяет на соответствие регулярке и возвращает True/False
        :param email:
        :return: bool
        """
        reg = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if re.match(reg, email):
            self.email = email
            return True
        else:
            return False

    async def write_user_in_db(self):
        """Метод для записи информации о пользователе в БД"""
        fields_for_req = {
            'tlg_id': self.tlg_id,
            'tlg_username': self.tlg_username,
            'telephone': self.telephone,
            'email': self.email,
            'deal_id': self.deal_id,
            'is_staff': self.is_staff,
        }
        user_data = dict()
        for i_key, i_value in fields_for_req.items():
            if i_value:
                user_data[i_key] = i_value
        result = await post_user_data(user_data)
        return result


class Company:
    """Класс для работы с данными компании"""

    def __init__(self, user_tlg_id, comp_name=None, address=None, ogrn=None,
                 inn=None, top_management_post=None, top_management_name=None, state_name=None):
        """
        Конструктор для класса работы с данными о компании клиента.
        :param user_tlg_id: int - Telegram ID пользователя бота(клиента)
        :param comp_name: str - Название компании
        :param address: str - Адрес компании
        :param ogrn: str - ОГРН компании (13 цифр)
        :param inn: str - ИНН компании (12 цифр)
        :param top_management_post: str - Должность лица, управляющего компанией
        :param top_management_name: str - ФИО лица, управляющего компанией
        """

        self.user_tlg_id = user_tlg_id
        self.comp_name = comp_name
        self.address = address
        self.ogrn = ogrn
        self.inn = inn
        self.top_management_post = top_management_post
        self.top_management_name = top_management_name
        self.state_name = state_name

    async def get_inn(self):
        """Геттер для ИНН"""
        return self.inn

    async def set_inn(self, inn):
        """
        Сеттер для ИНН.Проверяет по регулярке наличие
        :param inn: str - ИНН
        :return: bool
        """
        reg = r'^\d{10,12}$'
        if re.match(reg, inn):
            self.inn = inn
            return True
        else:
            return False

    async def get_ogrn(self):
        """Геттер для ОГРН"""
        return self.ogrn

    async def set_ogrn(self, ogrn):
        """
        Сеттер для ОГРН. Проверяет по регулярке наличие 13 цифр.
        :param ogrn: str - ОГРН
        :return: bool
        """
        reg = r'^\d{13}$'
        if re.match(reg, ogrn):
            self.ogrn = ogrn
            return True
        else:
            return False

    async def write_company_data(self):
        """Метод для записи информации о компании в БД"""

        # {"comp_name": "ИП Шестаков Ярослав Викторович", "address": "299700, г Севастополь", "ogrn": "321920000008415",
        #  "inn": "920151840873", "top_management_post":"", "top_management_name":"", "user": 1978587604}
        company_data = {
            'comp_name': self.comp_name,
            'address': self.address,
            'ogrn': self.ogrn,
            'inn': self.inn,
            'top_management_post': self.top_management_post,
            'top_management_name': self.top_management_name,
            'user': self.user_tlg_id,
        }
        return await post_company_data(company_data)


class BankDetail:
    """Класс для работы с банковскими реквизитами компании"""

    def __init__(self, inn_comp, bik=None, rs=None, cor_a=None, bank_name=None):
        """
        Конструктор класса для работы с банковскими реквизитами компании
        :param inn_comp: int - ИНН компании (10-12 цифр)
        :param bik: int - БИК (9 цифр)
        :param rs: int - Расчётный счёт (20 цифр)
        :param cor_a: int - Корреспондентский счёт (20 цифр)
        :param bank_name: str - Название банка
        """

        self.inn_comp = inn_comp
        self.bik = bik
        self.rs = rs
        self.cor_a = cor_a
        self.bank_name = bank_name
        self.state_name = None

    async def get_bik(self):
        """Геттер для БИК"""
        return self.bik

    async def set_bik(self, bik):
        """
        Сеттер для БИК. Проверяет регуляркой наличие 9 цифр в строке
        :param bik: str - БИК
        :return: bool
        """
        reg = r'^\d{9}$'
        if re.match(reg, bik):
            self.bik = bik
            return True
        else:
            return False

    async def get_rs(self):
        """Геттер для расчётного счёта."""
        return self.rs

    async def set_rs(self, rs):
        """
        Сеттер для расчётного счёта. Проверяет регуляркой наличие 20 цифр в строке.
        :param rs: str - расчётный счёт
        :return: bool
        """
        reg = r'^\d{20}$'
        if re.match(reg, rs):
            self.rs = rs
            return True
        else:
            return False

    async def get_cor_a(self):
        """Геттер для корреспондентского счёта"""
        return self.cor_a

    async def set_cor_a(self, cor_a):
        """
        Сеттер для корреспондентского счёта. Проверяет регуляркой наличие 20 цифр в строке.
        :param cor_a: str - Корреспондентский счёт
        :return: bool
        """
        reg = r'^\d{20}$'
        if re.match(reg, cor_a):
            self.cor_a = cor_a
            return True
        else:
            return False

    async def write_company_bank_details(self):
        """Метод для записи банковских реквизитов компании в БД"""

        bank_data = {
            'inn_comp': self.inn_comp,
            'bik': self.bik,
            'rs': self.rs,
            'cor_a': self.cor_a,
            'bank_name': self.bank_name,
        }
        return await post_bank_data(bank_data)
