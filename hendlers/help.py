from aiogram import Router
from aiogram.types.message import Message
from aiogram.filters.command import Command

routerHelp = Router()

@routerHelp.message(Command(commands='help'))
async def commandHelp(message: Message, logger):
    logger.info('Запускаем информирование об условиях использования')
    await message.answer(text=f'Правила использования робота')
