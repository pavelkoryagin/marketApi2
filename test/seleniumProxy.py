from seleniumwire import webdriver
from selenium.webdriver.common.by import By

proxy_list = ['http://YZWbvc:6crqnT@45.144.170.95:8000', 'http://YZWbvc:6crqnT@45.144.169.118:8000', 'http://YZWbvc:6crqnT@192.109.91.26:8000']


for PROXY in proxy_list:
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        url = 'https://stepik.org/lesson/716118/step/6?unit=716910'

        with webdriver.Chrome(options=chrome_options) as browser:
            browser.get(url)
            text = browser.page_source
            print(text)

            browser.set_page_load_timeout(5)

            proxy_list.remove(PROXY)
    except Exception as _ex:
        print(f"Превышен timeout ожидания для - {PROXY}")
        continue