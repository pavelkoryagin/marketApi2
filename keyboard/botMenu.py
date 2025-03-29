from aiogram import Bot
from aiogram.types import BotCommand
import logging
from error.log_files import DebugFilter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='[%(asctime)s] #%(levelname)-8s %(filename)s:'
                                  '%(lineno)d - %(name)s:%(funcName)s - %(message)s')
error_file = logging.FileHandler('./bot/error/logsmenu.log', 'w', encoding='utf-8')
error_file.addFilter(DebugFilter())
error_file.setFormatter(formatter)
logger.addHandler(error_file)

logger.debug('Старт функции меню')


async def set_mein_menu(bot: Bot):
    main_menu = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/tovaradd', description='Добавление товаров'),
        BotCommand(command='/stop', description='Отменить добавление товара'),
        BotCommand(command='/clear', description='Удалить все товары'),
        BotCommand(command='/moitovari', description='Мои товары'),
        BotCommand(command='/podpiska', description='Оформить подписку'),
        BotCommand(command='/help', description='Правила использования')
    ]
    await bot.set_my_commands(main_menu)


logger.debug('Стоп функции меню')
