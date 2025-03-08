from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

addTovar = InlineKeyboardButton(text='Добавить товар', callback_data='tovaradd')
deleteVseTovar = InlineKeyboardButton(text='Удалить все товары', callback_data='delete_vse_tovar')
addPodpiska = InlineKeyboardButton(text='Добавить подписку', callback_data='add_podpiska')

keyboardAddTovar = InlineKeyboardMarkup(inline_keyboard=[[addTovar], [addPodpiska]])
keyboarDeleteVseTovares = InlineKeyboardMarkup(inline_keyboard=[[deleteVseTovar]])


class DeleteOneTovarCallbackFactory(CallbackData, prefix="delete_one_tovar"):
    id_moi_tovar: int

