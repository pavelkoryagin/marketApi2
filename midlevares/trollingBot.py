from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from aiogram.fsm.storage.redis import RedisStorage
import asyncio

class ThrottlingMidleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        user = f'user{event.from_user.id}'
        chec_user = await self.storage.redis.get(name=user)
        if chec_user:
            if int(chec_user.decode()) == 1:
                await self.storage.redis.set(name=user, value=0,ex=10)
