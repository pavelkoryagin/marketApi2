import psycopg
from datetime import datetime
import asyncio

class TovarDB:
    def __init__(self, pool, logger):
        self.pool = pool
        self.logger = logger

    #проверка что товар уже не добавлен ранее
    async def is_tovar(self, url) -> bool:
        async with self.pool.connection() as connection:
            async with connection.cursor(binary=False) as cursor:
                try:
                    data = await cursor.execute("SELECT id FROM tovar WHERE url=%s", (url,))
                    res = await data.fetchone()
                    if res == None:
                        return False
                    else:
                        return True

                except psycopg.OperationalError as er:
                    self.logger.exception(f'Ошибка запросе к БД для проверки наличия в ней такого товара'
                                          f'{repr(er)} {er.__class__.__name__}')

    #Подсчет количества товаров у одного пользователя
    async def user_count_tovar(self, fk_user_id: int):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    cur = await cursor.execute(f"""
                                        SELECT COUNT(id) FROM tovar WHERE fk_id_user = %s 
                                    """, (fk_user_id,))
                    idTovar = await cur.fetchone()
                    if idTovar == None:
                        return 0
                    else:
                        return int(idTovar[0])
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'При запросе в БД количества товаров возникла ошибка - user_count_tovar -'
                                          f'TovarDB. {repr(ex)}')

    #Получение перечня товаров пользователя
    async def get_tovars_user(self, fk_id_user):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    data = await cursor.execute("""
                        SELECT id, url FROM tovar WHERE  fk_id_user=%s
                    """, (fk_id_user,))
                    result = await data.fetchall()
                    dict_url = dict()
                    if result != None:
                       dict_url = dict(result)
                       dict_url['false'] = False
                       return dict_url
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка при запросе перечня товаров в базе данных товары по пользователю'
                                          f'{repr(ex)} {ex.__class__.__name__}')


    #Добавление нового товара пользователю
    async def addNewTowar(self, fk_id_user, fk_id_magazin, url, url_parsing, artikul, zena) -> None:
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(f"""
                        INSERT INTO tovar (
                            fk_id_user,
                            fk_id_magazin,
                            url,
                            url_parsing,
                            artikul,
                            zena,
                            zena_new,
                            data
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        fk_id_user,
                        fk_id_magazin,
                        url,
                        url_parsing,
                        artikul,
                        zena,
                        0,
                        datetime.now()
                    ))
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка записи нового товара в БД {repr(ex)} {ex.__class__.__name__}')


    #Удаление одного товара у пользователя
    async def delete_one_tovar(self, idTovar) -> None:
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute('DELETE FROM tovar WHERE id = %s', (idTovar,))
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка при удалении товара с id = {idTovar}'
                                          f'{repr(ex)} {ex.__class__.__name__}')

    #Удаление всех товаров у пользователя
    async def delete_alles_tovars(self, fk_user_id) -> None:
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute('DELETE FROM tovar WHERE fk_id_user = %s', (fk_user_id,))
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка удаления всех товаров у пользователя'
                                          f'{repr(ex)} {ex.__class__.__name__}')


    #Получение товара, у которго новая цена меньше старой,
    #Перезаписываем новую цену вместо старой
    #Старую цену обозначаем как ноль
    async def rassilka(self):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    data = await cursor.execute("""
                                SELECT url, zena_new, user_id 
                                FROM tovar
                                INNER JOIN users ON tovar.fk_id_user = users.id
                                WHERE zena > zena_new
                            """)
                    zena = await data.fetchall()
                    await cursor.execute("""
                                UPDATE tovar
                                SET zena = zena_new
                                WHERE zena > zena_new
                            """)
                    return zena
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка получения меньшего означения цены для рассылки'
                                          f'{repr(ex)}'
                                          f'{ex.__class__.__name__}')

