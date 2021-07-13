import random
from config import TOKEN, admin_id
import telebot
from sqlighter import SQLighter

from keyboards import menu, functions

bot = telebot.TeleBot(TOKEN)

# инициализация соединения с БД
db = SQLighter('db/db.db')


def sand_to_admin():
    bot.send_message(chat_id=admin_id, text="bot_started")


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('stickers/static/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.first_name}!\n"
                                      f"Я - бот, созданный для того, чтобы принести кому-то пользу.", reply_markup=menu)


@bot.message_handler(commands=['help'])
def help_me(message):
    text = "Узнать свой id\n /id\n\n"
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['id'])
def get_id(message):
    user_id = message.chat.id
    bot.send_message(message.chat.id, text=f"Ваш id: <b>{user_id}</b>\n", parse_mode='HTML')


# Команда активации подписки
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    if not db.subscriber_exists(message.chat.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.chat.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.chat.id, True)
    bot.send_message(
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# # Команда отписки
# @bot.message_handler(commands=['unsubscribe'])
# def unsubscribe(message):
#     if not db.subscriber_exists(message.chat.id):
#         # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
#         db.add_subscriber(message.from_user.id, False)
#         bot.send_message("Вы итак не подписаны.")
#     else:
#         # если он уже есть, то просто обновляем ему статус подписки
#         db.update_subscription(message.from_user.id, False)
#         bot.send_message("Вы успешно отписаны от рассылки.")


def steam_to_csmoney(message):
    if message.text == 'Вернуться обратно в меню':
        bot.send_message(message.chat.id, 'Вы были перемещены обратно в меню.', reply_markup=menu)
        exit
    # elif message.text == "ТП STEAM → CSMONEY" or "Рандомное число от 0 до 100" or "Продажа в реал → CSMONEY":
    #     bot.send_message(message.chat.id, 'dasd\n', reply_markup=functions)
    else:
        try:
            float(message.text.split()[0])
            float(message.text.split()[1])
            if len(message.text.split()) == 2:
                buy_STEAM = float(message.text.split()[0])
                sell_CSMONEY = float(message.text.split()[1])
                fees = 0.1304347826086956
                if buy_STEAM <= 0 or sell_CSMONEY <= 0:
                    text = "Утихомирьте свой пыл, Вы делаете невозможное."
                    bot.send_message(message.chat.id, text=text)
                    return
                percent_buy_STEAM_to_sell_CSMONEY = (sell_CSMONEY / buy_STEAM - 1) * 100
                if percent_buy_STEAM_to_sell_CSMONEY < 0:
                    text = f"Убыток в % при трейде на CS.M: {round(percent_buy_STEAM_to_sell_CSMONEY, 2)}%\n"
                    bot.send_message(message.chat.id, text=text)
                elif percent_buy_STEAM_to_sell_CSMONEY == 0:
                    text = "Ни убытка, ни профита в этом трейде не присутствует."
                    bot.send_message(message.chat.id, text=text)
                elif percent_buy_STEAM_to_sell_CSMONEY > 0:
                    text = f"Профит в % при трейде на CS.M: {round(percent_buy_STEAM_to_sell_CSMONEY, 2)}%\n"
                    bot.send_message(message.chat.id, text=text)
                    if percent_buy_STEAM_to_sell_CSMONEY > 50:
                        percent_buy_STEAM_to_sell_CSMONEY = 50
                    for percent in range(20, int(percent_buy_STEAM_to_sell_CSMONEY), 5):
                        percent += 5
                        sell_STEAM = sell_CSMONEY / (percent / 100 + 1)
                        profit = (round(sell_STEAM * (1 - fees), 2)) - buy_STEAM
                        try:
                            if profit > 0:
                                text = f"Процент CSMONEY: {percent}\n" \
                                       f"За сколько продать на ТП стима: {round(sell_STEAM, 2)}\n" \
                                       f"Сколько получите с продажи: {round(sell_STEAM * (1 - fees), 2)}\n" \
                                       f"Профит в валюте: {round(profit, 2)}\n" \
                                       f"Профит в %: {round(profit / sell_STEAM, 2) * 100}\n"
                                bot.send_message(message.chat.id, text=text)
                        except:
                            bot.send_message(message.chat.id, text='Профита при продаже на ТП STEAM нет.')
                            break
        except Exception as e:
            bot.send_message(message.chat.id, text='Ошибка, Вы, скорее всего, ввели не два числа.\n'
                                                   'Введите, пожалуйста, в следующий раз два числа.')
            print(repr(e))


# сделать бесконечный цикл для ввода чисел, если неправильные пишет типо дебил неправильно введи два числа,
# а так пока выкидывает в менюшку обратно
# если зашёл в кнопку и жмёшь выйти в меню, пишет сначала ошибку, а со второго раза в меню закидывает уже
# неудобно каждый раз кнопку жать человек говорит
def real_from_csmoney(message):
    if message.text == 'Вернуться обратно в меню':
        bot.send_message(message.chat.id, 'Вы были перемещены обратно в меню.', reply_markup=menu)
        exit
    # elif message.text == "ТП STEAM → CSMONEY" or "Рандомное число от 0 до 100" or "Продажа в реал → CSMONEY":
    #     bot.send_message(message.chat.id, 'dasd\n', reply_markup=functions)
    else:
        try:
            float(message.text.split()[-1])
            float(message.text.split()[-2])
            # это условие скорее всего не нужно, нужно сделать чтобы при вводе "2 3 пав" всё работало
            if len(message.text.split()) >= 2:
                buy_STEAM = float(message.text.split()[0])
                sell_CSMONEY = float(message.text.split()[1])
                if buy_STEAM <= 0 or sell_CSMONEY <= 0:
                    text = "Утихомирьте свой пыл, Вы делаете невозможное."
                    bot.send_message(message.chat.id, text=text)
                    return
                for percent in range(40, 70, 5):
                    percent += 5
                    sell_real = sell_CSMONEY * (percent / 100)
                    profit = sell_real - buy_STEAM
                    profit_percent = (sell_real / buy_STEAM - 1) * 100
                    try:
                        if 0 > profit_percent > -30:
                            bot.send_message(message.chat.id, f'Процент от CSMONEY: {round(percent, 2)}\n'
                                                              f'Ценник в реал: {round(sell_real, 2)}\n'
                                                              f'Убыток в валюте: {round(profit, 2)}\n'
                                                              f'Убыток в процентах: {round(profit_percent, 2)}\n')
                        elif profit_percent >= 0:
                            bot.send_message(message.chat.id, f'Процент от CSMONEY: {round(percent, 2)}\n'
                                                              f'Ценник в реал: {round(sell_real, 2)}\n'
                                                              f'Профит в валюте: {round(profit, 2)}\n'
                                                              f'Профит в процентах: {round(profit_percent, 2)}\n')
                    except:
                        bot.send_message(message.chat.id, text='Профита при продаже на ТП STEAM нет.')
                        break
        except Exception as e:
            bot.send_message(message.chat.id, text='Ошибка, Вы, скорее всего, ввели не два числа.\n'
                                                   'Введите, пожалуйста, в следующий раз два числа.')
            print(repr(e))


@bot.message_handler(content_types='text')
def answer(message):
    if message.text == 'ТП STEAM → CSMONEY':
        bot.send_message(message.chat.id, 'Идея этой функции в том, чтобы узнать под какой % на CSMONEY Вы можете '
                                          'выставить свой предмет на торговую площадку стима, чтобы он отобразился '
                                          'в таблице или каком-нибудь боте и Вам было проще его продать.\n\n'
                                          'Введите за сколько купили скин на ТП STEAM и сколько стоит на CSMONEY: \n'
                                          'Например: 999.99 1499.99, где 999.99 - это за сколько купили на ТП STEAM, '
                                          'а 1499.99 - продажа на CSMONEY.')
        bot.register_next_step_handler(message, steam_to_csmoney)
    elif message.text == 'Продажа в реал → CSMONEY':
        bot.send_message(message.chat.id, 'Идея этой функции в том, чтобы узнать за сколько % от CSMONEY Вы можете '
                                          'продать свой скин в реал, чтобы легче было определить адекватно ли слить '
                                          'скин по такому прайсу.\n\n'
                                          'Введите за сколько купили скин на ТП STEAM и сколько стоит на CSMONEY: \n'
                                          'Например: 999.99 1499.99, где 999.99 - это за сколько купили на ТП STEAM, '
                                          'а 1499.99 - продажа на CSMONEY.')
        bot.register_next_step_handler(message, real_from_csmoney)
    elif message.text == "А что ты умеешь?":
        bot.send_message(message.chat.id,
                         'Не очень-то и много чего, но есть пара-тройка функций. \nЯ пытаюсь активно развиваться!',
                         reply_markup=functions)
    elif message.text == 'Вернуться обратно в меню':
        # переносит в меню отправляя сообщение, с пустым или без сообщения не работает, нужно поправить
        bot.send_message(message.chat.id, 'Вы были перемещены обратно в меню.', reply_markup=menu)
    elif message.text == 'Ссылки на создателя':
        bot.send_message(message.chat.id, 'VK - vk.com/laifodes\n'
                                          'Telegram - @laifodes\n'
                                          'Почта - laifodes@mail.ru\n'
                                          'Instagram - instagram.com/laifodes/\n')
    elif message.text == 'Рандомное число от 0 до 100':
        bot.send_message(message.chat.id, str(random.randint(0, 100)))
    else:
        bot.send_message(message.chat.id, 'Я конечно умный, но на это ответить ещё не способен.')


bot.polling(none_stop=True)
