from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from dbEntity.userDB import UserDb
from keyboard.buttonTovar import keyboardAddTovar
from dbEntity.podpiskaDB import PodpiskaDB

startRouter = Router()

@startRouter.message(CommandStart())
async def start_message(message: Message, pool, logger):
    logger.info('Запускаем стартовый хэндлер НЕ ЗАБЫТЬ ПРОВЕРИТЬ ЧТО ПОЛЬЗОВАТЕЛЬ НЕ ЗАБЛОКИРОВАН')
    user_id = message.from_user.id
    try:
        await message.answer(text='Если Вам понравился товар в интернет-магазине '
                                  '<b><i><a href="https://www.wildberries.ru">Wildberries</a></i></b> или '
                                  '<b><i><a href="https://www.ozon.ru">Ozon</a></i></b>, но Вы хотите приобрести его за меньшую стоимость, '
                                  '<b>пришлите нам ссылку на товар</b> и Бот оповестить о снижении цены.\n '
                                  'Для добавления ссылки можно воспользоваться пунктом меню '
                                  '<b>/tovaradd</b> или соответствующей кнопкой.\n '
                                  ' <b>Максимальное количество товаров, которое можно добавлять без подписки - 1 товар.</b>'
                                  '<b>Подписка на 10 товаров - 100 рублей на 6 месяцев</b>. \n'
                                  'Если нужно получать выгрузку или мониторить'
                                  'большее количество товаров, смотри раздел <b>/help "Правила использования"</b>',
                             parse_mode='HTML',
                             reply_markup=keyboardAddTovar)
    except Exception as ex:
        logger.info('В команде старт возникла ошибка')
        logger.exception(f'При отправке команды /start возникла ошибка - {repr(ex)}')

    #await hendlerStartAddUser.addUser(user_id, dbConnect, logger)
    #Добавление в базу данных нового пользователя
    try:
        userDB = UserDb(pool, logger)
        #Проверяем пользователя в базе
        idUser = await userDB.is_user(user_id)
        if idUser == 0:
        #Если нет в базе то добавляем
            try:
                await userDB.createUser(user_id)
                # Добавляем пользователю подписку FALSE
                fk_user_id_podpiska = await userDB.is_user(user_id)
                podpiskaDB = PodpiskaDB(pool, logger)
                await podpiskaDB.new_user_podpiska(fk_user_id_podpiska)
            except Exception as exc:
                logger.exception(
                    f'Пользователь нажал на кнопку старт. Новый пользователь - {user_id} в базу не записан. {repr(exc)}')


        #Проверяем, что пользователь не заблокирован и его после нажания на кнопку старт нужно разблокировать
        if await userDB.is_user_blok(user_id):
            await userDB.lift_no_blok(user_id)
    except Exception as ex:
        logger.exception(f'Пользователь нажал на кнопку старт. Ошибка извлечения данных о пользователе из базы данных.')


# @startRouter.message(CommandStart())
# async def start_message(message: Message, some_var, dbConnect, logger):
#     logger.info('Запускаем стартовый хэндлер')
#     a = 0
#     b = 1
#     try:
#         c = b/a
#         print(c)
#     except ZeroDivisionError as ex:
#         #logger.error('Ошибка деления на ноль', exc_info=True)
#         logger.exception('Тут было исключение')
#     user_id = message.from_user.id
#     some_var.privet()
#     await message.answer(text='Если Вам понравился товар в интернет-магазине Wildberries или Ozon, но Вы хотите приобрести '
#                               'его за меньшую стоимость, Бот оповестит о снижении цены. Для этого необходимо'
#                               ' перейти в меню /tovaradd и добавить ссылку на интересующий Вас товар.  '
#                               'Максимальное количество товаров, которое можно добавлять - 10 товаров.')
#
#     await hendlerStartAddUser.addUser(user_id, dbConnect, logger)
