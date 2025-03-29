import concurrent.futures
import asyncio
from dbEntity.tovarDB import TovarDB

async def zapros_rassilka(pool, logger):
    tovarDB = TovarDB(pool, logger)
    zena = await tovarDB.rassilka()
    if zena == None:
        rassilka = 0
        return rassilka
    else:
        return zena


async def rassilka(bot,  pool, logger):
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as concurent:
        futures.append(concurent.submit(zapros_rassilka, pool, logger))
        dates = futures[0]
        if dates.result() == 0:
            return
        else:
            data = await dates.result()
            n = 0
            #Узкое место, потом можно сделать функцию и запустить через несколько потоков
            for i in data:
                if n == 50:
                    await asyncio.sleep(60)
                url, zena_new, id_user = i
                await bot.send_message(id_user, text=f"<a href='{url}'>Цена на товар снизилась.</a> \nСейчас она составляет - {zena_new}")
                n = n + 1
