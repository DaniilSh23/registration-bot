from pyrogram import filters

from settings.config import USER_DATA_STORAGE


async def func_display_bank_data_filter(_, __, query):
    """Фильтр для нажатия кнопки отображения банковских реквизитов."""
    return query.data == 'info_about_bank'


async def func_display_company_data_filter(_, __, query):
    """Фильтр для нажатия кнопки отображения данных о компании."""
    return query.data == 'info_about_comp'


async def func_plug_handler_filter(_, __, query):
    """Фильтр для хэндлера-заглушки"""
    return query.data == 'plug'


async def func_i_paid_filter(_, __, query):
    """Фильтр для кнопки Я ОПЛАТИЛ"""
    return query.data == 'i_paid'


async def func_rate_bot_filter(_, __, query):
    """Фильтр для кнопок оценки бота"""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'rate_bot'


async def func_filter_input_rating(_, __, message):
    """Фильтр для обработчика ввода коммента к оценке бота"""
    if USER_DATA_STORAGE.get(message.from_user.id):
        if USER_DATA_STORAGE[message.from_user.id].get('user'):
            return USER_DATA_STORAGE[message.from_user.id].get('user').state_name == 'input_rating_comment'


async def func_filter_rating_without_comment(_, __, query):
    """Фильтр для обработки нажатия на кнопку БЕЗ КОММЕНТАРИЕВ. Это когда клиент не хочет комментировать свою оценку"""
    return query.data == 'no_rating_comments'


display_bank_data_filter = filters.create(func_display_bank_data_filter)
display_company_data_filter = filters.create(func_display_company_data_filter)
plug_handler_filter = filters.create(func_plug_handler_filter)
i_paid_filter = filters.create(func_i_paid_filter)
rate_bot_filter = filters.create(func_rate_bot_filter)
filter_input_rating = filters.create(func_filter_input_rating)
filter_rating_without_comment = filters.create(func_filter_rating_without_comment)