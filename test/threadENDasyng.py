import asyncio
import threading
import time
import concurrent.futures


def privet():
    print("Привет 1. Ждем 10 ссекунд в новом потоке")
    time.sleep(10)
    print('Привет 2. Подождал в новом потоке 10 секунд')
    time.sleep(35)
    print('Привет 3. Подждал 35 секунд в новом потоке.')
    time.sleep(41)
    print('Привет из потока. Ждал 41 секунду. Но ты меня не увидишь если не join или не daemon False')
    a = 0
    b = 1
    try:
        c = b / a
    except ZeroDivisionError as ex:
        print("На ноль делить нельзя")
        print(repr(ex))

    #Генерируем исключение для ThreadPoolExecutor
    raise ZeroDivisionError

async def privet2():
    print('PRIVET от асинхронной функции. Ожидаем 1 секунду')
    await asyncio.sleep(1)
    print("PRIVET 2 от асинхронной функции. Подождал 1 секунду")

async def ura():
    print('ОТЛИЧНО! УРААА от асинхронки')


async def main():
    print("Привет в основном потоке")
    await asyncio.sleep(5) #Блокирующий вызов код дальше не идет. Ждем здесь!
    print('ПРождал 5 секунд в основном потоке, запустил поток')

    #В Потоке ВЫБРОСИТЬ исключение на верх НЕТ ВОЗМОЖНОСТИ ТОЛЬКО В ThreadPoolExecutor
    #t1 = threading.Thread(target=privet, daemon=True) #Поток исполнятся сам по себе, ошибки отловить сложно
    #t1 = threading.Thread(target=privet, daemon=False)
    #Ошибка, здесь не отловить исключение в финале
    #Это не блокирующий вызов и управление перешло в поток
    #Здесь мы ошибку не увидим и не отловим
    # try:
    #     t1.start()
    # except Exception as ex:
    #     print(repr(ex))
    #Нужно отлавливать в самом Потоке все ошибки
    #t1.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(privet) #Теперь идет только вспомогательный поток, основной пойдет потом ВАЖНО!!!
    #Если не обработать будет ошибка и исключение из функции
    try:
        res = future.result()#Это болкирующий вызов и сюда придет в конце ошибка
    except ZeroDivisionError as ex:
        print(repr(ex))

    await asyncio.sleep(30)#Застрял здесь, но основной поток работает сам по себе и продлолжит уведомлять
    print('Еде дождался в основном потоке 30 секунд')
    await privet2()
    print("Привет в основном потоке 2")
    #t1.join()#Блокирующий вызов. Без негопток будет прибит и ого окончание не увидим, т.к. дольше работает чем основной
    await ura()

if __name__ == "__main__":
    asyncio.run(main())
