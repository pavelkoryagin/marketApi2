# import requests
#
# url = 'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=123585567&spp=30&ab_testing=false&nm=124368667'
# #url = 'https://www.wildberries.ru/catalog/232826827/detail.aspx'
#
# headers = {
#     'Content-type': 'application/json',
#     'x-requested-with': 'XMLHttpRequest',
#     'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.706 YaBrowser/24.10.2.706 Yowser/2.5 Safari/537.36'
# }
#
# response = requests.get(url, headers=headers)
# response.encoding = 'utf-8'
# if response.status_code == 200:
#     data = response.json()
#     #print(data['data']['products'][1]['sizes'][0]['price'])
#     print(int(data['data']['products'][0]['sizes'][0]['price']['product'])/100)
#     # print(response.text)
#     # print(response.cookies)
#     # print(response.headers)





# import aiohttp
# import asyncio
#
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
# url = 'https://www.wildberries.ru/catalog/80012708/detail.aspx'
# data = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}
#
# async def main():
#     async with aiohttp.ClientSession(trust_env=True) as session:
#         async with session.get(url=url, headers=headers, timeout=1, params=data) as response:
#             print(await response.text())
#
#
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(main())




# import time
# from random import randint
# from fake_useragent import UserAgent
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.os_manager import ChromeType
# from selenium.webdriver.chrome.service import Service as ChromiumService
# from selenium.webdriver.common.by import By
#
# user = UserAgent()
# options = webdriver.ChromeOptions()
# options.add_argument(f'user-agent={user.random}')
# options.add_argument("-disable-blink-features=AutomationControlled")
# with webdriver.Chrome(options=options, service=ChromiumService(ChromeDriverManager().install())) as driver:
#     driver.get("https://www.ozon.ru/product/yandeks-televizor-tv-stantsiya-beysik-s-alisoy-43-4k-uhd-chernyy-1720788364/?avtc=1&avte=4&avts=1733596659&sh=lukn3qHWsw")
#     time.sleep(5)
#     driver.execute_script("windows.scrollTo(5,4000);")
#     time.sleep(10)
#     # body = driver.find_element(By.CSS_SELECTOR, '.sm7_27 .s7m_27 .mt1_27')
#     # print(body.text)




# import os
# from fake_useragent import UserAgent
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium_stealth import stealth
# import time
#
#
# def get_random_chrome_user_agent():
#     user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
#     return user_agent.random
#
#
# def create_driver(user_id=1):
#     options = Options()
#     options.add_argument("start-maximized")
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option('useAutomationExtension', False)
#
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     base_directory = os.path.join(script_dir, 'users')
#     user_directory = os.path.join(base_directory, f'user_{user_id}')
#
#     options.add_argument(f'user-data-dir={user_directory}')
#     #options.add_argument('--disable-gpu')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument("--disable-notifications")
#     options.add_argument("--disable-popup-blocking")
#     options.add_argument('--no-sandbox')
#     # options.add_argument('--headless')
#
#     driver = webdriver.Chrome(options=options)
#     ua = get_random_chrome_user_agent()
#     stealth(driver=driver,
#             user_agent=ua,
#             languages=["ru-RU", "ru"],
#             vendor="Google Inc.",
#             platform="Win64",
#             webgl_vendor="Intel Inc.",
#             renderer="Intel Iris OpenGL Engine",
#             fix_hairline=True,
#             run_on_insecure_origins=True
#             )
#
#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         'source': '''
#             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
#             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
#             delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
#       '''
#     })
#     return driver
#
#
# def main_login(user_id=1):
#     driver = create_driver(user_id)
#     driver.get('https://www.ozon.ru/product/yandeks-televizor-tv-stantsiya-beysik-s-alisoy-43-4k-uhd-chernyy-1720788364/?avtc=1&avte=4&avts=1733596659&sh=lukn3qHWsw')
#     time.sleep(350)
#     driver.quit()
#
# main_login(user_id=1)



# url = 'https://stepik.org/course/104774'
# options = webdriver.ChromeOptions()
# options.add_extension('1.1.8_0.crx')
#
# driver = webdriver.Chrome("/chromedriver-win64/chromedriver")
# driver.get(url)
# driver.implicitly_wait(0.5)
# time.sleep(3)


# from seleniumbase import Driver
# import time
#
# driver = Driver(uc_cdp=True, incognito=True)
# driver.get("https://antoinevastel.com/bots/datadome")
# time.sleep(50)
# driver.quit()

# from urllib.request import urlopen
# url = 'https://www.ozon.ru/product/yandeks-televizor-tv-stantsiya-beysik-s-alisoy-43-4k-uhd-chernyy-1720788364/?avtc=1&avte=4&avts=1733596659&sh=lukn3qHWsw'
# response = urlopen(url)
# print(response.read().decode('utf-8'))
# from urllib.parse import urlparse
# url = "https://www.example.com/search?q=python&amp;lang=en"
# parsed_url = urlparse(url)
# print(parsed_url)



