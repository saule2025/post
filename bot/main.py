# Подключаем модуль случайных чисел 
import random
# Подключаем модуль для Телеграма
import telegram
import telebot
# Импорт модуля Psycopg2 в программу
import psycopg2
import os
# С помощью класса Error можно обрабатывать любые ошибки и исключения базы данных
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# Подключаем модуль для работы с датой/веременем
from datetime import datetime
# Функция для преобразования объектов datetime с использованием часовых поясов.
#import pytz
#local_tz = pytz.timezone('Asia/Almaty')
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types
# Для определения имени пользователя
import getpass
# QR Code
#from pyzbar.pyzbar import decode
#from PIL import Image
#import cv2 
#import numpy 
from telegram.constants import ParseMode

# Проверка адреса электронной почты
from validate_email import validate_email
# Для отправки электронной почты
# https://www.courier.com/blog/three-ways-to-send-emails-using-python-with-code-tutorials/
import smtplib 

# Указываем токен
API_TOKEN = '5185625280:AAHa8qoy8CRENooYDRBOCwE5ykoIkTpIDcI'
bot = telebot.TeleBot(API_TOKEN)
# Текст приглашения
welcome_message = "Бот предназначен для поиска почтовых отправлений по трек-номеру или номеру телефона"

# Строка соединения (Connecion string)
database_name="d98ui5eq2lp29a"
#database_name="post"

"""
def get_connection_string():
    cs = psycopg2.connect("postgres://dhayvxvdlspbzy:cd27da59cf5fef16b9ceeddf205a5c5301458c6380df72e157924d2a675414f1@ec2-44-194-92-192.compute-1.amazonaws.com:5432/d98ui5eq2lp29a", sslmode="require")
    return cs

def get_connection_string2():
    cs = psycopg2.connect("postgres://dhayvxvdlspbzy:cd27da59cf5fef16b9ceeddf205a5c5301458c6380df72e157924d2a675414f1@ec2-44-194-92-192.compute-1.amazonaws.com:5432/d98ui5eq2lp29a", sslmode="require")
    return cs
"""

def get_connection_string():
    print("get_connection_string")
    cs = psycopg2.connect(user="postgres",
                            password="3552998",
                            host="127.0.0.1",
                            port="5433",
                            database="post")
    return cs

def get_connection_string2():
    print("get_connection_string2")
    cs = psycopg2.connect(user="postgres",
                            password="3552998",
                            host="127.0.0.1",
                            port="5433")
    return cs


# Метод, который получает сообщения и обрабатывает их
#@bot.message_handler(content_types=['text'])
# Пользователь клиент
class Customer:
    def __init__(self, id, telegram_id, phone_number, first_name, last_name, email):
        self.id = id
        self.telegram_id = telegram_id
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        
# Страна
class Country:
    def __init__(self, title):
        self.title = title

# Статус
class Status:
    def __init__(self, title):
        self.title = title

#  Посылка (почтовое отправление)
class Package:
    def __init__(self, track_number, dates, sender_country, sender_address, sender_name, recipient_country, recipient_address, recipient_name, recipient_phone):
        self.track_number = track_number
        self.dates = dates
        self.sender_country = sender_country
        self.sender_address = sender_address
        self.sender_name = sender_name
        self.recipient_country = recipient_country
        self.recipient_address = recipient_address
        self.recipient_name = recipient_name
        self.recipient_phone = recipient_phone

# Перемещение посылки
class Movement:
    def __init__(self, package, datem, status, details):
        self.package = package
        self.datem = datem
        self.status = status
        self.details = details        

# Посылка (почтовое отправление) 
class ViewPackage:
    def __init__(self, track_number, dates, sender_country_id, sender_country, sender_address, sender_name, recipient_country_id, recipient_country, recipient_address, recipient_name, recipient_phone, final):
        self.track_number = track_number
        self.dates = dates
        self.sender_country_id = sender_country_id
        self.sender_country = sender_country
        self.sender_address = sender_address
        self.sender_name = sender_name
        self.recipient_country_id = recipient_country_id
        self.recipient_country = recipient_country
        self.recipient_address = recipient_address
        self.recipient_name = recipient_name
        self.recipient_phone = recipient_phone
        self.final = final

# Создание базы данных 
try:
    # Подключение к PostgreSQL 
    conn = get_connection_string2()
    # Транзакция в режиме «autocommit» (автофиксация), то есть каждый оператор выполняется в своей отдельной транзакции, которая неявно фиксируется в конце оператора
    # (если оператор был выполнен успешно; в противном случае транзакция откатывается).
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)    
    # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
    # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                     
    cursor = conn.cursor()
    # Проверка наличия базы данных
    cursor.execute("SELECT * FROM pg_database WHERE datname = '" + database_name + "'")
    result = cursor.fetchall()
    if len(result) > 0:
        print("База данных уже существует")        
    else:
        cursor.execute("CREATE DATABASE " + database_name)
        print("База данных создана")        
    # Закрыть объект cursor после завершения работы.
    cursor.close()
    # Закрыть соединение после завершения работы.
    conn.close()
    # Подключение к PostgreSQL 
    conn = get_connection_string()
    # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
    # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                     
    cursor = conn.cursor()
    # Проверка наличия таблицы клиентов
    cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'customer'")
    result = cursor.fetchall()
    if len(result) > 0:
        print("Таблица клиентов уже существует")        
    else:
        create_table_query = '''CREATE TABLE "customer" (
            "id"	integer NOT NULL,
            "telegram_id"	integer NOT NULL,
            "phone_number"	varchar(20) NOT NULL,
            "email"	        varchar(128),
            "first_name"	varchar(64) NOT NULL,
            "last_name"	varchar(64),
            PRIMARY KEY("id" AUTOINCREMENT) );'''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)
        conn.commit()
        print("Таблица клиентов создана")        
    # Проверка наличия таблицы Страна
    cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'country'")
    result = cursor.fetchall()
    if len(result) > 0:
        print("Таблица Страна уже существует")        
    else:
        create_table_query = '''CREATE TABLE country(
            id bigint NOT NULL DEFAULT nextval('country_id_seq'::regclass),
            title character varying(196) COLLATE pg_catalog."default" NOT NULL,
            CONSTRAINT country_pkey PRIMARY KEY (id),
            CONSTRAINT country_title_key UNIQUE (title)
            )'''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)
        conn.commit()
        print("Таблица Страна создана")
    # Проверка наличия таблицы Статус
    cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'status'")
    result = cursor.fetchall()
    if len(result) > 0:
        print("Таблица Статус уже существует")        
    else:
        create_table_query = '''CREATE TABLE status(
            id bigint NOT NULL DEFAULT nextval('status_id_seq'::regclass),
            title character varying(196) COLLATE pg_catalog."default" NOT NULL,
            CONSTRAINT status_pkey PRIMARY KEY (id),
            CONSTRAINT status_title_key UNIQUE (title)
            )'''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)
        conn.commit()
        print("Таблица Статус создана")         
    # Проверка наличия таблицы Посылка (почтовое отправление)
    cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'package'")
    result = cursor.fetchall()
    if len(result) > 0:
        print("Таблица Посылка (почтовое отправление) уже существует")        
    else:
        create_table_query = '''CREATE TABLE "package"(
            id bigint NOT NULL DEFAULT nextval('package_id_seq'::regclass),
            track_number character varying(13) COLLATE pg_catalog."default" NOT NULL,
            dates timestamp with time zone NOT NULL,
            sender_address character varying(192) COLLATE pg_catalog."default" NOT NULL,
            sender_name character varying(192) COLLATE pg_catalog."default" NOT NULL,
            recipient_address character varying(192) COLLATE pg_catalog."default" NOT NULL,
            recipient_name character varying(192) COLLATE pg_catalog."default" NOT NULL,
            recipient_phone character varying(64) COLLATE pg_catalog."default",
            recipient_country_id bigint NOT NULL,
            sender_country_id bigint NOT NULL,
            CONSTRAINT package_pkey PRIMARY KEY (id),
            CONSTRAINT package_track_number_key UNIQUE (track_number),
            CONSTRAINT package_recipient_country_id_d4ce20f4_fk_country_id FOREIGN KEY (recipient_country_id)
                REFERENCES public.country (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT package_sender_country_id_9b38d103_fk_country_id FOREIGN KEY (sender_country_id)
                REFERENCES public.country (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                DEFERRABLE INITIALLY DEFERRED)'''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)
        conn.commit()
        print("Таблица Посылка (почтовое отправление) создана")        
    # Проверка наличия таблицы Перемещение посылки
    cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'movement'")
    result = cursor.fetchall()
    if len(result) > 0:
        print("Таблица Перемещение посылки уже существует")        
    else:
        create_table_query = '''CREATE TABLE movement(
            id bigint NOT NULL DEFAULT nextval('movement_id_seq'::regclass),
            datem timestamp with time zone NOT NULL,
            details text COLLATE pg_catalog."default",
            package_id bigint NOT NULL,
            status_id bigint NOT NULL,
            CONSTRAINT movement_pkey PRIMARY KEY (id),
            CONSTRAINT movement_package_id_1674c3b0_fk_package_id FOREIGN KEY (package_id)
                REFERENCES public."package" (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT movement_status_id_0e3fb70a_fk_status_id FOREIGN KEY (status_id)
                REFERENCES public.status (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                DEFERRABLE INITIALLY DEFERRED)'''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)
        conn.commit()
        print("Таблица Перемещение посылки создана")        
except (Exception, Error) as error:
    print(error)    

# Проверка наличия пользовтаеля Telegram (telegram_id) в базе данных пользователей
def check_telegram_id(telegram_id):
    print("check_telegram_id")        
    try:
        # Подключение к PostgreSQL 
        conn = get_connection_string()
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                     
        cursor = conn.cursor()
        # SQL-запрос
        sql = "SELECT id, telegram_id, phone_number, first_name, last_name, email FROM customer WHERE telegram_id=" + str(telegram_id)
        #print(sql)
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если такого пользователя нет то вернуть false если есть то true
        if row is None:
            exists = False
        else:
            global customer  
            customer = Customer(row[0], row[1], row[2], row[3], row[4], row[5])
            exists = True
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        print("exists ", exists)
        return exists
    except (Exception, Error) as error:
        print("check_telegram_id: ",error)        

# Проверка наличия пользовтаеля Telegram (phone_number) в базе данных пользователей
def check_phone_number(phone_number):
    print("check_phone_number")
    try:
        # Проверить, есть ли такой пользователь в базе данных
        # Подключение к PostgreSQL 
        conn = get_connection_string()
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                     
        cursor = conn.cursor()
        # SQL-запрос
        sql = "SELECT id, telegram_id, phone_number, first_name, last_name, email FROM customer WHERE phone_number='" + phone_number + "'"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если такого пользователя нет то вернуть false если есть то true
        if row is None:
            exists = False
        else:
            # Пользователь
            global customer  
            customer = customer(row[0], row[1], row[2], row[3], row[4], row[5])
            exists = True
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        return exists
    except (Exception, Error) as error:
        print(error)        

# Добавление пользователя
def add_customer():
    print("add_customer")
    try:
        if customer.last_name is not None:
            sql = "INSERT INTO customer (telegram_id, phone_number, first_name, last_name, email) VALUES (" + str(customer.telegram_id) +", '" + customer.phone_number +"', '" + customer.first_name +"', '" + customer.last_name + "', '" + customer.email +"') "
        else:
            sql = "INSERT INTO customer (telegram_id, phone_number, first_name, last_name, email) VALUES (" + str(customer.telegram_id) +", '" + customer.phone_number +"', '" + customer.first_name +"', '', '" + customer.email +"') "
        print(sql)
        # Подключение к PostgreSQL 
        conn = get_connection_string()
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                     
        cursor = conn.cursor() 
        cursor.execute(sql)
        conn.commit()        
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        print("Пользователь добавлен")
        # Обновить экземпляр класа Customer (ролучить id таблицы Customer)
        check_telegram_id(customer.telegram_id)
        #print(customer.id)
        #print(customer.telegram_id)
        #print(customer.phone_number)
        #print(customer.first_name)
        #print(customer.last_name)
    except (Exception, Error) as error:
        print(error)
        bot.reply_to(message, 'упс')
          
# Запись/проверка контакта в БД
@bot.message_handler(content_types=['contact']) #Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :) 
def contact(message):
    print("contact")
    try:
        # Пользователь
        global customer        
        # print(message.contact) Выводим в панели контактные данные
        print(message.contact.user_id)
        print(message.contact.phone_number)
        print(message.contact.first_name)
        print(message.contact.last_name)
        print(message.contact.user_id)
        if message.contact.last_name is None:
            customer = Customer(None, message.contact.user_id, message.contact.phone_number, message.contact.first_name, None, None)
        else:
            customer = Customer(None, message.contact.user_id, message.contact.phone_number, message.contact.first_name, message.contact.last_name, None)
        # Проверить, есть ли такой пользователь в базе данных, если нет то добавить
        if check_telegram_id(customer.telegram_id):
            print("Пользователь существует")
            # Подключаем клавиатуру
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            # Указываем название кнопок, добавляем клавиатуру
            markup.add('Найти по трек-номеру').add('Найти по номеру телефона').row('История по трек-номеру')
            # Стартовое сообщение
            msg = bot.reply_to(message, '\nЧто Вы хотите сделать?', reply_markup=markup)
            # Выбор действия 
            bot.register_next_step_handler(msg, menu) 
        else:
            print("Необходимо добавить пользователя")
            message = bot.reply_to(message, "Введите адрес электронной почты")
            bot.register_next_step_handler(message, get_email)            
                  
             
    except Exception as error:
        print(error)
        bot.reply_to(message, 'упс')

# Получение email
def get_email(message):
    print("get_email ", message.text)
    # Проверка чтобы только цифры или знак    
    while True:
        try:
            # Проверка адреса электронной почты
            #is_valid = validate_email(message.text, verify=True)
            is_valid = validate_email(message.text)
            if is_valid == False:
                # Генерация исключительной ситуации
                raise Exception("Ошибка")
            # email
            customer.email = message.text
            # Добавить пользователя   
            add_customer()
            # Подключаем клавиатуру
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            # Указываем название кнопок, добавляем клавиатуру
            markup.add('Найти по трек-номеру').add('Найти по номеру телефона').row('История по трек-номеру')
            # Стартовое сообщение
            msg = bot.reply_to(message, '\nЧто Вы хотите сделать?', reply_markup=markup)
            # Выбор действия 
            bot.register_next_step_handler(msg, menu)   
        except:
            print("Необходимо ввести действующий адрес электронной почты")
            bot.send_message(message.chat.id,"Необходимо ввести действующий адрес электронной почты")
            bot.register_next_step_handler(message, get_email)            
        finally:
            break

# Декоратор @message_handler реагирует на входящие сообщение.
@bot.message_handler(content_types=['text'])
def send_welcome(message):
    print("send_welcome")
    try:
        # Проверить, есть ли такой пользователь в базе данных, если нет то предложить отправить контакт и добавить его
        if check_telegram_id(message.chat.id):
            #print("Пользователь существует")
            # print(message.contact) Выводим в панели контактные данные
            # customer = Customer(message.contact.telegram_id, message.contact.phone_number, message.contact.first_name, message.contact.last_name)
            # Подключаем клавиатуру
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            # Указываем название кнопок, добавляем клавиатуру
            markup.add('Найти по трек-номеру').add('Найти по номеру телефона').row('История по трек-номеру')
            # Выбор действия 
            bot.register_next_step_handler(message, menu)
            bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
        else:
            #print("Пользователя не существует")
            # Подключаем клавиатуру
            keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
            # Указываем название кнопки, которая появится у пользователя
            contact_button = types.KeyboardButton(text="Отправить контакт", request_contact=True)
            # Добавляем эту кнопку
            keyboard.add(contact_button)
            bot.send_message(message.chat.id, welcome_message + "\nНажмите на кнопку \"Отправить контакт\" отправьте свои номер телефона (при оплате поездки необходимая сумма будет списана с этого номера).", reply_markup=keyboard)
    except Exception as error:
        print(error)
        bot.reply_to(message, str(error))
    
def menu(message):
    print("menu")
    #print(message.chat.id)
    try:
        if (message.text == u'Найти по трек-номеру'):
            # Запросить трек-номер
            message = bot.reply_to(message, """Введите трек-номер полностью (13 символов)""")
            bot.register_next_step_handler(message, get_track_number, 1) 
        elif (message.text == u'Найти по номеру телефона'):
            # Последнее движение по номеру телефона
            #print(customer.phone_number)
            movement_final2(message)    
        elif (message.text == u'История по трек-номеру'):
            # Запросить трек-номер
            message = bot.reply_to(message, """Введите трек-номер полностью (13 символов)""")
            bot.register_next_step_handler(message, get_track_number, 2) 
    except Exception as error:
        print(error)
        bot.reply_to(message, str(error))

# Получить Номер трека
def get_track_number(message, mode):
    print("get_track_number")
    track_number = message.text
    print(track_number)
    # Проверка длины тек-номера
    if len(track_number) == 13:                
        # Последнее движение по номеру трека
        if mode == 1:
            movement_final1(message)        
        # История по трек-номеру
        elif mode == 2:
            history(message)        
    else:
        print('Введите номер-трека полностью (13 символов)')
        bot.send_message(message.chat.id, 'Введите номер-трека полностью (13 символов)')
        bot.register_next_step_handler(message, get_track_number)    

# Последнее движение по номеру трека
def movement_final1(message):
    print("movement_final1")
    track_number = message.text
    #print(track_number)
    try:
        # Подключение к PostgreSQL 
        conn = get_connection_string()
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                     
        cursor = conn.cursor()
        sql = "SELECT track_number, \"final\" "
        sql = sql + "FROM view_package "
        sql = sql + "WHERE track_number='" + track_number + "'"
        #print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        if cursor.rowcount <= 0:
            bot.send_message(message.chat.id,  "<b>Трек-номер:</b> " + track_number + ". Информации о местоположении посылки пока нет. После отправки посылки может пройти несколько дней, прежде чем она начнет отслеживаться. ", parse_mode='HTML' )                
        else:
            for row in results:
                bot.send_message(message.chat.id,  "<b>Трек-номер:</b> " + str(row[0]) +  "\n<b>Последнее движение:</b> " + str(row[1]), parse_mode='HTML' )
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        send_welcome(message)
    except Exception as error:
        print(error)
        bot.reply_to(message, 'упс')       


# Последнее движение по номеру телефона
def movement_final2(message):
    print("movement_final2")
    recipient_phone = customer.phone_number
    # Убрать в телефоне плюс
    if recipient_phone[0]!='+':
        recipient_phone = "+" + recipient_phone        
    print(recipient_phone)
    #print(track_number)
    try:
        # Подключение к PostgreSQL 
        conn = get_connection_string()
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                     
        cursor = conn.cursor()
        sql = "SELECT track_number, recipient_phone, \"final\", dates, sender_country || ', ' || sender_address  || ', ' || sender_name AS sender, recipient_country || ', ' ||  recipient_address || ', ' ||  recipient_name "
        sql = sql + "FROM view_package "
        sql = sql + "WHERE recipient_phone='" + recipient_phone + "'"
        #print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            bot.send_message(message.chat.id,  "<b>Трек-номер:</b> " + str(row[0])  +  "\n<b>Телефон:</b> " + str(row[1]) +  "\n<b>Последнее движение:</b> " + str(row[2])  , parse_mode='HTML' )
            send_email(str(row[0]), "Трек-номер " + str(row[0]) +  "\nНомер телефона: " + str(row[1]) + "\nОткуда: " + str(row[4]) + "\nКуда: " + str(row[5]) + "\nПоследнее движение: " + str(row[2]))
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        send_welcome(message)
    except Exception as error:
        print(error)
        bot.reply_to(message, 'упс')       

# Отправка по адресу электронной почты
def send_email(sub, mess):
    print("send_email")
    try:
        HOST = "smtp.mail.ru"
        # От кого (пароль для внешних приложений)
        FROM = "post130322@mail.ru"
        PASSWORD = "hiLrs7E7FsxAUsKCSafG"
        # Кому
        TO = "user538542@mail.ru"
        # Тема
        #SUBJECT = "Тема"
        SUBJECT = sub
        #Create your SMTP session 
        smtp = smtplib.SMTP(HOST, 25) 
        #Use TLS to add security 
        smtp.starttls() 
        #User Authentication - Пароль для внешних приложений
        smtp.login(FROM, PASSWORD)
        #Defining The Message 
        #message = "Сообщение" 
        # Тело письма
        BODY = "\r\n".join((
            "From: %s" % FROM,
            "To: %s" % TO,
            "Subject: %s" % SUBJECT ,
            "",
            mess
        ))
        BODY = BODY.encode('utf-8')
        #Sending the Email
        smtp.sendmail(FROM, TO, BODY) 
        #Terminating the session 
        smtp.quit() 
        print ("Email sent successfully!") 
    except Exception as ex:
        print("Something went wrong....",ex)
        
# История по трек-номеру
def history(message):
    print("history")
    track_number = message.text
    #print(track_number)
    try:
        # Подключение к PostgreSQL 
        conn = get_connection_string()
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                     
        cursor = conn.cursor()
        sql = "SELECT track_number, to_char(datem, 'DD.MM.YYYY HH12:MI:SS'), title "
        sql = sql + "FROM movement LEFT JOIN package ON movement.package_id = package.id LEFT JOIN status ON movement.status_id=status.id "
        sql = sql + "WHERE track_number='" + track_number + "'"
        sql = sql + "ORDER BY datem"
        #print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        if cursor.rowcount <= 0:
            bot.send_message(message.chat.id,  "<b>Трек-номер:</b> " + track_number + ". Информации о местоположении посылки пока нет. После отправки посылки может пройти несколько дней, прежде чем она начнет отслеживаться. ", parse_mode='HTML' )                
        else:
            for row in results:
                bot.send_message(message.chat.id,  "<b>Трек-номер:</b> " + str(row[0]) +  "\n<b>Последнее движение:</b> " + str(row[1]) + " " + str(row[2]) , parse_mode='HTML' )                
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        send_welcome(message)
    except Exception as error:
        print(error)
        bot.reply_to(message, 'упс')       


bot.polling(none_stop=True, interval=0)



