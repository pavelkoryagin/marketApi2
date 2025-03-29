import psycopg

class MagazinDB:
    def __init__(self, pool, logger):
        self.pool = pool
        self.logger = logger

    async def get_magazib_id(self, url: str) -> int:
        #self.logger('Запрос к базе на получение id для маганина по url')
        async with self.pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    result = await cursor.execute(f"SELECT id FROM magazin WHERE url = %s", (url,))
                    idMagazin = await result.fetchone()
                    if idMagazin == None:
                        return 0
                    else:
                        return int(idMagazin[0])
                except psycopg.OperationalError as ex:
                    self.logger.exception(f'При запросе к базе для получения id для магазина по url '
                                          f'произошла ошибка. {repr(ex)}')
