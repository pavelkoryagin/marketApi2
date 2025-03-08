import asyncio
import aiohttp

sites = ['https://metanit.com/python/database/2.5.php'] * 100
async def download_site(url, session):
    async with session.get(url) as response:
        print(response.content.total_bytes)

async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.create_task(download_site(url, session))
            tasks.append(task)

        try:
            print("Начало парсинга")
            await asyncio.gather(*tasks)
        except Exception as ex:
            print(repr(ex))





asyncio.run(download_all_sites(sites))
