import aiohttp as aiohttp
from loguru import logger
from settings.config import USER_DATA_URL, COMPANY_DATA_URL, BANK_DATA_URL, OPEN_LINE_URL, DEAL_UPDATE_URL, \
    DOCS_GEN_URL, PERS_DATA_URL, RATING_URL, LAWYER_TASK_URL, REMIND_URL, MARKETPLACES_URL


async def get_user_data(tlg_id):
    """
    GET запрос для получения данных о пользователе бота.
    :param tlg_id: int - TG ID пользователя
    :return: dict | bool
    """
    url_ads = ''.join([USER_DATA_URL, f'?tlg_id={tlg_id}'])
    async with aiohttp.ClientSession() as session:
        async with session.get(url_ads) as response:
            if response.status == 200:
                logger.success(f'Успешный GET-запрос для получения инфо о пользователе бота')
                return await response.json()
            else:
                logger.warning(f'GET-запрос для получения инфо о пользователе бота НЕ УДАЛСЯ')
                return False


async def post_user_data(user_data):
    """
    POST запрос для создания или обновления записи о пользователе в БД.
    :return: bool
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=USER_DATA_URL, data=user_data) as response:
            if response.status == 200:
                logger.success(f'Успешный POST-запрос для создания/обновления записи о пользователе бота')
                return True
            else:
                logger.warning(f'POST-запрос для создания/обновления записи о пользователе бота НЕ УДАЛСЯ')
                return False


async def get_company_data(tlg_id):
    """
    GET запрос для получение компании по TG ID пользователя
        ?tlg_id=.. - получение компании клиента по TG ID
    :return: dict | bool
    """
    req_url = f'{COMPANY_DATA_URL}?tlg_id={tlg_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=req_url) as response:
            if response.status == 200:
                logger.success(f'Успешный GET-запрос для получения записи о компании')
                return await response.json()
            else:
                logger.warning(f'GET-запрос для получения записи о компании НЕ УДАЛСЯ')
                return False


async def post_company_data(company_data):
    """
    POST запрос для создания или обновления записи о компании в БД.
    :return: bool
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=COMPANY_DATA_URL, data=company_data) as response:
            if response.status == 200:
                logger.success(f'Успешный POST-запрос для создания/обновления записи о компании')
                return True
            else:
                logger.warning(f'POST-запрос для создания/обновления записи о компании НЕ УДАЛСЯ')
                return False


async def get_bank_data(inn):
    """
    GET запрос для получения банковских данных по РС клиента
        ?inn - получение одной записи по ИНН компании
    :return: dict | bool
    """
    req_url = f'{BANK_DATA_URL}?inn={inn}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=req_url) as response:
            if response.status == 200:
                logger.success(f'Успешный GET-запрос для получения данных о банке')
                return await response.json()
            else:
                logger.warning(f'GET-запрос для получения данных о банке НЕ УДАЛСЯ')
                return False


async def post_bank_data(bank_data):
    """
    POST запрос для создания или обновления записей о реквизитах банка в БД.
    :return: bool
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url=BANK_DATA_URL, data=bank_data) as response:
            if response.status == 200:
                logger.success(f'Успешный POST-запрос для создания/обновления записи о банке компании')
                return True
            else:
                logger.warning(f'POST-запрос для создания/обновления записи о банке компании НЕ УДАЛСЯ')
                return False


async def get_open_line_create(tlg_id):
    """
    GET запрос для создания чата, где будет "логирование" действий клиента с ботом.
    Параметры запроса:
        ?tlg_id - TG ID пользователя
    :return: bool
    """
    req_url = f'{OPEN_LINE_URL}?tlg_id={tlg_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=req_url) as response:
            if response.status == 200:
                logger.success(f'Успешный GET-запрос для создания чата в Битриксе.')
                return True
            else:
                logger.warning(f'GET-запрос для создания чата в Битриксе НЕ УДАЛСЯ!')
                return False


async def post_send_msg_to_open_line(tlg_id, username, msg_text, last_name=None, name=None):
    """
    POST запрос для пересылки сообщения в открытую линию
    Параметры запроса:
        tlg_id - (int, max_value=9999999999) TG ID пользователя
        username - (str, max_length=400) TG username пользователя (опционально)
        last_name - (str, max_length=400) TG last_name пользователя (опционально)
        name - (str, max_length=400) TG first_name пользователя (опционально)
        msg_text - (str, max_length=5000) текст сообщения пользователя в чате с ботом
    :return: bool
    """
    req_data = {
        'tlg_id': tlg_id,
        'username': username,
        'msg_text': msg_text,
        'last_name': last_name,
        'name': name,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=OPEN_LINE_URL, data=req_data) as response:
            if response.status == 200:
                logger.success(f'Успешный POST-запрос для пересылки сообщения (user_tlg_id=={tlg_id}) в открытую линию.')
                return True
            else:
                logger.warning(f'POST-запрос для пересылки сообщения (user_tlg_id=={tlg_id}) в открытую линию НЕ УДАЛСЯ!')
                return False


async def get_for_crt_comp_and_bank_dtail_in_btrx(tlg_id):
    """
    GET запрос для создания в Битриксе компании и банковских реквизитов, затем привязка всего этого к сделке.
    :param tlg_id: int - TG ID пользователя.
    :return: bool
    """
    req_url = f'{DEAL_UPDATE_URL}?tlg_id={tlg_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=req_url) as response:
            if response.status == 200:
                logger.success(f'Успешный GET-запрос для создания в Битре компании и реквизитов(user_tlg_id=={tlg_id})')
                return True
            else:
                logger.warning( f'GET-запрос для создания в Битре компании и реквизитов НЕ УДАЛСЯ!(user_tlg_id=={tlg_id})')
                return False


async def post_for_add_products_in_deal_btrx(products, tlg_id):
    """
    POST запрос для добавления товаров в сделку в Битриксе.
    Параметры запроса:
            products - str, <fst_prod_id:numb,sec_prod_id:numb,...> ID товаров и их количество в виде строки
            tlg_id - int, TG ID пользователя
    :return: bool
    """
    req_data = {
        'products': products,
        'tlg_id': tlg_id,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=DEAL_UPDATE_URL, data=req_data) as response:
            if response.status == 200:
                logger.success(f'Успешный POST-запрос для добавления товаров в сделку!(user_tlg_id=={tlg_id})')
                return True
            else:
                logger.warning(f'POST-запрос для добавления товара в сделку НЕ УДАЛСЯ!(user_tlg_id=={tlg_id})')
                return False


async def get_for_create_docs_in_btrx(tlg_id):
    """
    GET запрос для создания документов (счёт и договор) в Битриксе.
    :param tlg_id: - int, TG ID пользователя
    :return: bool
    """
    req_url = f'{DOCS_GEN_URL}?tlg_id={tlg_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=req_url) as response:
            if response.status == 200:
                logger.success(f'Успешный GET-запрос для генерации док-в(счёт, договор)!(user_tlg_id=={tlg_id})')
                return True
            else:
                logger.warning(f'GET-запрос для для генерации док-в(счёт, договор) НЕ УДАЛСЯ!(user_tlg_id=={tlg_id})')
                return False


async def get_form_link_for_pers_data(tlg_id):
    """
    GET запрос для получения из Битрикса ссылки на форму сбора персональных данных.
    :param tlg_id: int - TG ID пользователя
    :return: dict - ссылка на форму сбора персональных данных {'form_link':<ссылка>}
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{PERS_DATA_URL}?tlg_id={tlg_id}') as response:
            if response.status == 200:
                logger.success('Успешный запрос для получения ссылки на форму сбора персональных данных.')
                return await response.json()
            else:
                logger.warning('НЕ УДАЛСЯ запрос для получения ссылки на форму сбора перс.данных!')
                return False


async def post_for_write_pers_data(tlg_id, snls, pssprt):
    """
    POST запрос для записи перс.данных в Битрикс и сохранения даты и времени согласия на их обработку.
    :param tlg_id: int - TG ID пользователя
    :param snls: int - СНИЛС
    :param pssprt: str - серия и номер паспорта
    :return: bool
    """
    req_data = {
        'tlg_id': tlg_id,
        'snls': snls,
        'pssprt': ''.join(pssprt.split()),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=PERS_DATA_URL, data=req_data) as response:
            if response.status == 200:
                logger.success(f'Успешный POST-запрос для записи перс.данных(user_tlg_id=={tlg_id})')
                return True
            else:
                logger.warning(f'POST-запрос для записи перс.данных НЕ УДАЛСЯ!(user_tlg_id=={tlg_id})\n'
                               f'Ответ сервера:{await response.text()}')
                return False


async def post_for_add_bot_rating(tlg_id, rating=None, comment=None):
    """
    POST запрос для записи оценки бота в админку.
    :param tlg_id: int - TG ID пользователя
    :param rating: str - оценка бота(число в виде строки с длиной == 1)
    :param comment: str - комментарий к оценке(строка с макс. длиной 4096)
    :return: bool
    """
    req_data = {
        "tlg_id": tlg_id,
    }
    if rating:
        req_data['rating'] = rating
    elif comment:
        req_data['comment'] = comment
    async with aiohttp.ClientSession() as session:
        async with session.post(url=RATING_URL, data=req_data) as response:
            if response.status == 200:
                logger.success('Запрос для записи оценки бота выполнен успешно!')
                return True
            else:
                logger.warning('Запрос для записи оценки бота НЕ УДАЛСЯ!')
                return False


async def get_for_add_task_to_lawyer(tlg_id, task_type):
    """
    GET запрос для создания в Битриксе задачи для юриста.
    :param tlg_id: int - TG ID пользователя
    :param task_type: int - Tип задачи
    :return: bool
    """
    req_link = f'{LAWYER_TASK_URL}?tlg_id={tlg_id}&task_type={task_type}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=req_link) as response:
            if response.status == 200:
                logger.success(f'Запрос для добавления задачи юристу выполнен!(ТИП ЗАДАЧИ == {task_type})')
                return True
            else:
                logger.warning(f'Запрос для добавления задачи юристу НЕ УДАЛСЯ!(ТИП ЗАДАЧИ == {task_type})')
                return False


async def get_for_manage_reminds(tlg_id, reminder_type, act):
    """
    GET запрос для управления напоминаниями
    :param tlg_id: int - TG ID пользователя
    :param reminder_type: str - Тип напоминания(p, s - оплата и подпись соответственно)
    :param act: str - Действие (add, del)
    :return: bool
    """
    req_link = f'{REMIND_URL}?tlg_id={tlg_id}&reminder_type={reminder_type}&act={act}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=req_link) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для управления напоминаниями. Действие == {act}')
                return True
            else:
                logger.warning(f'Неудачный запрос для управления напоминаниями. Действие == {act}, TG ID == {tlg_id}')
                return False


async def post_for_add_marketplaces_in_deal(tlg_id, marketplaces_id):
    """
    POST запрос для добавления маркетплейсов в сделку
    :param tlg_id: int - TG ID пользователя
    :param marketplaces_id: str - ID маркетплейсов из системы Битрикс, указанные в виде строки через пробел
    :return: bool
    """
    req_data = {'tlg_id': tlg_id, 'marketplaces': marketplaces_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=MARKETPLACES_URL, data=req_data) as response:
            if response.status == 200:
                logger.success(f'Успешный запрос для добавления маркетплейсов в сделку. USR_TG_ID == {tlg_id}')
                return True
            else:
                logger.warning(f'Неудачный запрос для добавления маркетплейсов в сделку. USR_TG_ID == {tlg_id}')
                return False
