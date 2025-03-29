from aiohttp import InvalidUrlClientError
import aiohttp
from fake_useragent import UserAgent
import random


class ParseWB:
    def __init__(self, proxies: list, proxies_login: str, proxies_password: str, url: str, logger):
        self.proxies = proxies,
        self.login = proxies_login,
        self.password = proxies_password,
        self.url = url,
        self.logger = logger

    def res_proxies(self):
        for i in self.proxies:
            listProxies = i
        return listProxies

    async def parseWBAddTovar(self):
        proxy = self.res_proxies()
        proxyAyth = aiohttp.BasicAuth(str(self.login[0]), str(self.password[0]))
        url = str(self.url[0])

        useragent = UserAgent()

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json; charset=utf-8',
            'x-requested-with': 'XMLHttpRequest',
            'User-agent': useragent.random
        }
        i = random.randint(0, 2)
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url=url, headers=headers, proxy=proxy[i], proxy_auth=proxyAyth) as response:
                        assert response.status == 200
                        data = await response.json()
                        return data
                except InvalidUrlClientError as er:
                    self.logger.exception(f'Неверный url {repr(er)} {er.__class__.__name__}')
        except Exception as ex:
            self.logger.exception(f'Ошибка при попытке парсинга товара WB при добавлении {repr(ex)} {ex.__class__.__name__}')



#asyncio.run(parseWB())
