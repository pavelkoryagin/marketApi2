import aiohttp
import asyncio
from fake_useragent import UserAgent
from random import random


async def read_json(url, session, proxy, proxy_autx):
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

    tovar = dict()

    async with session.get(url=url, proxy=proxy, proxy_auth=proxy_autx) as response:
        assert response.status == 200
        return await response.text()



async def main():
    proxy1 = 'http://45.144.170.95:8000'
    proxy2 = 'http://45.144.169.118:8000'
    proxy3 = 'http://192.109.91.26:8000'

    proxyAutx1 = aiohttp.BasicAuth('YZWbvc', '6crqnT')
    proxyAutx2 = aiohttp.BasicAuth('YZWbvc', '6crqnT')
    proxyAutx3 = aiohttp.BasicAuth('YZWbvc', '6crqnT')

    dataWB = [(6, 1, 1,
               'https://stepik.org/lesson/742822/step/4?unit=744611'),
              (7, 1, 1,
               'https://stepik.org/lesson/742822/step/4?unit=744611'),
              (8, 1, 1,
               'https://stepik.org/lesson/742822/step/4?unit=744611'),
              (6, 1, 1,
               'https://stepik.org/lesson/742822/step/4?unit=744611'),
              (7, 1, 1,
               'https://stepik.org/lesson/742822/step/4?unit=744611'),
              (8, 1, 1,
               'https://stepik.org/lesson/742822/step/4?unit=744611'),
              (6, 1, 1,
               'https://stepik.org/lesson/742822/step/4?unit=744611'),
              (7, 1, 1,
               'https://stepik.org/lesson/742822/step/4?unit=744611'),
              (8, 1, 1,
               'https://stepik.org/lesson/742822/step/4?unit=744611')
              ]
    tasks = []
    urls = []

    async with aiohttp.ClientSession(trust_env=True) as session:
        for data in dataWB:
            if len(urls) == 3:
                task1 = asyncio.create_task(read_json(urls[0], session, proxy1, proxyAutx1))
                tasks.append(task1)
                task2 = asyncio.create_task(read_json(urls[1], session, proxy2, proxyAutx2))
                tasks.append(task2)
                task3 = asyncio.create_task(read_json(urls[2], session, proxy3, proxyAutx3))
                tasks.append(task3)

                try:
                    #await asyncio.gather(*tasks)
                    for i, t in enumerate(asyncio.as_completed((task1, task2, task3)), start=1):
                        tovar = await t
                        print(tovar)
                except Exception as ex:
                    repr(ex)

                urls.clear()
                tasks.clear()
            else:
                id, fk_id_user, fk_id_magazin, url = data
                urls.append(url)
                print(len(urls))

        # async with session.get(url='https://stepik.org/lesson/742822/step/4?unit=744611', proxy=proxy1, proxy_auth=proxyAutx1) as response:
        #     print(await response.text())


asyncio.run(main())
