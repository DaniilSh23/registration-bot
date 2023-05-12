from pyrogram import filters

from settings.config import USER_DATA_STORAGE


async def func_filter_start_write_pers_data(_, __, query):
    """Фильтр для кнопки начала ввода персональных данных"""
    return query.data == 'start_write_pers_data'


async def func_filter_cancel_write_pers_data(_, __, query):
    """Фильтр для кнопки отмены ввода персональных данных"""
    return query.data == 'cncl_wrt_pers_data'


async def func_filters_ask_snils(_, __, message):
    """Фильтр для запроса СНИЛС."""
    user_data = USER_DATA_STORAGE.get(message.from_user.id)
    if user_data:
        return user_data['user'].state_name == 'input_passport'     # TODO: state будет другой


async def func_filter_wrt_snils_and_finish(_, __, message):
    """Фильтр для записи СНИЛС и финиша бота."""
    user_data = USER_DATA_STORAGE.get(message.from_user.id)
    if user_data:
        return user_data['user'].state_name == 'input_snils'


async def func_filter_i_signed(_, __, query):
    """Фильтр для кнопки Я ПОДПИСАЛ"""
    return query.data == 'i_signed'


filter_start_write_pers_data = filters.create(func_filter_start_write_pers_data)
filter_cancel_write_pers_data = filters.create(func_filter_cancel_write_pers_data)
filters_ask_snils = filters.create(func_filters_ask_snils)
filter_wrt_snils_and_finish = filters.create(func_filter_wrt_snils_and_finish)
filter_i_signed = filters.create(func_filter_i_signed)