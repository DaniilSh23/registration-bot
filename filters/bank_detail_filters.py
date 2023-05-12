from pyrogram import filters

from settings.config import USER_DATA_STORAGE


async def func_start_input_bank_detail_filter(_, __, query):
    """Фильтр для хэндлера старта сбора реквизитов банка."""
    return query.data == 'input_bank_detail'


async def func_cancel_bank_detail_input_filter(_, __, query):
    """Фильтр для кнопки отмена ввода банковских реквизитов"""
    return query.data == 'cancel_inpt_bank'


async def func_write_bik_filter(_, __, message):
    """Фильтр для хэндлера записи БИК."""
    bank_obj = USER_DATA_STORAGE[message.from_user.id].get('bank')
    if bank_obj:
        return bank_obj.state_name == 'bik_input'


async def func_write_cor_a_filter(_, __, message):
    """Фильтр для хэндлера записи кор.счёта"""
    bank_obj = USER_DATA_STORAGE[message.from_user.id].get('bank')
    if bank_obj:
        return bank_obj.state_name == 'input_cor_a'


async def func_write_bank_name_filter(_, __, message):
    """Фильтр для хэндлера записи названия банка."""
    bank_obj = USER_DATA_STORAGE[message.from_user.id].get('bank')
    if bank_obj:
        return bank_obj.state_name == 'input_bank_name'


async def func_write_rs_filter(_, __, message):
    """Фильтр для хэндлера записи расчётного счёта."""
    bank_obj = USER_DATA_STORAGE[message.from_user.id].get('bank')
    if bank_obj:
        return bank_obj.state_name == 'input_rs'


async def func_confirm_bank_data_filter(_, __, query):
    """Фильтр для хэндлера подтверждения банковских данных от ДаДата."""
    return query.data == 'conf_bank'


async def func_reject_bank_data_filter(_, __, query):
    """Фильтр для хэндлера НЕ подтверждения банковских данных от ДаДата."""
    return query.data == 'reject_bank_by_bik'


start_input_bank_detail_filter = filters.create(func_start_input_bank_detail_filter)
cancel_bank_detail_input_filter = filters.create(func_cancel_bank_detail_input_filter)
write_bik_filter = filters.create(func_write_bik_filter)
write_cor_a_filter = filters.create(func_write_cor_a_filter)
write_bank_name_filter = filters.create(func_write_bank_name_filter)
write_rs_filter = filters.create(func_write_rs_filter)
confirm_bank_data_filter = filters.create(func_confirm_bank_data_filter)
reject_bank_data_filter = filters.create(func_reject_bank_data_filter)
