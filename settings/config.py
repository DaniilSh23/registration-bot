import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN', '5265303938:AAE1daGp-VJR0R15J9tHksR38hQlbCXMYdU')
API_ID = os.environ.get('API_ID', '1234567890')
API_HASH = os.environ.get('API_HASH', 'какой-то там хэш')
DADATA_TOKEN = os.environ.get('DADATA_TOKEN', 'токен DaData')
DADATA_SECRET = os.environ.get('DADATA_SECRET', 'секретный ключ DaData')
BOT_ID = os.environ.get('BOT_ID', 5265303938)
PERS_DATA_POLICY_URL = os.environ.get('PERS_DATA_POLICY_URL', 'https://cfunalog.ru/')
ABOUT_MCHD_URL = os.environ.get('ABOUT_MCHD_URL', 'https://ca.kontur.ru/articles/25216-mashinochitaemaya_doverennost')

# Константы для API Django проекта
BASE_HOST_URL = os.environ.get('BASE_HOST_URL', 'http://127.0.0.1:8000/')
USER_DATA_URL = f'{BASE_HOST_URL}reg_bot/bot_users/'
COMPANY_DATA_URL = f'{BASE_HOST_URL}reg_bot/company/'
BANK_DATA_URL = f'{BASE_HOST_URL}reg_bot/bank/'
OPEN_LINE_URL = f'{BASE_HOST_URL}reg_bot/open_line/'
DEAL_UPDATE_URL = f'{BASE_HOST_URL}reg_bot/deal_update/'
DOCS_GEN_URL = f'{BASE_HOST_URL}reg_bot/docs_gen/'
PERS_DATA_URL = f'{BASE_HOST_URL}reg_bot/prs_dt/'
RATING_URL = f'{BASE_HOST_URL}reg_bot/rating/'
LAWYER_TASK_URL = f'{BASE_HOST_URL}reg_bot/law_task/'
REMIND_URL = f'{BASE_HOST_URL}reg_bot/remind/'
MARKETPLACES_URL = f'{BASE_HOST_URL}reg_bot/marketplaces/'

# Словари-временные хранилища разных данных
USER_DATA_STORAGE = dict()
CALCULATOR_DATA_STORAGE = dict()
TEMPORARY_STORAGE = dict()  # Нужно чисто для одного шага в хэндлерах, чтобы не упускать данные