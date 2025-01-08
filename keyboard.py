from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_get_num = InlineKeyboardButton('Получить номер', callback_data='button_get_num')
keyboard_first_menu = InlineKeyboardMarkup().add(button_get_num)

button_eng = InlineKeyboardButton('Англия', callback_data='country_16')
button_vietnam = InlineKeyboardButton('Вьетнам', callback_data='country_10')
button_india = InlineKeyboardButton('Индия', callback_data='country_22')
button_indonesia = InlineKeyboardButton('Индонезия', callback_data='country_6')
keyboard_select_country = InlineKeyboardMarkup(resize_keyboard=True).row(button_eng,
                                                                         button_vietnam).row(button_india,
                                                                                             button_indonesia)

button_get_code = InlineKeyboardButton('Код', callback_data='button_code')
button_cancel = InlineKeyboardButton('Отмена', callback_data='button_cancel')
keyboard_thr_menu = InlineKeyboardMarkup(resize_keyboard=True).add(button_get_code).add(button_cancel)
