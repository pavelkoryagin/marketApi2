import psycopg
import datetime
from bot.entity.podpiska import Podpiska

class User:
    def __init__(self, user_id: int, data_registration: datetime, blok: bool, podpiska: Podpiska):
        self.user_id: int = user_id,
        self.data_registration: datetime = data_registration,
        self.blok: bool = blok,
        self.podpiska = podpiska

    async def get_user(self):
        return User(self.user_id, self.data_registration, self.blok, self.podpiska)

    #Проверяем существование пользователя
    async def is_user(self):
        return await self.get_user()


    async def is_podpiska(self):
        pass
        print('Получаем подписку из класса подписки по методу этого класса')