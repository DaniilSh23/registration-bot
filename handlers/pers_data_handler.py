from pyrogram import Client, filters

from filters.pers_data_filters import filter_start_write_pers_data, filter_cancel_write_pers_data, filters_ask_snils, \
    filter_wrt_snils_and_finish, filter_i_signed
from keyboards.bot_keyboards import CNCL_WRT_PERS_DATA_KBRD, START_PERS_DATA_KBRD, RATE_BOT_KBRD, I_SIGNED_KBRD, \
    form_webapp_kbrd
from secondary_functions.req_to_bot_api import get_for_manage_reminds
from settings.config import USER_DATA_STORAGE


@Client.on_callback_query(filter_start_write_pers_data)
async def start_write_pers_data(client, callback):  # TODO: Скорее всего удалить
    """
    Начало заполнения персональных данных.
    Запрашиваем ссылку на веб-форму в Битриксе и присылаем её клиенту.
    """
    user_obj = USER_DATA_STORAGE[callback.from_user.id]['user']
    # TODO: Сделать механизм получения ссылки на веб-форму из Битрикса
    form_link = 'https://b24-tplb1d.bitrix24.site/crm_form_11vmr/'
    inline_kbrd = await form_webapp_kbrd(form_link=form_link)
    await callback.edit_message_text(
        text=f'🪪Пожалуйста, заполните <b>данные из формы ниже</b>.\n\n'
             f'<i>Если вы пользуетесь браузерной версией Telegram, то <a href="form_link">нажмите сюда<a></i>',
        reply_markup=inline_kbrd
    )
    user_obj.state_name = 'input_passport'


@Client.on_callback_query(filter_cancel_write_pers_data)
async def cancel_write_pers_data(client, callback):     # TODO: Скорее всего удалить
    """Отмена заполнения персональных данных."""

    user_obj = USER_DATA_STORAGE[callback.from_user.id]['user']
    user_obj.state_name = None
    await callback.edit_message_text(
        text=f'🙅<b>Вы отменили ввод персональных данных</b>.\n\n'
             f'Если ошиблись, то можно начать сначала. Приступим, это уже крайний шаг.\n\n'
             f'<i>Нажимая на кнопку <b>"Заполнить персональные данные"</b>, Вы даете свое согласие на '
             f'обработку и хранение персональных данных.</i>',
        reply_markup=START_PERS_DATA_KBRD
    )


@Client.on_message(filters.private & filters_ask_snils)
async def ask_snils(client, message):   # TODO: Скорее всего удалить
    """Записываем ........., спрашиваем СНИЛС"""

    user_obj = USER_DATA_STORAGE[message.from_user.id]['user']
    write_result = await user_obj.set_passport_data(passport_data=message.text)
    if write_result:    # Если запись прошла успешно
        await message.reply_text(
            text=f'🪪 Введите <b>СНИЛС</b>\n\n'
                 f'<i>Подсказка: 11 цифр без тире и пробелов.</i>\n'
                 f'<i>Пример: <code>12345678901</code></i>',
            reply_markup=CNCL_WRT_PERS_DATA_KBRD
        )
        user_obj.state_name = 'input_snils'
    else:   # TODO: Если какие-то данные, которые здесь будут, не прошли запись
        await message.reply_text(
            text=f'❕<b>Неверный формат паспортных данных</b>\n\n'
                 f'<i>Пример:</i> <code>1111 223344</code> - серия и номер разделены пробелом.\n\n'
                 f'🪪Вы ввели: {message.text}',
            reply_markup=CNCL_WRT_PERS_DATA_KBRD
        )
        user_obj.state_name = 'input_passport'


@Client.on_message(filters.private & filter_wrt_snils_and_finish)
async def write_snils_and_finish_him(client, message):  # TODO: Скорее всего удалить
    """Записываем СНИЛС и присылаем кнопку Я ПОДПИСАЛ"""

    user_obj = USER_DATA_STORAGE[message.from_user.id]['user']
    write_result = await user_obj.set_snils(snils=message.text)
    if write_result:    # Если данные валидны и успешно записались
        text_for_message = f'📧Спасибо, на вашу <b>почту ({user_obj.email}) придет письмо со ссылкой на МЧД</b>\n(пример письма на фото).\n\n' \
                           f'✍Подписание производится <b>с компьютера</b>, не забудьте <b>вставить ЭЦП</b>.'
        await message.reply_photo(
            photo='mail_example.jpeg',
            caption=text_for_message,
            reply_markup=I_SIGNED_KBRD
        )
        send_persdata_rslt = await user_obj.send_pers_data()
        if not send_persdata_rslt:
            await message.reply_text(
                text=f'🛠Неудачный запрос. Мы уже решаем эту проблему.\n'
                     f'Не удалось записать Ваши данные. Пожалуйста, попробуйте повторить позже.',
                reply_markup=START_PERS_DATA_KBRD
            )
        user_obj.state_name = None
        # Отправка запроса к Джанго для создания записи в таблице напоминалок
    else:   # Если данные не прошли запись
        await message.reply_text(
            text=f'❕<b>Неверный формат СНИЛС</b>\n\n'
                 f'<i>Подсказка: 11 цифр без тире и пробелов.</i>\n'
                 f'<i>Пример:\nВаш СНИЛС:<code>123-456-789 01</code>\nНеобходимо записать:<code>12345678901</code></i>',
            reply_markup=CNCL_WRT_PERS_DATA_KBRD
        )
        user_obj.state_name = 'input_snils'


@Client.on_callback_query(filter_i_signed)
async def i_signed_handler(client, callback):
    """Обработка нажатия кнопки Я ПОДПИСАЛ."""

    await callback.message.delete()
    await callback.message.reply_text(
        text=f'Благодарим Вас за уделённое время.\n\n'
             f'⭐️Оцените взаимодействие с ботом.',
        reply_markup=RATE_BOT_KBRD
    )
    # TODO: Отправка запроса к Джанго для удаления записи из таблицы напоминалок
    # Удаляем отложенную задачу для напоминания о необходимости подписи
    await get_for_manage_reminds(tlg_id=callback.from_user.id, reminder_type='s', act='del')

