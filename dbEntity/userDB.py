import psycopg
from datetime import datetime


class UserDb:
    def __init__(self, pool, logger):
        self.pool = pool
        self.logger = logger

    #Добавляем ногово пользователя
    async def createUser(self, user_id: int) -> None:
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute("""INSERT INTO users (
                                            user_id,
                                            data_registration,
                                            blok_bot
                                            ) VALUES (%s, %s, %s)""", (
                                            user_id,
                                            datetime.now(),
                                            False
                                        ))
                except psycopg.OperationalError as ex:
                    self.logger.exception(
                        f'Возникла ошибка при проверке существования пользователя. is_user - UserDB - {repr(ex)}')


    #Проверяем, что пользователь не заблокировал сам себя
    async def is_user_blok(self, user_id):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    data = await cursor.execute('SELECT blok_bot FROM users WHERE user_id=%s', (user_id,))
                    blok_bot = await data.fetchone()
                    if blok_bot == None:
                        return False
                    else:
                        return blok_bot[0]
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка при проверке болкировки у пользователя. {repr(ex)} '
                                          f'Ошибка - {ex.__class__.__name__}')


    #Разблокировка пользователя
    async def lift_no_blok(self, user_id):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute('UPDATE users SET blok_bot=%s WHERE user_id=%s', (False, user_id,))
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Ошибка при разблокировке пользователя {repr(ex)} Ошибка - {ex.__class__.__name__}')


    #Блокировка пользователя
    async def blok_user(self, user_id):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute('UPDATE users SET blok_bot=%s WHERE user_id=%s', (True, user_id))
                except psycopg.OperationalError() as ex:
                    self.logger.exception(f'Ошибка при блокировке пользователя {repr(ex)} {ex.__class__.__name__}')



    #     async with self.connection:
    #         async with self.connection.cursor() as cursor:
    #             try:
    #                 await cursor.execute("""INSERT INTO users (
    #                                 user_id,
    #                                 data_registration,
    #                                 blok_bot
    #                             ) VALUES (%s, %s, %s)""", (
    #                             user_id,
    #                             date.today(),
    #                             False
    #                         ))
    #                 self.connection.close()
    #             except psycopg.OperationalError as ex:
    #                 self.logger.exception('Ошибка записи в базу данных нового пользователя')
    #                 self.logger.info('Ошибка записи в базу данных нового пользователя')

    #Проверяем наличие пользователя в базе данных
    async def is_user(self, user_id: int) -> int:
        # logger.info('Начало проверки пользователя в базе данных')
        # async with self.connection:
        #     async with self.connection.cursor as cursor:
        #         try:
        #             id = await cursor.execute(f"""SELECT id FROM users WHERE""")
        #             self.connection.close()
        #         except psycopg.OperationalError as ex:
        #             logger.exception(f'При проверке пользователя в базе возникла ошибка - {repr(ex)}. error - is_user - UserDB')
        idUser = None
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    cur = await cursor.execute('SELECT id FROM users WHERE user_id=%s', (user_id,))
                    idUser = await cur.fetchone()
                    if idUser == None:
                        return 0
                    else:
                        return idUser[0]
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'Возникла ошибка при проверке существования пользователя. is_user - UserDB - {repr(ex)}')
        return idUser

