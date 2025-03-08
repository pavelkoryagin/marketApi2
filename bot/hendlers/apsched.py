import threading

from aiogram import Bot
from parser.parseWB2 import ParseWB2
from bot.db.parseDB import ParseDB
from parser.parserOzon import ParseOzon
import concurrent.futures
import asyncio
from asyncio import Semaphore


#Вспомогательные функции для парсинга валдберис и озона
async def parse_apsch_wb(bot, pool, logger, proxies, proxies_login, proxies_password):
    await bot.send_message(928570159, text='Запущен парсинг')
    parseWB2 = ParseWB2(proxies, proxies_login, proxies_password, pool, logger)
    parseDB = ParseDB(pool, logger)
    dataWB = await parseDB.startParseLoadMagazin(1)
    if dataWB != None and len(dataWB) > 0:
        WBResTime = await parseWB2.parseWB(dataWB)
        tovar = WBResTime['tovar']
        parseDB = ParseDB(pool, logger)
        await parseDB.loadParseWBPrizeNew(tovar)
        # if WBResTime:
        #     await bot.send_message(928570159, text=f'Время парсинга WB - {WBResTime['times']}.')


def wb_parse(bot, pool, logger, proxies, proxies_login, proxies_password):
    asyncio.run(parse_apsch_wb(bot, pool, logger, proxies, proxies_login, proxies_password))

async def parse_apsh_ozon(bot, pool, logger, proxies, proxies_login, proxies_password):
    parserOzon = ParseOzon(pool, logger)
    parseDB = ParseDB(pool, logger)
    dataOzon = await parseDB.startParseLoadMagazin(2)
    if dataOzon != None and len(dataOzon) > 0:
        tasks = []
        result = []
        semaphore: Semaphore = Semaphore(3)
        for data in dataOzon:
            id, url = data
            task = asyncio.create_task(parserOzon.parseOzonAPSH(1, url, id, semaphore))
            tasks.append(task)

        try:
            # True что бы в случае исключения в 1 задаче полючить результаты в других
            data = await asyncio.gather(*tasks, return_exceptions=True)
            # ВАЖНО!!!!!!
            for res in data:
                if isinstance(res, Exception):
                    logger(f'Ошбка {Exception} {res}')
                    # Залогировать ошибку после просмотра резальтата работы программы
                else:
                    result.append(res)  # Так можно вернуть результат только без ошибок
        except Exception as ex:
            logger(f'Ошибка парсера валдберис {repr(ex)}')

        parseDB = ParseDB(pool, logger)
        await parseDB.loadParseOzonPrizeNew(result)
    else:
        print('Пусто')

def ozon_parse(bot, pool, logger, proxies, proxies_login, proxies_password):
    asyncio.run(parse_apsh_ozon(bot, pool, logger, proxies, proxies_login, proxies_password))

#Создаем отдельные потоки для парсинга валдберис и озона
def parse_message_time(bot, pool, logger, proxies, proxies_login, proxies_password):
    concurent = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    # Парсим валдберс
    concurent.submit(wb_parse, bot, pool, logger, proxies, proxies_login, proxies_password)
    # Парсинг озона
    concurent.submit(ozon_parse, bot, pool, logger, proxies, proxies_login, proxies_password)
    concurent.shutdown(wait=True)


#Выводим парсинг магазинов в отдельный поток
async def parsing_magazines(bot: Bot, pool, logger, proxies, proxies_login, proxies_password):
    print('начали парсинг')
    t = threading.Thread(target=parse_message_time,
                         args=(bot, pool, logger, proxies, proxies_login, proxies_password),
                         daemon=False)
    t.start()




