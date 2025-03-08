import asyncio
from asyncio import CancelledError
from asyncio import Semaphore
from aiohttp import ClientSession
import aiohttp
from fake_useragent import UserAgent
from random import randint
from bot.db.parseDB import startParseLoadWB, loadParseWBPrizeNew
import time


#Получаем json со страницы валдбериса
async def read_json(url: str, id: int, session: ClientSession, proxy, proxy_autx, semaphore: Semaphore):
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



async def parseWB():
    start = time.perf_counter()
    proxy = ['http://45.144.170.95:8000', 'http://45.144.169.118:8000', 'http://192.109.91.26:8000']
    proxyAutx = aiohttp.BasicAuth('YZWbvc', '6crqnT')
    dataWB = startParseLoadWB()
    tasks = []
    semaphore: Semaphore = Semaphore(3)
    i = -1
    async with aiohttp.ClientSession(trust_env=True) as session:
        for dates in dataWB:
            id, url = dates
            if i == 2:
                i = 0
            else:
                i = i + 1
            task = asyncio.create_task(read_json(url, id, session, proxy[i], proxyAutx, semaphore))
            tasks.append(task)

        try:
            await asyncio.gather(*tasks)
        except Exception as ex:
            print(repr(ex))

    stopTime = time.perf_counter() - start
    print(stopTime)







asyncio.run(parseWB())


# async def get_url(url: str, session: ClientSession, semaphore: Semaphore):
#     print('Старт Семафора')
#     async with semaphore:
#         print('Открываем подключение')
#         response = await session.get(url)
#         print('Закрываем подключение')
#         return response.status
#
#
# async def main():
#     start = time.perf_counter()
#     # Хотя мы запускаем 1000 задач, одновременно будут выполняться только 10 задач.
#     semaphore: Semaphore = Semaphore(100)
#     async with ClientSession() as session:
#         tasks = [asyncio.create_task(get_url("https://www.example.com", session, semaphore))
#                  for _ in range(5000000)]
#         await asyncio.gather(*tasks)
#         # for i, t in enumerate(asyncio.as_completed(*tasks), start=0):
#         #     res = await t
#         #     print(res)
#     stop = time.perf_counter() - start
#     print(stop)
#
# if __name__ == "__main__":
#     asyncio.run(main())


# import asyncio
#
# async def msg(text):
#     await asyncio.sleep(0.1)
#     print(text)
#
# async def long_msg():
#     print('Старт большой задержки')
#     await asyncio.sleep(3)
#     print('Конец большой задержки')
#
#
# async def main():
#     await msg('Привет')
#     task = asyncio.create_task(long_msg())
#     #await long_msg()
#     await msg("Привет еще раз")
#     await task
#     # task1 = asyncio.create_task(msg('Privet'))
#     # task2 = asyncio.create_task(long_msg())
#     # await asyncio.gather(task2, task1)
#
# asyncio.run(main())
