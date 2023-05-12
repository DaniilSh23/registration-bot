from pyrogram import filters

from settings.config import USER_DATA_STORAGE


async def func_input_company_name_filter(_, __, query):
    """Фильтр для хэндлера запроса названия компании"""
    return query.data == 'start_input'


async def func_cancel_company_input_filter(_, __, query):
    """Фильтр для хэндлера отмена ввода данных компании"""
    return query.data == 'cancel_comp_input'


async def func_write_comp_name_filter(_, __, query):
    """Фильтр для хэндлера записи названия компании"""
    company_obj = USER_DATA_STORAGE[query.from_user.id].get('company')
    if company_obj:
        return company_obj.state_name == 'input_company_name'


async def func_confirm_comp_data_filter(_, __, query):
    """Фильтр для хэндлера подтверждения пользователем данных компании"""
    return query.data == 'confirm_comp'


async def func_reject_comp_by_name_filter(_, __, query):
    """Фильтр для хэндлера отклонения данных компании (после запроса по названию)"""
    return query.data == 'reject_comp_by_name'


async def func_write_inn_filter(_, __, query):
    """Фильтр для хэндлера записи ИНН"""
    company_obj = USER_DATA_STORAGE[query.from_user.id].get('company')
    if company_obj:
        return company_obj.state_name == 'input_inn'


async def func_reject_comp_data_by_inn_filter(_, __, query):
    """Фильтр для хэндлера отклонения данных компании (после запроса по ИНН)"""
    return query.data == 'reject_comp_by_inn'


async def func_write_ogrn_filter(_, __, query):
    """Фильтр для хэндлера записи ОГРН"""
    company_obj = USER_DATA_STORAGE[query.from_user.id].get('company')
    if company_obj:
        return company_obj.state_name == 'input_ogrn'


async def func_write_telephone_filter(_, __, query):
    """Фильтр для хэндлера записи контактного телефона"""
    company_obj = USER_DATA_STORAGE[query.from_user.id].get('company')
    if company_obj:
        return company_obj.state_name == 'input_telephone'


async def func_write_email_filter(_, __, query):
    """Фильтр для хэндлера записи контакного мыла."""
    user_obj = USER_DATA_STORAGE[query.from_user.id].get('user')
    return user_obj.state_name == 'input_email'


async def func_write_address_filter(_, __, query):
    """Фильтр для хэндлера записи адреса компании"""
    user_obj = USER_DATA_STORAGE[query.from_user.id].get('user')
    return user_obj.state_name == 'input_address'


async def func_write_top_management_post_filter(_, __, query):
    """Фильтр для хэндлера записи должности главного управленца в компании."""
    company_obj = USER_DATA_STORAGE[query.from_user.id].get('company')
    if company_obj:
        return company_obj.state_name == 'input_top_manage_post'


async def func_write_top_management_name_filter(_, __, query):
    """Фильтр для хэндлера записи ФИО главного управленца компании"""
    company_obj = USER_DATA_STORAGE[query.from_user.id].get('company')
    if company_obj:
        return company_obj.state_name == 'input_top_manage_name'


async def func_write_telephone_again_filter(_, __, query):
    """Фильтр для хэндлера записи контактного телефона...ещё один."""
    company_obj = USER_DATA_STORAGE[query.from_user.id].get('company')
    if company_obj:
        return company_obj.state_name == 'input_telephone_again'


async def func_write_email_again_filter(_, __, query):
    """Фильтр для хэндлера записи контактного мыла...ещё один."""
    user_obj = USER_DATA_STORAGE[query.from_user.id].get('user')
    return user_obj.state_name == 'input_email_again'


input_company_name_filter = filters.create(func_input_company_name_filter)
cancel_company_input_filter = filters.create(func_cancel_company_input_filter)
write_comp_name_filter = filters.create(func_write_comp_name_filter)
confirm_comp_data_filter = filters.create(func_confirm_comp_data_filter)
reject_comp_by_name_filter = filters.create(func_reject_comp_by_name_filter)
write_inn_filter = filters.create(func_write_inn_filter)
reject_comp_data_by_inn_filter = filters.create(func_reject_comp_data_by_inn_filter)
write_ogrn_filter = filters.create(func_write_ogrn_filter)
write_telephone_filter = filters.create(func_write_telephone_filter)
write_email_filter = filters.create(func_write_email_filter)
write_address_filter = filters.create(func_write_address_filter)
write_top_management_post_filter = filters.create(func_write_top_management_post_filter)
write_top_management_name_filter = filters.create(func_write_top_management_name_filter)
write_telephone_again_filter = filters.create(func_write_telephone_again_filter)
write_email_again_filter = filters.create(func_write_email_again_filter)
