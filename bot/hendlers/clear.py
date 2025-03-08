from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from bot.db.dbEntity.tovarDB import TovarDB
from bot.db.dbEntity.userDB import UserDb
from aiogram import Router, F
from bot.keyboard.buttonTovar import keyboardAddTovar, DeleteOneTovarCallbackFactory

clearRouter = Router()

@clearRouter.message(Command(commands='clear'))
async def clearTovars(message: Message, pool, logger):
    user_id = message.from_user.id
    #Получить Id пользователя в базе данных
    try:
        userDB = UserDb(pool=pool, logger=logger)
        idUserInDB = await userDB.is_user(user_id)
    except Exception as ex:
        logger.exception(f'Ошбка получения ID пользователя из базы для удаления всех товаров'
                         f'{repr(ex)} {ex.__class__.__name__}')

    #Удалить у пользователя все товары, которые находятся в базе данных
    if idUserInDB > 0:
        try:
            tovarDB = TovarDB(pool=pool, logger=logger)
            await tovarDB.delete_alles_tovars(idUserInDB)
            await message.answer(text='Все товары удалены из вашего личного кабинета!'
                                      'Вы всегда можете добавить новый товар для мониторинга',
                                 reply_markup=keyboardAddTovar)
        except Exception as ex:
            logger.exception(f'Ошбка удаления всех товаров у пользователя в БД'
                             f'{repr(ex)} {ex.__class__.__name__}')


@clearRouter.callback_query(F.data == 'delete_vse_tovar')
async def delete_vse_tovars(callback: CallbackQuery, pool, logger):
    user_id = callback.from_user.id
    #Получить Id пользователя в базе данных
    try:
        userDb = UserDb(pool=pool, logger=logger)
        idUserInDB = await userDb.is_user(user_id)
    except Exception as ex:
        logger.exception(f'Ошибка при получении Id пользователя из базы'
                         f'{repr(ex)} {ex.__class__.__name__}')

    # Удалить у пользователя все товары, которые находятся в базе данных
    if idUserInDB > 0:
        try:
            await callback.answer()
            tovarDB = TovarDB(pool=pool, logger=logger)
            await tovarDB.delete_alles_tovars(idUserInDB)
            await callback.message.answer(text='Все товары удалены из вашего личного кабинета!'
                                      'Вы всегда можете добавить новый товар для мониторинга',
                                 reply_markup=keyboardAddTovar)
        except Exception as ex:
            logger.exception(f'Ошбка удаления всех товаров у пользователя в БД'
                             f'{repr(ex)} {ex.__class__.__name__}')


@clearRouter.callback_query(DeleteOneTovarCallbackFactory.filter())
async def delete_one_tovar_callback(callback: CallbackQuery, callback_data: DeleteOneTovarCallbackFactory, pool, logger):
    id_tovara = callback_data.id_moi_tovar
    await callback.answer()
    tovarDB = TovarDB(pool=pool, logger=logger)
    await tovarDB.delete_one_tovar(id_tovara)
    await callback.message.answer(text='Товар удален.')
