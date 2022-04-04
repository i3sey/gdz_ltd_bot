# -*- coding: utf8 -*-
################################################################################################################################
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import asyncio
from config import siteReq
import io
#################################################################################################################################

######################################################################                         
from aiogram.dispatcher.filters import Command                        
from aiogram.utils.exceptions import PhotoDimensions, BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage              
######################################################################

######################
import config        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ config.py
import keyboard        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ keyboard.py
######################

import logging # ПРОСТО ВЫВОДИТ В КОНСОЛЬ ИНФОРМАЦИЮ, КОГДА БОТ ЗАПУСТИТСЯ

#Обьявление переменных глобальных
storage = MemoryStorage() 
bot = Bot(token=config.botkey, 
parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
lesson = 0 
number = 0
step = 0

#Логи
logging.basicConfig(format='%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO,)

#Первый хендлер-команда старт
@dp.message_handler(Command("start"), state=None)
async def welcome(message): 
    joinedFile = open("user.txt","r", encoding="utf8") #Чекаем, есть ли чел в бд и если нет, то добавляем
    joinedUsers = set ()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("user.txt","a", encoding="utf8")
        joinedFile.write(str(message.chat.id)+ "\n")
        joinedUsers.add(message.chat.id)
#Здороваемся
    await bot.send_message(
        message.chat.id, f"*Привет, {message.from_user.first_name}, здесь ты можешь найти гдз ко всему учебнику по английскому*", 
        reply_markup=keyboard.start, 
        parse_mode='Markdown')

#Дальше системная команда для рассылки инфы
@dp.message_handler(commands=['asa'])
async def rassilka(message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, 
        "*Рассылка началась \nБот оповестит когда рассылку закончит*", 
        parse_mode='Markdown')
        receive_users, block_users = 0, 0
        joinedFile = open ("user.txt", "r", encoding="utf8")
        jionedUsers = set ()
        for line in joinedFile:
            jionedUsers.add(line.strip())
        joinedFile.close()
        for user in jionedUsers:
            try:
                await bot.send_photo(user, 
                open('update.png', 'rb'), 
                message.text[message.text.find(' '):])
                receive_users += 1
            except BotBlocked:
                block_users += 1
            await asyncio.sleep(0.4)
        await bot.send_message(message.chat.id, 
        f"*Рассылка была завершена *\n"f"получили сообщение: *{receive_users}*\n"f"заблокировали бота: *{block_users}*", 
        parse_mode='Markdown')
    else:
        await bot.send_message(message.chat.id, 
        "Думаешь почитал код и такой умный, **а нет**, я проверку на админку поставил, ха", 
        parse_mode='Markdown')

#тут капец гениальное решение......
#ВОТ ТУТ НАДО УМНОГО ЧЕЛА
@dp.message_handler(content_types=['text'])
async def get_message(message):
    global lesson # не юзайте глобал, это плохо
    global number
    global step
    #начинаем прогонять входящее сообщение через 7 кругов ада:
    #Если вы знаете как это упростить то сделайте коммит пж, я тупой
    if message.text == "Информация": #Если чел тыкнул по кнопке с инфой то мы ему шлем картинку с подписью 
        await bot.send_photo(message.chat.id, 
        photo=open('banner.jpg', 'rb'), 
        caption="<b>Информация:</b>\nБот найдёт и скинет вам гдз из учебника Тер-Тинасовой за 8 класс в 2 частях\nТут исходный код: <a href='https://github.com/i3sey/gdz_ltd_bot'>тут</a>", 
        parse_mode='HTML')
    elif message.text == "/stats": #Если админ написал о стате, то переспрашиваем его через инлайн кнопочки
        await bot.send_message(message.chat.id, 
        text = "Хочешь просмотреть статистику бота?", 
        reply_markup=keyboard.stats, 
        parse_mode='Markdown')
    elif message.text == "Получить гдз": #если чел неужели решил заюзать основной функционал бота, то идём дальше
        await bot.send_message(message.chat.id, 
        text = "Введи *номер урока*", 
        parse_mode='Markdown') # просим ввести номер урока
        step = 1 #Эта переменная раскажет нам о текущем состоянии процесса
    elif message.text == "Создатель": #Тут я резко вспомнил про эту кнопку
        await bot.send_message(message.chat.id, 
        text = "Бота разрабатывает @i3sey. Жду жалоб и предложений **<3.**", 
        parse_mode='Markdown')
    else:
        if step == 1: # воооооооот, если мы получили сообщение в ответ на просьбу номера УРОКА (а мы определили по степ = 1)
            try:
                lesson = int(message.text) # Пробуем перевести строкку в цифру
            except ValueError:
                await bot.send_message(message.chat.id, 
                text = "*Цифрами*, пожалуйста", 
                parse_mode='Markdown') # Если не получается то не меняя степ просим еще раз
            else:
                await bot.send_message(message.chat.id, 
                text = "Введи *номер упражнения*", 
                parse_mode='Markdown') #Следующее - номер просим
                step = 2 # второй степ
        elif step == 2: # если мы получили сообщение в ответ на просьбу номера НОМЕРА (мне лень каждый раз писать упражнения) (а мы определили по степ = 2)
            try:
                number = int(message.text) # Опять пробуем 
            except ValueError:
                await bot.send_message(message.chat.id, 
                text = "*Цифрами*, пожалуйста", 
                parse_mode='Markdown') #Опять разочаровываемся...
            else:
                step = 0 # сбрасываем степ, чтобы потом еще раз сделать
                data = siteReq(lesson, number) #Получаем картинку
                if data == -1:
                    await bot.send_message(message.chat.id, 
                        text = "Такого номера нет :(", 
                        parse_mode='Markdown')
                else:
                    try:
                        await bot.send_photo(message.chat.id, 
                        data.content, 
                        reply_markup=keyboard.arrows) #Пробуем отправить её как фото
                        #Это не всегда получается, ибо некоторые пикчи большие по размеру (в px, а не МБ) и там не работает
                    except PhotoDimensions: # Знаю, что так нельзя, но я не могу найти название исключения - ВОТ ТУТ НАДО УМНОГО ЧЕЛА
                        file_obj = io.BytesIO(data.content)
                        file_obj.name = f"{number}.jpg" #Делаем название файлу чтобы был не document, а 1.jpg культурный
                        await bot.send_document(message.chat.id, 
                        file_obj, 
                        reply_markup=keyboard.arrows) #Отправляем как док
        else:
            await bot.send_message(message.chat.id, 
                        text = "Я тебя не понял, используй кнопки внизу👇", 
                        parse_mode='Markdown')

#########################################################################################################
# кринж кончился вроде
#########################################################################################################

#Тут прописываем кнопочки, я думаю понятно
@dp.callback_query_handler(text_contains='Предыдущиий номер') 
async def prev(call: types.CallbackQuery):
    global lesson # глобал - плоха
    global number
    number = number - 1
    data = siteReq(lesson, number)
    if data != -1:
        file_obj1 = io.BytesIO(data.content)
        try: #Та же самая штука. Пробуем как фото, потом как док
            await bot.edit_message_media(
                types.InputMediaPhoto(file_obj1),
                chat_id=call.message.chat.id, 
                message_id=call.message.message_id, 
                reply_markup=keyboard.arrows)
        except PhotoDimensions:
            file_obj1 = io.BytesIO(data.content)
            file_obj1.name = f'{number}.jpg'
            await bot.edit_message_media(
                types.InputMediaDocument(file_obj1),
                chat_id=call.message.chat.id, 
                message_id=call.message.message_id,
                reply_markup=keyboard.arrows)
    else:
        with open('no.png', 'rb') as file:
            photo = types.InputMediaPhoto(file)
            await bot.edit_message_media(
                    media=photo,
                    chat_id=call.message.chat.id, 
                    message_id=call.message.message_id, 
                    reply_markup=keyboard.arrows)

@dp.callback_query_handler(text_contains='Предыдущии урок')
async def prev_lesson(call: types.CallbackQuery):
    global lesson
    global number
    lesson = lesson - 1
    data = siteReq(lesson, number)
    if data != -1:
        file_obj1 = io.BytesIO(data.content)
        try: #Та же самая штука. Пробуем как фото, потом как док
            await bot.edit_message_media(
                types.InputMediaPhoto(file_obj1),
                chat_id=call.message.chat.id, 
                message_id=call.message.message_id, 
                reply_markup=keyboard.arrows)
        except PhotoDimensions:
            file_obj1 = io.BytesIO(data.content)
            file_obj1.name = f'{number}.jpg'
            await bot.edit_message_media(
                types.InputMediaDocument(file_obj1),
                chat_id=call.message.chat.id, 
                message_id=call.message.message_id,
                reply_markup=keyboard.arrows)
    else:
        with open('no.png', 'rb') as file:
            photo = types.InputMediaPhoto(file)
            await bot.edit_message_media(
                    media=photo,
                    chat_id=call.message.chat.id, 
                    message_id=call.message.message_id, 
                    reply_markup=keyboard.arrows)

@dp.callback_query_handler(text_contains='Следующий урок')
async def next_lesson(call: types.CallbackQuery):
    global lesson
    global number
    lesson = lesson + 1
    data = siteReq(lesson, number)
    if data != -1:
        file_obj1 = io.BytesIO(data.content)
        try: #Та же самая штука. Пробуем как фото, потом как док
            await bot.edit_message_media(
                types.InputMediaPhoto(file_obj1),
                chat_id=call.message.chat.id, 
                message_id=call.message.message_id, 
                reply_markup=keyboard.arrows)
        except PhotoDimensions:
            file_obj1 = io.BytesIO(data.content)
            file_obj1.name = f'{number}.jpg'
            await bot.edit_message_media(
                types.InputMediaDocument(file_obj1),
                chat_id=call.message.chat.id, 
                message_id=call.message.message_id,
                reply_markup=keyboard.arrows)
    else:
        with open('no.png', 'rb') as file:
            photo = types.InputMediaPhoto(file)
            await bot.edit_message_media(
                    media=photo,
                    chat_id=call.message.chat.id, 
                    message_id=call.message.message_id, 
                    reply_markup=keyboard.arrows)

@dp.callback_query_handler(text_contains='Следующий номер')
async def nextNumber(call: types.CallbackQuery):
    global lesson
    global number
    number = number + 1
    data = siteReq(lesson, number)
    if data != -1:
        file_obj1 = io.BytesIO(data.content)
        try: #Та же самая штука. Пробуем как фото, потом как док
            await bot.edit_message_media(
                types.InputMediaPhoto(file_obj1),
                chat_id=call.message.chat.id, 
                message_id=call.message.message_id, 
                reply_markup=keyboard.arrows)
        except PhotoDimensions:
            file_obj1 = io.BytesIO(data.content)
            file_obj1.name = f'{number}.jpg'
            await bot.edit_message_media(
                types.InputMediaDocument(file_obj1),
                chat_id=call.message.chat.id, 
                message_id=call.message.message_id,
                reply_markup=keyboard.arrows)
    else:
        with open('no.png', 'rb') as file:
            photo = types.InputMediaPhoto(file)
            await bot.edit_message_media(
                    media=photo,
                    chat_id=call.message.chat.id, 
                    message_id=call.message.message_id, 
                    reply_markup=keyboard.arrows)

@dp.callback_query_handler(text_contains='Удалить')
async def delt(call: types.CallbackQuery):
    await bot.delete_message(
        chat_id=call.from_user.id, 
        message_id=call.message.message_id) #Удаляем решение

@dp.callback_query_handler(text_contains='Да') # тут вопросик насчёт статы
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin: # Ты админ?
        d = sum(1 for line in open('user.txt', encoding='utf8'))
        await bot.edit_message_text(chat_id=call.message.chat.id, 
        message_id=call.message.message_id, 
        text=f'*Вот статистика бота*: {d} человек', 
        parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, 
        message_id=call.message.message_id, 
        text = "У тебя нет админки\n *Куда ты полез*", 
        parse_mode='Markdown')



@dp.callback_query_handler(text_contains='Нет') # Домой, на базу
async def cancle(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, 
    message_id=call.message.message_id, 
    text= "Ты вернулся В главное меню.", 
    parse_mode='Markdown')


##############################################################
if __name__ == '__main__':
    print('Ура, победа!')                                    
executor.start_polling(dp)
##############################################################
