import psycopg
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types.message import Message
from bot.db.dbEntity.tovarDB import TovarDB
from bot.db.dbEntity.userDB import UserDb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.keyboard.buttonTovar import keyboarDeleteVseTovares, keyboardAddTovar, DeleteOneTovarCallbackFactory

moiTovaresRouter: Router = Router()

@moiTovaresRouter.message(Command(commands='moitovari'))
async def command_moi_tovari(message: Message, pool, logger):
    user_id = message.from_user.id
    count_tovar = 0
    tovarDB = TovarDB(pool, logger)
    #Получаекм номер пользователя в бд
    try:
        userDB = UserDb(pool=pool, logger=logger)
        idUserBD = await userDB.is_user(user_id)
        #Подсчитаем количество товаров у одного пользователя для сообщения
        count_tovar = await tovarDB.user_count_tovar(idUserBD)
    except Exception as ex:
        logger.exception(f'Ошибка получения ID пользователя в БД в хэндлере мои товары'
                         f'{repr(ex)} {ex.__class__.__name__}')


    #Получаем все товары из личного магазина
    # не забываем, что нужно добавить кнопку удалить все товары (посмотреть куда ее можно добавить)
    try:
        list_rovarov = await tovarDB.get_tovars_user(idUserBD)
    except psycopg.OperationalError as ex:
        logger.exception(f'Ошибка получения списка товаров у пользователя'
                         f'{repr(ex)} {ex.__class__.__name__}')

    if count_tovar > 0:
        await message.answer(text=f'Ваших товаров - {count_tovar}.\n',
                             reply_markup=keyboarDeleteVseTovares)

        for key, value in list_rovarov.items():
            delete_one_tovar = InlineKeyboardButton(text='Удалить товар',
                                                callback_data=DeleteOneTovarCallbackFactory(id_moi_tovar=f'{key}').pack())

            keyboardDeleteOneTovar = InlineKeyboardMarkup(inline_keyboard=[[delete_one_tovar]])
            await message.answer(text=f'<a href="{value}">{value}</a>',
                             reply_markup=keyboardDeleteOneTovar)
    else:
        await message.answer(text='Товары отсутстуют',
                             reply_markup=keyboardAddTovar)


