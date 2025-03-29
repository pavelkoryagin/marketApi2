from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated
from aiogram import Router
from db.dbEntity.userDB import UserDb


blokBotUser: Router = Router()

#Отлавливает блокировку пользователя
@blokBotUser.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blok_bot(event: ChatMemberUpdated, pool, logger):
    #print(f'Пользователь {event.from_user.id} заблокировал бота. Не забудь отметить блокировку в базе данных')
    #Записываем в базу, что пользователь заблокировал бота
    user_id = event.from_user.id
    userDB = UserDb(pool=pool, logger=logger)
    await userDB.blok_user(user_id=user_id)
