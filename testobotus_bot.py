import telebot
from telebot import types
from _datetime import datetime

# Основной супер класс
class Chel:
    def __init__(self):
        self.name = ""
        self.age = ""
        self.tel = ""
        self.reg_adr = ""

# объявляем классы пользователей по интересам
class Inv(Chel): # класс инвалидов
    def __init__(self):
        super().__init__()
        self.num_gr = ""
        self.ft = ""
        self.desease_list = ""

    def __str__(self):
        return "Имя: " + self.name + "\nВозраст: " + self.age + "\nГруппа: " + self.num_gr + "\nРегион регистрации: " + self.reg_adr + "\nПервая попытка: " + self.ft + "\nЗаболевания: " + str(self.desease_list) + "\nНомер телефона: " + str(self.tel)

class Voen(Chel): # класс военника
    def __init__(self):
        super().__init__()
        self.status = ""

    def __str__(self):
        return "Имя: " + self.name + "\nКатегория: " + self.status +"\nВозраст: " + self.age + "\nРегион регистрации: " + self.reg_adr + "\nНомер телефона: " + self.tel

class Dip: # класс диплом
    def __init__(self):
        self.name = ""
        self.age = ""
        self.reg_adr = ""
        self.status = ""

    def __str__(self):
        return "Имя: " + self.name + "\nКатегория: " + self.status + "\nВозраст: " + self.age + "\nРегион регистрации: " + self.reg_adr + "\nНомер телефона: " + self.tel

class Pasport: # класс паспорт
    def __init__(self):
        self.name = ""
        self.age = ""
        self.reg_adr = ""
        self.status = ""

    def __str__(self):
        return "Имя: " + self.name + "\nКатегория: " + self.status + "\nВозраст: " + self.age + "\nРегион регистрации: " + self.reg_adr + "\nНомер телефона: " + self.tel

class Another: # класс других
    def __init__(self):
        self.name = ""
        self.age = ""
        self.reg_adr = ""
        self.status = ""

    def __str__(self):
        return "Имя: " + self.name + "\nКатегория: " + self.status + "\nВозраст: " + self.age + "\nРегион регистрации: " + self.reg_adr + "\nНомер телефона: " + self.tel

# объявляем глобальные переменные
name = ""
str_to_bot = ""
active_users = set()

bot = telebot.TeleBot(token='8385780029:AAF3FTM_ZMmTZw90eSVC_py3SqpXG4d4Gbo')

@bot.message_handler(commands=['start'])
def start_message(message):
    active_users.add(message.chat.id)
    bot.send_message(message.chat.id, "Давайте познакомимся для начала. Напишите своё имя:")
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, f"Рад познакомиться, {name}!\nПосмотрите услуги, которые мы предоставляем:")

    markup = types.InlineKeyboardMarkup()
    btn02 = types.InlineKeyboardButton("Инвалидность", callback_data="Инвалидность")
    btn03 = types.InlineKeyboardButton("Военный билет", callback_data="Военный билет")
    btn04 = types.InlineKeyboardButton("Диплом", callback_data="Диплом")
    btn05 = types.InlineKeyboardButton("Паспорт", callback_data="Паспорт")
    btn06 = types.InlineKeyboardButton("Другое...", callback_data="Другое...")
    markup.row(btn02, btn03)
    markup.row(btn04, btn05)
    markup.row(btn06)

    bot.send_message(message.chat.id, "Выберите интересующий документ или нажмите \"Другое...\", если в списке нет того, что Вам нужно", reply_markup=markup)

# создаём функции для обработки кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "Инвалидность":
        user_inv = Inv()
        user_inv.name = name

        bot.send_message(callback.message.chat.id, "Сейчас мы пройдём небольшой опрос, чтобы я мог эффективнее Вам помочь. Какая группа инвалидности Вас интересует?")

        @bot.message_handler(func=lambda message: True)
        def get_numGr(message):
            user_inv.num_gr = message.text.strip()
            bot.send_message(message.chat.id,"Укажите Ваш возраст:")
            bot.register_next_step_handler(message, get_age)

        def get_age(message):
            user_inv.age = message.text.strip()
            bot.send_message(message.chat.id, "Укажите регион регистрации:")
            bot.register_next_step_handler(message, get_regAdr)

        def get_regAdr(message):
            user_inv.reg_adr = message.text.strip()
            bot.send_message(message.chat.id, "Первый раз подаёте на инвалидность?")
            bot.register_next_step_handler(message, get_ft)

        def get_ft(message):
            user_inv.ft = message.text.strip()
            bot.send_message(message.chat.id, "Чем болеете?")
            bot.register_next_step_handler(message, get_deseaseList)

        def get_deseaseList(message):
            user_inv.desease_list = message.text.strip()

            bot.send_message(message.chat.id, "Для оформления понадобятся паспорт, ОМС и СНИЛС.\n И последний вопрос, укажите свой номер телефона, чтобы менеджер мог с Вами связаться:")
            bot.register_next_step_handler(message, get_tel)

        def get_tel(message):
            global str_to_bot
            user_inv.tel = message.text.strip()
            str_to_bot = "Инвалидность:\n"+"Имя: " + user_inv.name + "\nВозраст: " + user_inv.age + "\nГруппа: " + user_inv.num_gr + "\nРегион регистрации: " + user_inv.reg_adr + "\nПервая попытка: " + user_inv.ft + "\nЗаболевания: " + str(user_inv.desease_list) + "\nНомер телефона: " + str(user_inv.tel)
            bot.send_message(chat_id=7410204057, text=str_to_bot)
            bot.send_message(message.chat.id, "Отлично! Ожидайте звонка специалиста.")
            active_users.discard(message.chat.id)
            bot.send_message(message.chat.id, "Диалог завершён.  Начните новый с /start.")

    elif callback.data == "Военный билет":
        user_voen = Voen()
        user_voen.name = name

        bot.send_message(callback.message.chat.id,
                         "Сейчас мы пройдём небольшой опрос, чтобы я мог эффективнее Вам помочь. Какая категория Вас интересует? Напишите негоден/ограничено годен:")

        @bot.message_handler(func=lambda message: True)
        def get_status(message):
            user_voen.status = message.text.strip()
            bot.send_message(message.chat.id,"Укажите Ваш возраст:")
            bot.register_next_step_handler(message, get_age)

        def get_age(message):
            user_voen.age = message.text.strip()
            bot.send_message(message.chat.id, "Укажите регион регистрации:")
            bot.register_next_step_handler(message, get_regAdr)

        def get_regAdr(message):
            user_voen.reg_adr = message.text.strip()
            bot.send_message(message.chat.id, "Укажите свой номер телефона, чтобы менеджер мог с Вами связаться:")
            bot.register_next_step_handler(message, get_tel)

        def get_tel(message):
            global str_to_bot
            user_voen.tel = message.text.strip()
            str_to_bot = "Военный билет:\n"+"Имя: " + user_voen.name + "\nКатегория: " + user_voen.status +"\nВозраст: " + user_voen.age + "\nРегион регистрации: " + user_voen.reg_adr + "\nНомер телефона: " + user_voen.tel
            bot.send_message(chat_id=7410204057, text=str_to_bot)
            bot.send_message(message.chat.id, "Отлично! Ожидайте звонка специалиста.")
            active_users.discard(message.chat.id)
            bot.send_message(message.chat.id, "Диалог завершён.  Начните новый с /start.")

    elif callback.data == "Диплом":
        user_dip = Dip()
        user_dip.name = name

        bot.send_message(callback.message.chat.id,
                         "Сейчас мы пройдём небольшой опрос, чтобы я мог эффективнее Вам помочь.")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn08 = types.KeyboardButton("Поступаю впервые")
        btn09 = types.KeyboardButton("Второе высшее")
        btn10 = types.KeyboardButton("Доучиться")
        btn11 = types.KeyboardButton("Не хватает баллов")
        markup.row(btn08, btn09)
        markup.row(btn10, btn11)

        bot.send_message(callback.message.chat.id,"Выберите категорию, соответствующую Вашему запросу:",
                         reply_markup=markup)

        @bot.message_handler(func=lambda message: True)
        def get_status(message):
            user_dip.status = message.text.strip()
            bot.send_message(message.chat.id,"Укажите Ваш возраст:")
            bot.register_next_step_handler(message, get_age)

        def get_age(message):
            user_dip.age = message.text.strip()
            bot.send_message(message.chat.id, "Укажите регион регистрации:")
            bot.register_next_step_handler(message, get_regAdr)

        def get_regAdr(message):
            user_dip.reg_adr = message.text.strip()
            bot.send_message(message.chat.id, "Укажите свой номер телефона, чтобы менеджер мог с Вами связаться:")
            bot.register_next_step_handler(message, get_tel)

        def get_tel(message):
            global str_to_bot
            user_dip.tel = message.text.strip()
            str_to_bot = "Диплом:\n"+"Имя: " + user_dip.name + "\nКатегория: " + user_dip.status + "\nВозраст: " + user_dip.age + "\nРегион регистрации: " + user_dip.reg_adr + "\nНомер телефона: " + user_dip.tel
            bot.send_message(chat_id=7410204057, text=str_to_bot)
            bot.send_message(message.chat.id, "Отлично! Ожидайте звонка специалиста.")
            active_users.discard(message.chat.id)
            bot.send_message(message.chat.id, "Диалог завершён.  Начните новый с /start.")

    elif callback.data == "Паспорт":
        user_pas = Pasport()
        user_pas.name = name

        bot.send_message(callback.message.chat.id,
                         "Сейчас мы пройдём небольшой опрос, чтобы я мог эффективнее Вам помочь.")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn12 = types.KeyboardButton("Восстановить утерянный паспорт")
        btn13 = types.KeyboardButton("Получить новый, имея паспорт СССР")
        btn14 = types.KeyboardButton("Поменять имя, фамилию")
        btn15 = types.KeyboardButton("Получить гражданство")
        markup.row(btn12, btn13)
        markup.row(btn14, btn15)

        bot.send_message(callback.message.chat.id, "Выберите категорию, соответствующую Вашему запросу:",
                         reply_markup=markup)

        @bot.message_handler(func=lambda message: True)
        def get_status(message):
            user_pas.status = message.text.strip()
            bot.send_message(message.chat.id,"Укажите Ваш возраст:")
            bot.register_next_step_handler(message, get_age)

        def get_age(message):
            user_pas.age = message.text.strip()
            bot.send_message(message.chat.id, "Укажите регион регистрации:")
            bot.register_next_step_handler(message, get_regAdr)

        def get_regAdr(message):
            user_pas.reg_adr = message.text.strip()
            bot.send_message(message.chat.id, "Укажите свой номер телефона, чтобы менеджер мог с Вами связаться:")
            bot.register_next_step_handler(message, get_tel)

        def get_tel(message):
            global str_to_bot
            user_pas.tel = message.text.strip()
            str_to_bot = "Паспорт:\n"+"Имя: " + user_pas.name + "\nКатегория: " + user_pas.status + "\nВозраст: " + user_pas.age + "\nРегион регистрации: " + user_pas.reg_adr + "\nНомер телефона: " + user_pas.tel
            bot.send_message(chat_id=7410204057, text=str_to_bot)
            bot.send_message(message.chat.id, "Отлично! Ожидайте звонка специалиста.")
            active_users.discard(message.chat.id)
            bot.send_message(message.chat.id, "Диалог завершён.  Начните новый с /start.")

    elif callback.data == "Другое...":
        user_other = Another()
        user_other.name = name

        bot.send_message(callback.message.chat.id,
                         "Сейчас мы пройдём небольшой опрос, чтобы я мог эффективнее Вам помочь.")
        bot.send_message(callback.message.chat.id,
                         "Опишите Вашу ситуацию: в восстановлении, получении каких документов Вам требуется помощь?")

        @bot.message_handler(func=lambda message: True)
        def get_status(message):
            user_other.status = message.text.strip()
            bot.send_message(message.chat.id, "Укажите Ваш возраст:")
            bot.register_next_step_handler(message, get_age)

        def get_age(message):
            user_other.age = message.text.strip()
            bot.send_message(message.chat.id, "Укажите регион регистрации:")
            bot.register_next_step_handler(message, get_regAdr)

        def get_regAdr(message):
            user_other.reg_adr = message.text.strip()
            bot.send_message(message.chat.id, "Укажите свой номер телефона, чтобы менеджер мог с Вами связаться:")
            bot.register_next_step_handler(message, get_tel)

        def get_tel(message):
            global str_to_bot
            user_other.tel = message.text.strip()
            str_to_bot = "Другое:\n"+"Имя: " + user_other.name + "\nКатегория: " + user_other.status + "\nВозраст: " + user_other.age + "\nРегион регистрации: " + user_other.reg_adr + "\nНомер телефона: " + user_other.tel
            bot.send_message(chat_id=7410204057, text=str_to_bot)
            bot.send_message(message.chat.id, "Отлично! Ожидайте звонка специалиста.")
            active_users.discard(message.chat.id)
            bot.send_message(message.chat.id, "Диалог завершён.  Начните новый с /start.")


bot.infinity_polling()
