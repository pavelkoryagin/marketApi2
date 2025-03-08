import asyncio
import logging
import sys
from asyncio import WindowsSelectorEventLoopPolicy

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.hendlers.apsched import parsing_magazines
from bot.hendlers.rassilka import rassilka
from bot.config.config import Config, load_config
from bot.db.db_connect import dbConnection, adbConnection
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.error.log_files import DebugFilter
from bot.keyboard.botMenu import set_mein_menu
from bot.hendlers import message, hendlersStart, hendlertovar, blokBotUser, clear, help, moitovari, podpiska

from bot.midlevares.podpiskaMiddleware import PodpiskaMiddleware


async def main():
    #Иницилиилизируем логер
    logger = logging.getLogger(__name__)
    #Устанавливаем уровень логирования
    #logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    #Устанвавливаем форматирование
    formatter = logging.Formatter(fmt='[%(asctime)s] #%(levelname)-8s %(filename)s:'
                                      '%(lineno)d - %(name)s:%(funcName)s - %(message)s')
    #Инициилизируем хэндлеры для вывода на экран и записи в файл
    error = logging.StreamHandler(sys.stdout)
    #ДОбавляем фильтацию логов
    error.addFilter(DebugFilter())
    #Устанавливаем форматирование
    error.setFormatter(formatter)
    #Добавляем хэндлер к логеру
    logger.addHandler(error)
    #Пишем логи в файл
    error_file = logging.FileHandler('bot/error/logs.log', 'w', encoding='utf-8')
    error_file.setLevel(logging.DEBUG)
    error_file.addFilter(DebugFilter())
    error_file.setFormatter(formatter)
    logger.addHandler(error_file)
    #Информироуем о старте бота
    logger.info('Запуск бота')


    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    proxies: list = config.proxies.proxies
    proxies_login: str = config.proxies.login
    proxies_password: str = config.proxies.password

    # class Pavel:
    #     def __init__(self, some):
    #         self.some = some
    #
    #     def privet(self):
    #         print(self.some)
    #
    # some_var = Pavel("Привет")

    #Регистрируем точку входа в базу данных
    dbConnect = dbConnection(config)
    #Асинхронное подключение к базе данных
    pool = await adbConnection(config, logger)

    scheduler = AsyncIOScheduler()
    # #scheduler.add_job(send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
    #                   #kwargs={'bot': bot})
    # # scheduler.add_job(send_message_time, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute + 1,
    # #                   start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(parsing_magazines,
                      trigger='interval',
                      seconds=10800,
                      kwargs={'bot': bot,
                              'pool': pool,
                              'logger': logger,
                              'proxies': proxies,
                              'proxies_login': proxies_login,
                              'proxies_password': proxies_password})


    scheduler.add_job(rassilka,
                      trigger='interval',
                      seconds=7200,
                      kwargs={'bot': bot,
                              'pool': pool,
                              'logger': logger})



    scheduler.start()

    #Регистрируем роутеры в диспетчере
    logger.info('Регистрируем в диспетчере роутеры')
    dp.include_router(hendlersStart.startRouter)
    dp.include_router(help.routerHelp)
    dp.include_router(hendlertovar.tovarRouter)
    dp.include_router(clear.clearRouter)
    dp.include_router(moitovari.moiTovaresRouter)
    #Подписка
    #Хорошо бы сразу информировать пользователя что лимит по товарам исчерпан и нужно удалять или оформлять подписку
    dp.include_router(message.routerMessage)
    dp.include_router(blokBotUser.blokBotUser)

    #Регистрируем мидлевари
    #dp.update.outer_middleware(PodpiskaMiddleware(pool, logger))

    # НАстраиваем главное меню бота
    logger.info('Подключаем меню бота')
    await set_mein_menu(bot)

    logger.info('Запускаем бота')
    await bot.delete_webhook(drop_pending_updates=True)
    #await dp.start_polling(bot, dbConnect=dbConnect, logger=logger, some_var=some_var)
    #await dp.start_polling(bot, dbConnect=dbConnect, adbConnect=adbConnect, logger=logger)
    await dp.start_polling(
                        bot,
                        dbConnect=dbConnect,
                        pool=pool,
                        logger=logger,
                        proxies=proxies,
                        proxies_login=proxies_login,
                        proxies_password=proxies_password
    )


if sys.platform == "win32":
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
asyncio.run(main())
