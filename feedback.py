import telebot
from telebot import types
from config import token
c = 0
c1 = 1
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot(token=token)
data1 = {}
data = {}


@bot.message_handler(content_types=['text'])
def feedback(message):
    global data1
    global data
    global username
    text = message.text
    user = message.chat.id
    if text == "/start":
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(*[types.KeyboardButton(name) for name in ["Создать", "Присоединиться"]])
        msg = bot.send_message(user, "Выберите действие: создать комнату,присоединиться к комнате", reply_markup=keyboard)
        bot.register_next_step_handler(msg, sort)
    elif text == "/continue":
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(*[types.KeyboardButton(name) for name in ["Создать", "Присоединиться"]])
        msg = bot.send_message(user, "Выберите действие: создать комнату,присоединиться к комнате", reply_markup=keyboard)
        bot.register_next_step_handler(msg, sort)
    else:
        bot.register_next_step_handler(bot.send_message(user,
                         "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),feedback)
def sort(message):
    global roomnumber1
    global data1
    global number
    global c1
    text = message.text
    user = message.chat.id
    # if message.content_type!="text":
    #     bot.register_next_step_handler(bot.send_message(user,
    #                                                     "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),
    #                                    sort)
    if text == "Создать":
        # bot.register_next_step_handler(
        # bot.send_message(user, "Если вы хоите создать анонимную комнату формата парковка идей, используйте команду /park. Если хотите создать неанонимную комнату формата LACI, испоьзуйте команду /laci"), choice)
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(*[types.KeyboardButton(name) for name in ["LACI", "Парковка идей"]])
        msg =bot.send_message(user,"Выберите тип комнаты: парковка идей, LACI",reply_markup=keyboard)
        bot.register_next_step_handler(msg,choice)
    elif text == "Присоединиться":
        bot.register_next_step_handler(
            bot.send_message(user, "Введите номер комнаты, к которой вы хотите присоединиться:",reply_markup=types.ReplyKeyboardRemove()), join)
    else:
        bot.register_next_step_handler(bot.send_message(user,
                         "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос ",reply_markup=types.ReplyKeyboardRemove()),sort)
def choice(message):
    text = message.text
    user = message.chat.id
    global c
    global data
    global roomnumber
    global c1
    global data1
    global roomnumber1
    if text == "Парковка идей":
        c += 2
        roomnumber = str(c)
        data.update({roomnumber: {'admin_id': user, "message_id": message.message_id, "плюсы": "*Плюсы: *",
                                  "изменения": "*Изменения:* ", "вопросы": "*Вопросы:*  ",
                                  "общее": "*Идеи по применению:* ","voted":"*Количество проголосовавших: 0*"}})
        bot.send_message(user,
                         "Вот номер вашей комнаты:" + " " + roomnumber + ", " + "сообщите его людям, участвующим в опросе. ",reply_markup=types.ReplyKeyboardRemove())
        s = bot.send_message(user,
                             data[roomnumber]["плюсы"] + "\n" + data[roomnumber]["изменения"] + "\n" + data[roomnumber][
                                 "вопросы"] + "\n" + data[roomnumber]["общее"]+"\n" + data[roomnumber]["voted"], parse_mode="Markdown")
        data[roomnumber]["message_id"] = s.message_id
        data[roomnumber]['admin_id'] = s.chat.id
        bot.send_message(user,"Сообщение выше будет изменяться, когда члены комнаты будут заполнять опрос. Если вы хотите создать или присоединиться к комнате, введите команду /continue")
    elif text == "LACI":
        c1 += 2
        roomnumber1 = str(c1)
        data1.update({roomnumber1: {'admin_id': user, "message_id": message.message_id, "плюсы": "*Новое: *",
                                    "изменения": "*Применение:* ", "вопросы": "*Вызовы:*  ",
                                    "общее": "*Что можно изменить в своей работе:* ","voted":"*Количество проголосовавших: 0*"}})
        bot.send_message(user,
                         "Вот номер вашей комнаты:" + " " + roomnumber1 + ", " + "сообщите его людям, участвующим в опросе. ",reply_markup=types.ReplyKeyboardRemove())
        s1 = bot.send_message(user, data1[roomnumber1]["плюсы"] + " \n" + data1[roomnumber1]["изменения"] + "\n" +
                              data1[roomnumber1]["вопросы"] + "\n" + data1[roomnumber1]["общее"]+ "\n" + data1[roomnumber1]["voted"], parse_mode="Markdown")
        data1[roomnumber1]["message_id"] = s1.message_id
        data1[roomnumber1]['admin_id'] = s1.chat.id
        bot.send_message(user,
        "Сообщение выше будет изменяться, когда члены комнаты будут заполнять опрос. Если вы хотите создать или присоединиться к комнате, введите команду /continue")
    else:
        bot.register_next_step_handler(bot.send_message(user,
                         "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос ",reply_markup=types.ReplyKeyboardRemove()),choice)
def join(message):
    global data1
    global data
    global number
    user = message.chat.id
    text = message.text
    number = str(text)
    if number in data1:
        bot.register_next_step_handler(bot.send_message(user, "Давайте начнем. Что нового вы сегодня узнали?",reply_markup=types.ReplyKeyboardRemove()), likes1)
    elif number in data:
        bot.register_next_step_handler(bot.send_message(user, "Давайте начнем. Что сегодня вам понравилось?",reply_markup=types.ReplyKeyboardRemove()), likes)
    else:
        bot.register_next_step_handler(bot.send_message(user,
                         "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос ",reply_markup=types.ReplyKeyboardRemove()),join)
def likes1(message):
    global data1
    global number
    user = message.chat.id
    if message.content_type!="text":
        bot.register_next_step_handler(bot.send_message(user,
                                                        "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),
                                       likes1)
    text = message.text
    user = message.chat.id
    username = message.from_user.username
    data1[number]["плюсы"] += "\n" + "@" + username + " " + text
    bot.register_next_step_handler(
        bot.send_message(user, "Продолжаем. Скажите, как вы можете применить сегодняшние знания? "), changes1)


def changes1(message):
    global data1
    global number
    user = message.chat.id
    if message.content_type!="text":
        bot.register_next_step_handler(bot.send_message(user,
                                                        "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),
                                       changes1)
    text = message.text
    user = message.chat.id
    username = message.from_user.username
    data1[number]["изменения"] += "\n" + "@" + username + " " + text
    bot.register_next_step_handler(
        bot.send_message(user, "Мы почти закончили! Скажите, с какими препятствиями вы сегодня столкнулись ?"), ques1)


def ques1(message):
    global data1
    global number
    user = message.chat.id
    if message.content_type!="text":
        bot.register_next_step_handler(bot.send_message(user,
                                                        "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),
                                       ques1)
    text = message.text
    user = message.chat.id
    username = message.from_user.username
    data1[number]["вопросы"] += "\n" + "@" + username + " " + text
    bot.register_next_step_handler(bot.send_message(user, "Что бы вы изменили, чтобы работать быстрее?"), general1)


def general1(message):
    global data1
    global number
    user = message.chat.id
    if message.content_type!="text":
        bot.register_next_step_handler(bot.send_message(user,
                                                        "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),
                                       general1)
    text = message.text
    username = message.from_user.username
    data1[number]["общее"] += "\n" + "@" + username + " " + text
    data1[number]["voted"]=data1[number]["voted"].replace(data1[number]["voted"][-2],str(int(data1[number]["voted"][-2])+1))
    bot.edit_message_text(
        data1[number]["плюсы"] + "\n" + "\n" + data1[number]["изменения"] + "\n" + "\n" + data1[number][
            "вопросы"] + "\n" + "\n" + data1[number]["общее"]+ "\n" + "\n" + data1[number]["voted"], data1[number]['admin_id'],
        data1[number]['message_id'], parse_mode="Markdown")
    bot.register_next_step_handler(bot.send_message(user,
                                                    "Спасибо вам за ваше мнение! Создатель комнаты обязательно его прочитает. Чтобы принять участие в еще одном опросе, или создать свой, напишите /continue"),
                                   feedback)


def likes(message):
    global data
    global number
    text = message.text
    user = message.chat.id
    if message.content_type!="text":
        bot.register_next_step_handler(bot.send_message(user,
                                                        "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),
                                       likes)
    data[number]["плюсы"] += "\n" + text
    bot.register_next_step_handler(
        bot.send_message(user, "Продолжаем. Скажите, что сегодня вы хотели бы поменять или улучшить? "), changes)


def changes(message):
    global data
    global number
    text = message.text
    user = message.chat.id
    if message.content_type!="text":
        bot.register_next_step_handler(bot.send_message(user,
                                                        "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),
                                       changes)
    data[number]["изменения"] += "\n" + text
    bot.register_next_step_handler(
        bot.send_message(user, "Мы почти закончили! Скажите, возникли ли у вас сегодня какие-нибудь вопросы ?"), ques)


def ques(message):
    global data
    global number
    text = message.text
    user = message.chat.id
    if message.content_type!="text":
        bot.register_next_step_handler(bot.send_message(user,
                                                        "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),
                                       ques)
    data[number]["вопросы"] += "\n" + text
    bot.register_next_step_handler(
        bot.send_message(user, "Сможете ли вы как-то применить знания, полученные сегодня, и, если да, то как?"),
        general)


def general(message):
    global data
    global number
    text = message.text
    user = message.chat.id
    if message.content_type!="text":
        bot.register_next_step_handler(bot.send_message(user,
                                                        "Мне кажется, вы написали что-то не то. Пожалуйста, повторите запрос "),
                                       general)
    data[number]["общее"] += "\n" + text
    print(data[number]["voted"][-2])
    data[number]["voted"]=data[number]["voted"].replace(data[number]["voted"][-2],str(int(data[number]["voted"][-2]) + 1))
    print(data[number]["voted"][-2])
    bot.edit_message_text(data[number]["плюсы"] + "\n" + "\n" + data[number]["изменения"] + "\n" + "\n" + data[number][
        "вопросы"] + "\n" + "\n" + data[number]["общее"]+ "\n" + "\n" + data[number]["voted"], data[number]['admin_id'], data[number]['message_id'],
                          parse_mode="Markdown")
    bot.register_next_step_handler(bot.send_message(user,
                                                    "Спасибо вам за ваше мнение! Создатель комнаты обязательно его прочитает. Чтобы принять участие в еще одном опросе, или создать свой, напишите /continue"),
                                   feedback)

bot.polling(none_stop=True)
