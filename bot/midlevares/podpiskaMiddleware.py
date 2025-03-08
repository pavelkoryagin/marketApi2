import time
from aiogram.types import Message
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
import psycopg
from bot.db.dbEntity.tovarDB import TovarDB
from bot.db.dbEntity.podpiskaDB import PodpiskaDB
from bot.db.dbEntity.userDB import UserDb


class PodpiskaMiddleware(BaseMiddleware):
    def __init__(self, pool, logger):
        BaseMiddleware.__init__(self)
        self.pool = pool
        self.logger = logger


    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        #Если подключать к главному роутеру, то может сильно загражать основной поток
        user: User = data.get('event_from_user')
        user_id = user.id
        userDB = UserDb(self.pool, self.logger)
        fk_user_id = await userDB.is_user(user_id)
        podpiska = PodpiskaDB(self.pool, self.logger)
        count_tovarov_podpiska = await podpiska.is_tovarov_podpiska(fk_user_id)
        tovar = TovarDB(self.pool, self.logger)
        count_tovars = await tovar.user_count_tovar(fk_user_id)
        if count_tovars == count_tovarov_podpiska:
            result = await handler(event, data)
            return result
        #
        # await result.message.answer(text="Количество товаров превышено")



        #print('Проверяем наличие подписки у пользователя. Если нет, то дальше не идем и оповещаем, что нужно оплать')

        #return result

