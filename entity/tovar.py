import asyncio
import concurrent.futures
import psycopg
from dbEntity.userDB import UserDb
from dbEntity.magazinDB import MagazinDB
from dbEntity.tovarDB import TovarDB
import re
from parser.parseWB import ParseWB
from parser.parserOzon import ParseOzon
from dbEntity.podpiskaDB import PodpiskaDB


class Tovar:
    def __init__(self, id_user: int, url: str):
        self.id_user = id_user
        self.url = url

    async def is_magazin_wb(self) -> int:
        magazin_wb: int = self.url.find('https://wildberries.ru')
        return magazin_wb

    async def is_magazin_ozon(self) -> int:
        magazin_ozon: int = self.url.find("https://ozon.ru")
        return magazin_ozon

    async def is_magazin_wb_www(self) -> int:
        magazin_wb: int = self.url.find('https://www.wildberries.ru')
        return magazin_wb

    async def is_magazin_ozon_www(self) -> int:
        magazin_ozon: int = self.url.find("https://www.ozon.ru")
        return magazin_ozon

    async def get_url(self, url) -> str:
        url_len = len(url)
        start_url_https = self.url.find('https://')
        link = url[start_url_https:url_len]
        return link

    async def addTovarWB(self, fk_id_user, fk_id_magazin, url, link, pool, logger, proxies, proxies_login, proxies_passowrd):
        tovar = dict()
        try:
            res = re.search(r'\d{7,20}', link)  # Ищем артикул в ссылке от пользователя
            # для базы данных и формирования ссылки для парсинга
            artikul = res[0]
            url_parsing = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=123585567&spp=30&ab_testing=false&nm={artikul}"
        except Exception as ex:
            logger.exception('Ошибка при получении артикула из сслка на озон')
            return

        parseWB = ParseWB(proxies, proxies_login, proxies_passowrd, url_parsing, logger)
        data = await parseWB.parseWBAddTovar()
        # print(data)
        tovar['name'] = data['data']['products'][0]['name']
        tovar['basic'] = int(data['data']['products'][0]['sizes'][0]['price']['basic']) / 100
        tovar['product'] = int(data['data']['products'][0]['sizes'][0]['price']['product']) / 100
        tovar['total'] = int(data['data']['products'][0]['sizes'][0]['price']['total']) / 100
        if tovar['product'] != 0:
            zena = tovar['product']
        else:
            zena = tovar['basic']

        # Записываем данные о товаре базу данных
        tovarDB = TovarDB(pool, logger)
        await tovarDB.addNewTowar(fk_id_user, fk_id_magazin, link, url_parsing, artikul, zena)

        return tovar


    async def addTovarOzon(self, fk_id_user, fk_id_magazin, url, link, pool, logger, proxies, proxies_login, proxies_passowrd):
        tovar = dict()
        tovar['name'] = False
        tovar['basic'] = ''
        tovar['total'] = ''

        parseOzon = ParseOzon(pool, logger)
        zenaPars = await parseOzon.parseOzon(1, link)
        zena = int(zenaPars)
        tovar['product'] = zena
        url_parsing = link
        artikul = None
        # Записываем данные о товаре в базу данных
        tovarDB = TovarDB(pool, logger)
        await tovarDB.addNewTowar(fk_id_user, fk_id_magazin, link, url_parsing, artikul, zena)
        tovar['error'] = False
        tovar['error_url'] = True

        return tovar


    def asyncio_main_ozon(self, fk_id_user, fk_id_magazin, url, link, pool, logger, proxies, proxies_login, proxies_passowrd):
        asyncio.run(self.addTovarOzon(fk_id_user, fk_id_magazin, url, link, pool, logger, proxies, proxies_login, proxies_passowrd))



    async def addTovar(self, pool, logger, proxies, proxies_login, proxies_passowrd) -> dict:
        logger.info('Начинаем добавление нового товара')
        tovar = dict()
        # ПОлучаем id пользователя в базе данных
        try:
            userDB = UserDb(pool=pool, logger=logger)
            fk_id_user = await userDB.is_user(self.id_user)
            if fk_id_user == 0:
                await userDB.createUser(self.id_user)
        except Exception as ex:
            logger.exception(f'При дабавлении товара, получении id пользователя из базы возникла ошибка.'
                             f' {repr(ex)} {ex.__class__.__name__}')

        #Получаем количество товаров
        try:
            tovarDB = TovarDB(pool, logger)
            count_tovar = await tovarDB.user_count_tovar(fk_id_user)
        except Exception as ex:
            logger.exception(f'При получении количества товаров из базы возникла ошибка.'
                             f' {repr(ex)} {ex.__class__.__name__}')

        #Проверяем подписку, по ней другие првила
        #Если подписка имеется, там проставлено количество допустимых товаров по подписке
        #Меняем переменную max_count_tovar на значение, которое выдано по подписке 10 или неограниченно
        podpiska = PodpiskaDB(pool=pool, logger=logger)
        max_tovar_user = await podpiska.is_tovarov_podpiska(fk_id_user)

        #Проверяем, что количество товаров не превышает значение доступного бесплатно или по подписке
        if count_tovar >= max_tovar_user:
            #Если количество товаров у пользователя меньше 10 тогда работем, иначе выходим отправив ERROR
            tovar['error'] = True
            tovar['text'] = (
                'Вы превысили допустимое количество товаров. Обратитесь к разделу <b>/help</b> для уточнения'
                'деталей')
            return tovar

        #В разных приложениях ссылки разные в начале могжет быть описание и т.д.
        #Нужно вычлинить только ссылку для парсинга (принципиально на озон)
        #На валдберис я сам ссылку формирую
        link = await self.get_url(self.url)
        noLink = [
                'https://www.wildberries.ru',
                'https://www.ozon.ru',
                'https://wildberries.ru',
                'https://ozon.ru',
                'https://www.wildberries.ru/',
                'https://www.ozon.ru/',
                'https://wildberries.ru/',
                'https://ozon.ru/'
        ]
        if link in noLink:
            tovar['error'] = True
            tovar['text'] = 'Пришлите пожалуйста ссылку на товар!'
            return tovar

        #Прроверить что товар уже не добавлен
        if await tovarDB.is_tovar(link):
            tovar['error'] = True
            #Неверная ссылка данный магазин не обслуживаем
            tovar['text'] = 'Похоже Вы уже добавляли данный товар!'
            return tovar

        #Проверяем что ссылка на магазин правильная
        magazinWB: int = await self.is_magazin_wb()
        magazinOzon: int = await self.is_magazin_ozon()
        magazinWBWWW: int = await self.is_magazin_wb_www()
        magazinOzonWWW: int = await self.is_magazin_ozon_www()
        # -1 значит ссылки неправильные и не содержат нужный нам магазин
        if magazinWB == -1 and magazinOzon == -1 and magazinWBWWW == -1 and magazinOzonWWW == -1:
            tovar['error'] = True
            tovar['text'] = 'Неверная ссылка данный магазин не обслуживаем'
            return tovar
        #Нашли наши адреса формируем правильный адрес магазина
        if magazinWB == 0 or magazinWB > 0 or magazinWBWWW > 0 or magazinWBWWW == 0:
            url_magazin = "https://www.wildberries.ru"
        if magazinOzon == 0 or magazinOzon > 0 or magazinOzonWWW == 0 or magazinOzonWWW > 0:
            url_magazin = "https://www.ozon.ru"


        #Получаем id магазина в базе данных
        try:
            magazinDB = MagazinDB(pool=pool, logger=logger)
            fk_id_magazin = await magazinDB.get_magazib_id(url_magazin)
        except psycopg.OperationalError as ex:
            logger.exception(f'При получении id магазина произошла ошибка {repr(ex)}'
                                      f'{ex.__class__.__name__}')

        # tovar['fk_id_user'] = fk_id_user
        # tovar['fk_id_magazin'] = fk_id_magazin
        # tovar['link'] = link
        # return tovar

        if fk_id_magazin == 1:
            tovar['error'] = False
            tovar['product'] = await self.addTovarWB(fk_id_user, fk_id_magazin, self.url, link, pool, logger, proxies,
                                                     proxies_login, proxies_passowrd)
            return tovar

        if fk_id_magazin == 2:
            conc = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            #future = conc.submit(self.asyncio_main_ozon, fk_id_user, fk_id_magazin, self.url, link, pool, logger, proxies,
            #                                         proxies_login, proxies_passowrd)
            conc.submit(self.asyncio_main_ozon, fk_id_user, fk_id_magazin, self.url, link, pool, logger,
                                 proxies,
                                 proxies_login, proxies_passowrd)
            #conc.shutdown(wait=False)
            tovar['error'] = False
            tovar['product'] = False
            # await self.addTovarOzon(fk_id_user, fk_id_magazin, self.url, link, pool, logger, proxies,
            #                                           proxies_login, proxies_passowrd)
            return tovar






