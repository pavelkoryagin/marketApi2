import os
import random
import asyncio
from urllib.parse import urlparse
import aiohttp
from fake_useragent import UserAgent
#from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import time
from selenium.webdriver.common.by import By

class ParseOzon:
    def __init__(self, pool, logger):
        self.pool = pool
        self.logger = logger
    # def __init__(self):
    #     pass

    async def get_random_chrome_user_agent(self):
        user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
        return user_agent.random


    async def create_driver(self, user_id=1):
        proxies = ['http://YZWbvc:6crqnT@45.144.170.95:8000', 'http://YZWbvc:6crqnT@45.144.169.118:8000', 'http://YZWbvc:6crqnT@192.109.91.26:8000']
        proxy = proxies[random.randint(0,2)]
        proxyAutx = aiohttp.BasicAuth('YZWbvc', '6crqnT')
        options = Options()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_directory = os.path.join(script_dir, 'users')
        user_directory = os.path.join(base_directory, f'user_{user_id}')

        options.add_argument(f'user-data-dir={user_directory}')
        #options.add_argument('--disable-gpu')
        options.add_argument(f'--proxy-server={proxy}')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--no-sandbox')
        # options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)
        userAgent = await self.get_random_chrome_user_agent()
        stealth(driver=driver,
                user_agent=userAgent,
                languages=["ru-RU", "ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                run_on_insecure_origins=True
                )

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
        })
        return driver


    async def parseOzon(self, user_id, url):
        driver = await self.create_driver(user_id)
        #driver.get('https://electrics-kaluga.ru/')
        # time.sleep(3)
        # driver.execute_script("window.scrollBy(0,5000)")
        # time.sleep(5)
        # body = driver.find_element(By.CLASS_NAME, "container").find_element(By.TAG_NAME, "div").text

        #OZON
        driver.get(url)
        #time.sleep(0.5)
        await asyncio.sleep(1)
        #driver.implicitly_wait(0.5)
        driver.execute_script("window.scrollBy(0,5000)")
        #time.sleep(0.5)
        await asyncio.sleep(1)
        #body = driver.find_element(By.CLASS_NAME, "ul_27").find_element(By.TAG_NAME, "span").text
        #body = driver.find_element(By.PARTIAL_LINK_TEXT, "webSale").find_elements(By.TAG_NAME, "span")
        body = driver.find_element(By.TAG_NAME, "body").text
        #page = str(driver.page_source)
        body.encode('utf-8')
        listBody = body.split('₽')
        #print(listBody)
        listZena = listBody[0].split('\n')
        zenaPars = listZena[len(listZena) - 1]
        zena = zenaPars.replace('\u2009', '')
        if zena.isdigit() and zena.isnumeric():
            #print(zena)
            driver.quit()
            return zena
        else:
            self.logger(f'Ошибка при парсинге ОЗОНА. Ссылка - {url}')
            driver.quit()


    async def parseOzonAPSH(self, user_id, url, id, semaphore):
        driver = await self.create_driver(user_id)
        #driver.get('https://electrics-kaluga.ru/')
        # time.sleep(3)
        # driver.execute_script("window.scrollBy(0,5000)")
        # time.sleep(5)
        # body = driver.find_element(By.CLASS_NAME, "container").find_element(By.TAG_NAME, "div").text

        #OZON
        async with semaphore:
            driver.get(url)
            #time.sleep(0.5)
            await asyncio.sleep(1)
            #driver.implicitly_wait(0.5)
            driver.execute_script("window.scrollBy(0,5000)")
            #time.sleep(0.5)
            await asyncio.sleep(1)
            #body = driver.find_element(By.CLASS_NAME, "ul_27").find_element(By.TAG_NAME, "span").text
            #body = driver.find_element(By.PARTIAL_LINK_TEXT, "webSale").find_elements(By.TAG_NAME, "span")
            body = driver.find_element(By.TAG_NAME, "body").text
            #page = str(driver.page_source)
            body.encode('utf-8')
            listBody = body.split('₽')
            #print(listBody)
            listZena = listBody[0].split('\n')
            zenaPars = listZena[len(listZena) - 1]
            zena = zenaPars.replace('\u2009', '')
            if zena.isdigit() and zena.isnumeric():
                #print(zena)
                driver.quit()
                dataZena = {'id': id, 'zena': zena}
                return dataZena
            else:
                self.logger(f'Ошибка при парсинге ОЗОНА. Ссылка - {url}')
                driver.quit()




    # try:
    #     n = listBody.index('c Ozon Картой')
    #     zena = listBody[n - 1].encode('utf-8')
    #     zena.rstrip('₽')
    #     print(zena)
    # except ValueError as valEr:
    #     print(repr(valEr))
    #
    # try:
    #     n = listBody.index('Добавить в корзину')
    # except ValueError as er:
    #     print(repr(er))

# parseOzon = ParseOzon()
# asyncio.run(parseOzon.main_login(1, 'https://www.ozon.ru/product/scarlett-napolnye-vesy-diagnosticheskie-sc-bs33ed110-s-funktsiey-bluetooth-nagruzka-180-kg-tochnost-720721180/?campaignId=521'))
