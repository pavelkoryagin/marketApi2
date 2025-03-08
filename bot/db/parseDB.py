import psycopg

from bot.db.db_connect import dbConnection

#Получаем данные по товарам валдберис для работы парсера
class ParseDB:
    def __init__(self, pool, logger):
        self.pool = pool
        self.logger = logger

    async def startParseLoadMagazin(self, id_magazin):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    # Далее нужно сделать так, что-бы просматривать наличие подписки и парсить только тех, у кого есть подписка
                    await cursor.execute("""
                            SELECT id, url_parsing FROM tovar WHERE fk_id_magazin = %s
                        """, (id_magazin,))
                    magazinWB = await cursor.fetchall()
                    return magazinWB
                except psycopg.OperationalError as ex:
                    self.logger(f'Ошибка при получении данных для парсинга WB')



    #ЗАписываем новую цену в базу данных по валбдберису
    async def loadParseWBPrizeNew(self, tovar):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    for data in tovar:
                        id = int(data['id'])
                        # name = data['js']['data']['products'][0]['name']
                        #product = int(data['js']['data']['products'][0]['sizes'][0]['price']['product'])
                        basic = int(data['js']['data']['products'][0]['sizes'][0]['price']['basic'])
                        total = int(data['js']['data']['products'][0]['sizes'][0]['price']['total'])
                        if total < basic:
                            zena_new = total / 100
                        else:
                            zena_new = basic / 100

                        await cursor.execute("""
                                UPDATE tovar 
                                SET zena_new = %s
                                WHERE id = %s
                                """, (zena_new, id))
                except psycopg.OperationalError as ex:
                    self.logger(f'Ошибка записиси новой цены в базу данных {repr(ex)}'
                                f'{ex.__class__.__name__}')

    #Запись новой цены озона
    async def loadParseOzonPrizeNew(self, data):
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                for res in data:
                    id = res['id']
                    zena = res['zena']
                    try:
                        await cursor.execute("""
                                                UPDATE tovar 
                                                SET zena_new = %s
                                                WHERE id = %s
                                            """, (zena, id))
                    except psycopg.OperationalError as ex:
                        self.logger(f'Ошибка записи новой цены при парсинге всех товаров в магазине озон'
                                    f'{repr(ex)}'
                                    f'{ex.__class__.__name__}')






# data = startParseLoadWB()
# print(data)
# for tupl in data:
#     id, url = tupl
#     print(id)
