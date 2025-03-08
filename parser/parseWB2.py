import asyncio
from asyncio import CancelledError
from asyncio import Semaphore
from aiohttp import ClientSession, InvalidUrlClientError
import aiohttp
from fake_useragent import UserAgent
import random
from bot.db.parseDB import ParseDB
import time


class ParseWB2:
    def __init__(self, proxies: list, proxies_login: str, proxies_password: str, pool, logger):
        self.proxies = proxies,
        self.login = proxies_login,
        self.password = proxies_password,
        self.pool = pool,
        self.logger = logger

    def res_proxies(self):
        for i in self.proxies:
            listProxies = i
        return listProxies

    async def read_json(self, url, id, session: ClientSession, proxy, proxy_autx, semaphore: Semaphore):
        userAgent = UserAgent()

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json; charset=utf-8',
            'x-requested-with': 'XMLHttpRequest',
            'User-agent': userAgent.random
        }

        async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_autx) as response:
            async with semaphore:
                assert response.status == 200
                js = await response.json()
                data = {'id': id, 'js': js}
                return data

    async def parseWB(self, dataWB):
        start = time.perf_counter()
        proxy = self.res_proxies()
        proxyAutx = aiohttp.BasicAuth(str(self.login[0]), str(self.password[0]))
        # parseDB = ParseDB(str(self.pool), str(self.logger))
        # dataWB = await parseDB.startParseLoadWB()
        tasks = []
        semaphore: Semaphore = Semaphore(3)
        i = -1
        count = 0
        async with aiohttp.ClientSession(trust_env=True) as session:
            for dates in dataWB:
                id, url = dates
                if i == 2:
                    i = 0
                else:
                    i = i + 1
                task = asyncio.create_task(self.read_json(url, id, session, proxy[i], proxyAutx, semaphore))
                tasks.append(task)

            try:
                #True что бы в случае исключения в 1 задаче полючить результаты в других
                data = await asyncio.gather(*tasks, return_exceptions=True)
                #ВАЖНО!!!!!!
                result = []
                for res in data:
                    if isinstance(res, Exception):
                        self.logger(f'Ошбка {Exception} {res}')
                        #Залогировать ошибку после просмотра резальтата работы программы
                    else:
                        result.append(res)  #Так можно вернуть результат только без ошибок
            except Exception as ex:
                self.logger(f'Ошибка парсера валдберис {repr(ex)}')

        times = time.perf_counter() - start
        #return {'times': times, 'tovar': data}
        return {'times': times, 'tovar': result}
