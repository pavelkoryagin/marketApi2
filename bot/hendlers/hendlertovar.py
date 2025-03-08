from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.state import stateAddTovar
#from bot.db.hendlers.addTovar import addTovarHandler
from bot.entity.tovar import Tovar
from bot.keyboard.buttonTovar import keyboardAddTovar
from bot.db.dbEntity.userDB import UserDb
from bot.db.dbEntity.magazinDB import MagazinDB
from bot.db.dbEntity.tovarDB import TovarDB
import re
from datetime import datetime
from parser.parseWB import ParseWB
from parser.parserOzon import ParseOzon
from bot.db.dbEntity.podpiskaDB import PodpiskaDB

tovarRouter = Router()

@tovarRouter.message(Command(commands='tovaradd'), StateFilter(default_state))
async def message_tovar(message: Message, state: FSMContext):
    await state.set_state(stateAddTovar.stateAddTovar.tovarUrl)
    await message.answer('Для добавления товара пришлите в обратном сообщении ссылку на товар из'
                         'интернет-магазина '
                         '<b><i><a href="https://www.wildberries.ru">Wildberries</a></i></b> или '
                         '<b><i><a href="https://www.ozon.ru">Ozon</a></i></b>.\n'
                         'Для отмены нажмите /stop')


@tovarRouter.callback_query(F.data == 'tovaradd', StateFilter(default_state))
async def calback_tovar(calback: CallbackQuery, state: FSMContext):
    await state.set_state(stateAddTovar.stateAddTovar.tovarUrl)
    await calback.answer()
    await calback.message.answer('Для добавления товара пришлите в обратном сообщении ссылку на товар из'
                         'интернет-магазина '
                         '<b><i><a href="https://www.wildberries.ru">Wildberries</a></i></b> или '
                         '<b><i><a href="https://www.ozon.ru">Ozon</a></i></b>.\n'
                         'Для отмены нажмите /stop')


#В дефолтном состоянии реагируем на кнопку стоп
@tovarRouter.message(Command(commands='stop'), StateFilter(default_state))
async def stop_message_default(message: Message):
    await message.answer('Вы еще ничего не заполнили!')

#В состоянии FSM очищаем данные (Состояние не default)
@tovarRouter.message(Command(commands='stop'), ~StateFilter(default_state))
async def message_stop_clear_add_tovar(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Данные очищены')

#Если прислали товар
@tovarRouter.message(StateFilter(stateAddTovar.stateAddTovar.tovarUrl))
async def addTovar(message: Message, state: FSMContext, pool, logger, proxies: list,
                   proxies_login: str, proxies_password: str):
    await state.update_data(url=message.text)
    user_id = message.from_user.id
    user_dict: dict = dict()
    user_dict[user_id] = await state.get_data()
    url = user_dict[user_id]['url']
    tovarEntity = Tovar(user_id, url)
    tovar = await tovarEntity.addTovar(pool, logger, proxies, proxies_login, proxies_password)
    await state.clear()
    #Если с товаром что-то не так, далее будет понятно что именно
    # if tovar['error'] == False:
    #     #Неправильная ссылка, такой магазин не обслуживаем или ссылка не на товар
    #     if tovar['error_url'] == False:
    #         await message.answer(text='Неверная ссылка на товар! Попробуйте еще нажав на кнопку!.',
    #                              reply_markup=keyboardAddTovar)
    #     #Это уведомления для Озон. Сложно найти наименование товара
    #     if tovar['name'] == False:
    #         await message.answer(text=f'Товар из магазина Озон добавлен. Стоимость - <b>{tovar['total']}.</b>')
    #     else:
    #         #Это уведомление для валдберис
    #         await message.answer(text=f'Товар: "<b>{tovar['name']}</b>" добавлен. Стоимость без скидки - {tovar['basic']} руб., с красным цеником - {tovar['product']} руб.', )
    # else:
    #     #Информируем об ошибке. Такой товар есть, превисили количество допустивых товаров и так далее
    #     await message.answer(tovar['error'])
    if tovar['error'] == True:
        await message.answer(text=tovar['text'], reply_markup=keyboardAddTovar)
    if tovar['error'] == False:
        if tovar['product'] == False: #Значит это товар из озона
            await message.answer(text=f'Товар добавлен в мониторинг! После снижения стоимости, Вы получите'
                                  f' оповешение.', reply_markup=keyboardAddTovar)
        else:
            await message.answer(text=f'Товар {tovar['product']['name']} добавлен в мониторинг.'
                                      f'Стоимость товара - {tovar['product']['product']}',
                                 reply_markup=keyboardAddTovar)
