import logging
from dadata import Dadata
from settings.config import DADATA_SECRET, DADATA_TOKEN


class DadataHelper:
    dadata_token = DADATA_TOKEN
    dadata_secret = DADATA_SECRET

    @staticmethod
    def find_company_data_by_inn(inn: str):
        with Dadata(DadataHelper.dadata_token, DadataHelper.dadata_secret) as dadata:
            company_data = dadata.find_by_id(name="party", query=inn)
        logging.warning(company_data)
        top_management_post = ''
        top_management_name = ''
        if company_data:
            company_name = company_data[0]['value']
            company_management = company_data[0].get('data').get('management')
            if company_management:
                top_management_name = company_management['name']
                top_management_post = company_management['post']
            company_ogrn = company_data[0]['data']['ogrn']
            company_inn = company_data[0]['data']['inn']
            company_address = company_data[0]['data']['address']['unrestricted_value']
            company_text = f'{company_name}\n' \
                           f'{top_management_post}\n' \
                           f'{top_management_name}\n' \
                           f'ОГРН: {company_ogrn}\n' \
                           f'ИНН: {company_inn}\n' \
                           f'Адрес: {company_address}'

            company = {
                'company_name': company_name,
                'top_management_post': top_management_post,
                'top_management_name': top_management_name,
                'company_ogrn': company_ogrn,
                'company_inn': company_inn,
                'company_address': company_address,
                'company_text': company_text
            }
            return company

    @staticmethod
    def find_bank_data_by_bik(bik: str):
        with Dadata(DadataHelper.dadata_token, DadataHelper.dadata_secret) as dadata:
            bank_data = dadata.find_by_id(name="bank", query=bik)
        if bank_data:
            bank_name = bank_data[0]['value']
            bank_ca = bank_data[0]['data']['correspondent_account']
            bank_text = f'Название банка: {bank_name}\n' \
                        f'БИК: {bik}\n' \
                        f'к/с {bank_ca}\n'

            bank = {
                'bank_name': bank_name,
                'bank_ca': bank_ca,
                'bank_bik': bik,
                'bank_text': bank_text
            }
            return bank

    @staticmethod
    def find_company_data_by_name(name: str):
        """Метод возвращает найденную компанию в виде словаря, либо None."""

        with Dadata(DadataHelper.dadata_token, DadataHelper.dadata_secret) as dadata:
            company_data = dadata.suggest(name="party", query=name)
        logging.warning(company_data)
        top_management_post = ''
        top_management_name = ''
        if company_data:
            company_name = company_data[0]['value']
            company_management = company_data[0].get('data').get('management')
            if company_management:
                top_management_name = company_management['name']
                top_management_post = company_management['post']
            company_ogrn = company_data[0]['data']['ogrn']
            company_inn = company_data[0]['data']['inn']
            company_address = company_data[0]['data']['address']['unrestricted_value']
            company_text = f'{company_name}\n' \
                           f'{top_management_post}\n' \
                           f'{top_management_name}\n' \
                           f'ОГРН: {company_ogrn}\n' \
                           f'ИНН: {company_inn}\n' \
                           f'Адрес: {company_address}'
            company = {
                'company_name': company_name,
                'top_management_post': top_management_post,
                'top_management_name': top_management_name,
                'company_ogrn': company_ogrn,
                'company_inn': company_inn,
                'company_address': company_address,
                'company_text': company_text
            }
            return company
