import random

from aiogram.types import Message

from config import admin_id
from keyboards import menu, functions
from main import bot, dp, anti_flood
from sqlite import SQLight

db = SQLight('db.db')

async def sand_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="bot_started")


@dp.message_handler(commands=['start'])
async def welcome(message: Message):
    # await bot.send_sticker(message.from_user.id, )
    await bot.send_message(message.from_user.id, f'Добро пожаловать, {message.from_user.first_name}!\n'
                                                 f'Я - бот созданный каким-то бл*ть дебилом Станиславом чтобы меня тестировали.', reply_markup=menu)


@dp.message_handler(commands=['help'])
async def help_me(message: Message):
    text = "Узнать свой id\n /id\n\n"
    await bot.send_message(message.from_user.id, text=text)


@dp.message_handler(commands=['id'])
async def get_id(message: Message):
    user_id = message.from_user.id
    await bot.send_message(message.from_user.id, text=f"Ваш id: <b>{user_id}</b>\n")


@dp.message_handler(content_types=['text'])
@dp.throttled(anti_flood, rate=1)
async def communication(message: Message):
    if message.text == 'Процент ТП STEAM → CSMONEY':
        numbers = set
        # await bot.send_message(message.from_user.id,
        #                        text='Идея этой функции в том, чтобы узнать под какой % на CSMONEY Вы можете '
        #                             'выставить свой предмет на торговую площадку стима, чтобы '
        #                             'он отобразился в таблице или каком-нибудь боте и Вам было проще его продать.\n\n'
        #                             'Введите за сколько купили скин на ТП STEAM и сколько стоит на CS_MONEY: \n'
        #                             'Например: 999.99 1499.99, где 999.99 - это за сколько купили на ТП STEAM, '
        #                             'а 1499.99 - продажа на CSMONEY.')
    # нужно поправить, ибо без этого условия ничего не работает
        await message.answer('Идея этой функции в том, чтобы узнать под какой % на CSMONEY Вы можете '
                                    'выставить свой предмет на торговую площадку стима, чтобы '
                                    'он отобразился в таблице или каком-нибудь боте и Вам было проще его продать.\n\n'
                                    'Введите за сколько купили скин на ТП STEAM и сколько стоит на CS_MONEY: \n'
                                    'Например: 999.99 1499.99, где 999.99 - это за сколько купили на ТП STEAM, '
                                    'а 1499.99 - продажа на CSMONEY.')
        print('Мы тут')
        if message.text != 'Процент ТП STEAM → CSMONEY':
            try:
                print("а сейчас тут")
                float(message.text.split()[-1])
                float(message.text.split()[-2])
                # g[f'{message.from_user.id}'] = float(g[f'{message.from_user.id}'])
                if len(message.text.split()) == 2:
                    print("неужели и тут")
                    buy_STEAM = float(message.text.split()[0])
                    sell_CSMONEY = float(message.text.split()[1])
                    fees = 0.1304347826086956
                    # if buy_STEAM < 0 or sell_CSMONEY < 0:
                    #     text = f"Утихомирьте свой пыл, Вы делаете невозможное."
                    #     await bot.send_message(message.from_user.id, text=text)
                    percent_buy_STEAM_to_sell_CSMONEY = (sell_CSMONEY / buy_STEAM - 1) * 100
                    if percent_buy_STEAM_to_sell_CSMONEY < 0:
                        text = f"Убыток в % при трейде на CS.M: {round(percent_buy_STEAM_to_sell_CSMONEY, 2)}%\n"
                        await bot.send_message(message.from_user.id, text=text)
                    elif percent_buy_STEAM_to_sell_CSMONEY == 0:
                        text = "Ни убытка, ни профита в этом трейде не присутствует."
                        await bot.send_message(message.from_user.id, text=text)
                    elif percent_buy_STEAM_to_sell_CSMONEY > 0:
                        text = f"Профит в % при трейде на CS.M: {round(percent_buy_STEAM_to_sell_CSMONEY, 2)}%\n"
                        await bot.send_message(message.from_user.id, text=text)
                        if percent_buy_STEAM_to_sell_CSMONEY > 50:
                            percent_buy_STEAM_to_sell_CSMONEY = 50
                        for percent in range(15, int(percent_buy_STEAM_to_sell_CSMONEY), 5):
                            percent += 5
                            sell_STEAM = sell_CSMONEY / (percent / 100 + 1)
                            profit = (round(sell_STEAM * (1 - fees), 2)) - buy_STEAM
                            try:
                                if (profit > 0):
                                    text = f"Процент CSMONEY: {percent}\n" \
                                           f"За сколько продать на ТП стима: {round(sell_STEAM, 2)}\n" \
                                           f"Сколько получите с продажи: {round(sell_STEAM * (1 - fees), 2)}\n" \
                                           f"Профит в валюте: {round(profit, 2)}\n" \
                                           f"Профит в %: {round(profit / sell_STEAM, 3)}\n"
                                    await bot.send_message(message.from_user.id, text=text)
                            except:
                                await bot.send_message(message.from_user.id,
                                                       text='Профита при продаже на ТП STEAM нет.')
                                break
                else:
                    await bot.send_message(message.from_user.id, text='Введите, пожалуйста, два числа.')
            except Exception as e:
                print(repr(e))
        else:
            numbers.add(message.text)
    elif message.text == "А что ты умеешь?":
        await bot.send_message(message.from_user.id, 'Не очень-то и много чего, но есть парочка функций. \nЯ пытаюсь активно развиваться!', reply_markup=functions)
    elif message.text == 'Вернуться обратно в меню':
        # переносит в меню отправляя сообщение, с пустым или без сообщения не работает, нужно поправить
        await bot.send_message(message.from_user.id, 'Вы были перемещены обратно в меню.', reply_markup=menu)
    elif message.text == 'Ссылки на создателя':
        await bot.send_message(message.from_user.id, 'VK - vk.com/laifodes\n'
                                                     'Telegram - @laifodes\n'
                                                     'Почта - laifodes@mail.ru\n'
                                                     'Instagram - instagram.com/laifodes/\n')
    elif message.text == 'Рандомное число от 0 до 100':
        await bot.send_message(message.from_user.id, str(random.randint(0, 100)))