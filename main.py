# -*- coding: utf8 -*-
################################################################################################################################
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from config import siteReq
import io
import os
#################################################################################################################################

######################################################################
from aiogram.dispatcher import FSMContext                            
from aiogram.dispatcher.filters import Command                        
from aiogram.contrib.fsm_storage.memory import MemoryStorage        
from aiogram.dispatcher.filters.state import StatesGroup, State        
######################################################################

######################
import config        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ config.py
import keyboard        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ keyboard.py
######################

import logging # ПРОСТО ВЫВОДИТ В КОНСОЛЬ ИНФОРМАЦИЮ, КОГДА БОТ ЗАПУСТИТСЯ

storage = MemoryStorage() # FOR FSM
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
lesson = 0 
number = 0
step = 0

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO,)

@dp.message_handler(Command("start"), state=None)

async def welcome(message): 
    joinedFile = open("user.txt","r")
    joinedUsers = set ()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("user.txt","a")
        joinedFile.write(str(message.chat.id)+ "\n")
        joinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f"*Привет, {message.from_user.first_name}, здесь ты можешь найти гдз ко всему учебнику по английскому*", reply_markup=keyboard.start, parse_mode='Markdown')

@dp.message_handler(commands=['asa'])
async def rassilka(message):
    await bot.send_message(message.chat.id, f"*Рассылка началась \nБот оповестит когда рассылку закончит*", parse_mode='Markdown')
    receive_users, block_users = 0, 0
    joinedFile = open ("user.txt", "r")
    jionedUsers = set ()
    for line in joinedFile:
        jionedUsers.add(line.strip())
    joinedFile.close()
    for user in jionedUsers:
        try:
            await bot.send_photo(user, open('lzt.jpg', 'rb'), message.text[message.text.find(' '):])
            receive_users += 1
        except:
            block_users += 1
        await asyncio.sleep(0.4)
    await bot.send_message(message.chat.id, f"*Рассылка была завершена *\n"f"получили сообщение: *{receive_users}*\n"f"заблокировали бота: *{block_users}*", parse_mode='Markdown')

@dp.message_handler(content_types=['text'])
async def get_message(message):
    global lesson
    global number
    global step
    if message.text == "Информация":
        await bot.send_message(message.chat.id, text = "*Информация:*\nБота сделал @i3sey", parse_mode='Markdown')
    if message.text == "Статистика":
        await bot.send_message(message.chat.id, text = "Хочешь просмотреть статистику бота?", reply_markup=keyboard.stats, parse_mode='Markdown')
    if message.text == "Получить гдз":
        await bot.send_message(message.chat.id, text = "Введи *номер урока*", parse_mode='Markdown')
        step = 1
    else:
        if step == 1:
            try:
                lesson = int(message.text)
            except ValueError:
                await bot.send_message(message.chat.id, text = "*Цифрами*, пожалуйста", parse_mode='Markdown')
            else:
                await bot.send_message(message.chat.id, text = "Введи *номер упражнения*", parse_mode='Markdown')
                step = 2
        elif step == 2:
            try:
                number = int(message.text)
            except ValueError:
                await bot.send_message(message.chat.id, text = "*Цифрами*, пожалуйста", parse_mode='Markdown')
            else:
                step = 0
                await bot.send_message(message.chat.id, text = "Отправляю...", parse_mode='Markdown')
                data = siteReq(lesson, number)
                try:
                    await bot.send_photo(message.chat.id, data.content)
                except Exception:
                    file_obj = io.BytesIO(data.content)
                    file_obj.name = str(number) + ".jpg"
                    await bot.send_document(message.chat.id, file_obj)

       


    


@dp.callback_query_handler(text_contains='join') # МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "JOIN" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "JOIN"
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open('user.txt'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'*Вот статистика бота*: {d} человек', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "У тебя нет админки\n *Куда ты полез*", parse_mode='Markdown')



@dp.callback_query_handler(text_contains='cancle') # МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "cancle" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "cancle"
async def cancle(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "Ты вернулся В главное меню.", parse_mode='Markdown')


##############################################################
if __name__ == '__main__':
    print('Ура, победа!')                                    
executor.start_polling(dp)
##############################################################
