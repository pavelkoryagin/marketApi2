from aiogram import Router
from aiogram.types import Message

routerMessage = Router()

@routerMessage.message()
async def message(message: Message):
    # print(message.chat.id)
    # print(message.from_user.id)
    await message.answer('Для продолжения работы, выберите один из пунктов меню!')
