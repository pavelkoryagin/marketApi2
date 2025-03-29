import time
from datetime import datetime, timedelta
import psycopg
import asyncio


class PodpiskaDB:
    def __init__(self, pool, logger):
        self.pool = pool
        self.logger = logger

    #Проверка подписки
    async def is_podpiska(self, fk_user_id: int) -> bool:
        async with (self.pool.connection() as connection):
            async with connection.cursor() as cursor:
                try:
                    data = await cursor.execute('SELECT podpiska FROM podpiska WHERE fk_id_user=%s', (fk_user_id,))
                    res = await data.fetchone()
                    if res == None:
                        #Если пользователя не существует, то подписка тоже не существует
                        return False
                    else:
                        podpiska = res[0]
                        return podpiska
                except psycopg.OperationalError as ex:
                    self.pool.exception(f'Ошибка при проверке наличия подписки у пользователя {repr(ex)}. {ex.__class__.__name__}')

    #Проверка количества товаров в подписке
    async def is_tovarov_podpiska(self, fk_user_id) -> int:
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    res = await cursor.execute('SELECT tovarov FROM podpiska WHERE fk_id_user=%s', (fk_user_id,))
                    data = await res.fetchone()
                    if data == None:
                        return 2
                    else:
                        tovarov = int(data[0])
                        return tovarov
                    return data
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка получения значения доступных товаров по подписке'
                                          f'{repr(ex)} {ex.__class__.__name__}')


    #Обновление наличия подписки по дате
    async def obnovi_podpiska_data(self):
        #Обновить подписку по дате
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    dat = datetime.datetime + (60*60*24*30)
                    await cursor.execute('UPDATE podpiska SET podpiska=%s WHERE data_podpiska < %s', (False, dat))
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка обновления подписки по дате {repr(ex)} {ex.__class__.__name__}')


    #добавляем пользователю подписку
    async def set_podpiska(self, fk_user_id, count_tovarov):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    dat = datetime.now()
                    await cursor.execute(f'UPDATE podpiska SET podpiska=%s, data_podpiska=%s, tovarov=%s WHERE fk_user_id=%s', (True, dat, fk_user_id, count_tovarov)).commit()
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка при установке в базу наличия подписки {repr(ex)}. {ex.__class__.__name__}')


    #Удаляем пользователю подписку
    async def del_podpiska(self, fk_user_id):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute("UPDATE podpiska SET podpiska=%s, data_podpiska=%s WHERE fk_id_user=%s", (False, None, fk_user_id))
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Установка в базе данных подписки для пользователя прошла с ошибкой'
                                          f'{repr(ex)}. {ex.__class__.__name__}')


    #Заводим для нового пользователя с подпиской с FALSE
    async def new_user_podpiska(self, user_id):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute("""
                        INSERT INTO podpiska (
                                fk_id_user,
                                podpiska,
                                data_podpiska,
                                tovarov) VALUES (%s, %s, %s, %s)
                            """, (
                                user_id,
                                False,
                                None,
                                2
                        ))
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка добавления пользователя в таблицу подписка'
                                          f'{repr(ex)} {ex.__class__.__name__}')

# data1 = datetime.now()
# time.sleep(3)
# data2 = datetime.now()
# print(data1 < data2)
# print(data1)
# print(data2)

