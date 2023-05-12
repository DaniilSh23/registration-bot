from bot_objects.user_data_objects import User, Company, BankDetail
from secondary_functions.req_to_bot_api import get_user_data, get_company_data, get_bank_data
from settings.config import USER_DATA_STORAGE


async def get_instance_from_storage_or_req(user_id):
    """
    Функция, которая берёт инстанс User в словаре-хранилище или достаёт данные из БД и создаёт инстанс.
    """
    user_data = USER_DATA_STORAGE.get(user_id)
    if user_data:
        user_obj = user_data.get('user')
        if user_obj:
            return user_obj
    # Достаём инфу из БД
    response = await get_user_data(tlg_id=user_id)
    if response:
        # Создаём объект класса
        user_obj = User(
            tlg_id=user_id,
            deal_id=response.get('deal_id'),
            tlg_username=response.get('tlg_username'),
            is_staff=response.get('is_staff'),
            telephone=response.get('telephone'),
            email=response.get('email'),
        )
        # И возвращаем этот объект класса из функции
        return user_obj
    else:
        return False


async def get_company_data_from_storage_or_req(user_id):
    """
    Функция, которая достаёт данные компании из лок.хранилища(словаря) или из БД.
    """
    user_data = USER_DATA_STORAGE.get(user_id)
    if user_data:
        comp_obj = user_data.get('company')
        if comp_obj:
            return comp_obj
    # Достаём инфу из БД
    response = await get_company_data(tlg_id=user_id)
    if response:
        # Создаём объект класса
        comp_obj = Company(
            user_tlg_id=user_id,
            comp_name=response.get('comp_name'),
            address=response.get('address'),
            ogrn=response.get('ogrn'),
            inn=response.get('inn'),
            top_management_post=response.get('top_management_post'),
            top_management_name=response.get('top_management_name'),
        )
        # И возвращаем этот объект класса из функции
        return comp_obj
    else:
        return False


async def get_bank_data_from_storage_or_req(user_id):
    """
    Функция, которая достаёт реквизиты банка из локального хранилища или из БД.
    """
    # get_bank_data
    user_data = USER_DATA_STORAGE.get(user_id)
    if user_data:
        bank_obj = user_data.get('bank')
        if bank_obj:
            return bank_obj
    # Достаём инфу из БД
    company_obj = await get_company_data_from_storage_or_req(user_id)   # Сперва подтягиваем компанию через функцию
    response = await get_bank_data(inn=company_obj.inn)
    if response:
        # Создаём объект класса
        bank_obj = BankDetail(
            inn_comp=company_obj.inn,
            bik=response.get('bik'),
            rs=response.get('rs'),
            cor_a=response.get('cor_a'),
            bank_name=response.get('bank_name'),
        )
        # И возвращаем этот объект класса из функции
        return bank_obj
    else:
        return False


async def make_text_for_buh_result(user_id):
    """Создаём текст сообщения для отображения выбранных опций бух. сопровождения."""

    calc_obj = USER_DATA_STORAGE[user_id].get('calculator')
    positions_lst = [
        '▫️Правовая форма:',
        '▫️Система налогообложения:',
        '▫️Количество патентов:',
        '▫️Количество сотрудников:',
        '▫️Кол-во документов для ведения первичного документооборота:',
        '▫️Необходим контроль первичных документов:',
        '▫️Товарный учёт:',
        '▫️Кол-во документов товарного учёта:',
        '▫️Ведение учёта и отчётности по товарам, требующим маркировку:'
    ]
    selected_options_lst = [
        calc_obj.legal_form,
        calc_obj.tax_system,
        calc_obj.patent_numbers,
        calc_obj.employees_number,
        calc_obj.source_docs_num,
        calc_obj.need_control_source_docs,
        calc_obj.need_prod_accounting,
        calc_obj.prod_accounting_docs_numb,
        calc_obj.prod_requiring_labeling,
    ]
    text_for_message = '📒<b>Выбранные опции бухгалтерского сопровождения:</b>\n\n'
    for i_indx in range(9):
        if selected_options_lst[i_indx] or selected_options_lst[i_indx] == 0:
            text_for_message = ''.join([
                text_for_message,
                f'<b>{positions_lst[i_indx]}</b>',
                f' {selected_options_lst[i_indx]}\n'
            ])
    return text_for_message
