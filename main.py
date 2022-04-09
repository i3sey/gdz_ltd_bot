import asyncio
import io
import logging
import pickle

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked, PhotoDimensions

import config


arrows = InlineKeyboardMarkup()
langs = InlineKeyboardMarkup()


class Parameters:
    lesson = 0
    number = 1
    delCount = 5
    lang = 'Russian'
    info = ''
    creator = ''
    mainButton = ''
    settings = ''
    start = types.ReplyKeyboardMarkup(resize_keyboard=True)



def Lang(number):
    match Parameters.lang:
        case 'Russian':
            russianLang = [
                "<b>📝Информация:</b>\n✍️Бот найдёт и скинет вам гдз из учебника Тер-Тинасовой за 8 класс в 2 частях\n👾Исходный код: <a href='https://github.com/i3sey/gdz_ltd_bot'>тут</a>",
                "Бота разрабатывает @i3sey. Жду жалоб и предложений **<3.**",
                '✍️Введи номер урока:',
                "Я тебя не понял, используй кнопки внизу👇",
                'У тебя нет админки\n*Куда ты полез?*',
                '*Используй цифры*, пожалуйста',
                "✍️Введи номер упражнения:",
                "_Секунду..._",
                "🤷Такого номера нет, убедись, что всё *введено правильно*",
                '📝Информация',
                '🧑‍🎤Создатель',
                '👋Получить ГДЗ',
                '🔧Настройки',
                'Выбери язык:'
            ]
            return russianLang[number]
        case 'English':
            EnglishLang = [
                "<b>📝Information:</b>\n✍️The bot will find and send you the gdz from Ter-Minasova's textbook for the 8th grade in 2 parts\n👾Source code: <a href='https://github.com/i3sey/gdz_ltd_bot'>here</a>",
                "The bot is being developed by @i3sey. I am waiting for complaints and suggestions **<3.**",
                '✍️Enter the lesson number:',
                "I didn't understand you, use the buttons at the bottom👇",
                "You don't have an admin panel\n*Where are you going?*",
                '*Use numbers*, please',
                "✍️Enter the exercise number:",
                "_Just a second..._",
                "🤷There is no such number, make sure that everything * is entered correctly*",
                '📝Information',
                '🧑‍🎤Creator',
                '👋Get GDZ',
                '🔧Settings',
                'Select language'
            ]
            return EnglishLang[number]
        case 'roflRus':
            RoflLang = [
                "<b>📝Инфа:</b>\n✍️Домашку кидает по английскому(пока что), что еще тут пиздеть?\n👾Если дохуя умный, вот исходники: <a href='https://github.com/i3sey/gdz_ltd_bot'>хуй</a>",
                "Ахуеный челик — @i3sey. Если бабок дохуя, пишите, помогу потратить **8=====D.**",
                '✍️Номер урока блять:',
                "Сука, еблан, кнопки нажимай👇",
                "ТЫ ЧТО АХУЕЛ, У ТЕБЯ ДАЖЕ АДМИНКИ НЕТ\n*ИДИ НАХУЙ*",
                '*Пошел нахуй*, ЦЫФЕРАМИ БЛЯТЬ',
                "✍️Номер задания блять:",
                "_Пойду обкашляю вопросик..._",
                "🤷ЕБЛАН, *НЕТ ТУТ ТАКОГО*",
                '📝Инфа',
                '🧑‍🎤Пиздатый чел',
                '👋НА ПО ЕБАЛУ',
                '🔧Вопросики',
                'За базаром-то следи:'
            ]
            return RoflLang[number]
        case _:
            return russianLang[number]


arrows.add(
    InlineKeyboardButton('⬅️', callback_data='Предыдущиий номер'),
    InlineKeyboardButton('❌', callback_data='Удалить'),
    InlineKeyboardButton('➡️', callback_data='Следующий номер')
)


logging.basicConfig(
    filemode='logs.log',
    level=logging.INFO
)

storage = MemoryStorage()
bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
VERSION = 2.1


async def caseChoose(message):
    match message.text:
        case '📝Информация' | '📝Information' | '📝Инфа':
            await bot.send_message(message.chat.id,
                                   text=Lang(0),
                                   parse_mode='HTML')
        case '🧑‍🎤Создатель' | '🧑‍🎤Creator' | '🧑‍🎤Пиздатый чел':
            await bot.send_message(message.chat.id,
                                   text=Lang(1),
                                   parse_mode='Markdown')
        case '👋Получить ГДЗ' | '👋Get GDZ' | '👋НА ПО ЕБАЛУ':
            await message.answer(Lang(2))
            await getGdz.getLesson.set()
        case '🔧Настройки' | '🔧Settings' | '🔧Вопросики':
            await bot.send_message(message.chat.id,
                                   text=Lang(13),
                                   parse_mode='HTML',
                                   reply_markup=langs)
        case _:
            await bot.send_message(message.chat.id,
                                   text=Lang(3),
                                   parse_mode='Markdown')


def siteReq(lesson, number):
    gdzUrl = f'https://gdz.ltd/content/8-class/angliyskiy/Ter_Minasovaj/exercise/{lesson}/{number}.jpg'
    with open('answers_database.txt', encoding='utf8') as f:
        datafile = f.readlines()
    for line in datafile:
        if gdzUrl in line:
            r = requests.get(gdzUrl)
            return r.content
    return -1


class getGdz(StatesGroup):
    getLesson = State()
    getNumber = State()


@dp.message_handler(Command('start'), state=None)
async def welcome(message):
    joinedFile = open("users_database.txt","r", encoding="utf8") #Чекаем, есть ли чел в бд и если нет, то добавляем
    joinedUsers = set ()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("users_database.txt","a", encoding="utf8")
        joinedFile.write(str(message.chat.id)+ "\n")
        joinedUsers.add(message.chat.id)
    #await bot.send_message(message.chat.id,
    #                        f"Привет, *{message.from_user.first_name}!* Этот бот призван помочь тебе с заданиями по английскому.\n*Приятного использования!*",
    #                        reply_markup=Parameters.start, parse_mode='Markdown')
        #with open('saved_dictionary.pkl', 'wb') as f:
        #    pickle.dump(Parameters.d, f)
    Parameters.start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Parameters.info = types.KeyboardButton(Lang(9))
    Parameters.creator = types.KeyboardButton(Lang(10))
    Parameters.mainButton = types.KeyboardButton(Lang(11))
    #Parameters.settings = types.KeyboardButton(Lang(12))
    Parameters.start.add(Parameters.mainButton)
    Parameters.start.add(
        Parameters.info, Parameters.creator, Parameters.settings)
    await bot.send_message(message.chat.id,
                            f'*✅Обновление успешно*\n*Текущая версия:* {VERSION}',
                            reply_markup=Parameters.start, parse_mode='Markdown')
        #with open('saved_dictionary.pkl', 'wb') as f:
        #    pickle.dump(Parameters.d, f)
    
    


@dp.message_handler(Command('stats'), state=None)
async def statistic(message):
    if message.chat.id == config.admin:
        d = sum(1 for line in open('users_database.txt', encoding='utf8'))
        await bot.send_message(message.chat.id,
                               text=f'Вот статистика бота: *{d}* человек',
                               parse_mode='Markdown')
    else:
        await bot.send_message(message.chat.id,
                               text=Lang(4),
                               parse_mode='Markdown')


@dp.message_handler(commands=['send'])
async def sending(message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, "*Рассылка началась \nБот оповестит когда рассылку закончит*", parse_mode='Markdown')
        receive_users, block_users = 0, 0
        joinedFile = open ("users_database.txt", "r", encoding="utf8")
        jionedUsers = set()
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
        await bot.send_message(message.chat.id, f"*Рассылка была завершена *\n"
                               f"получили сообщение: *{receive_users}*\n"
                               f"заблокировали бота: *{block_users}*", parse_mode='Markdown')
    else:
        await bot.send_message(message.chat.id,
                               text='У тебя нет админки\n*Куда ты полез?*',
                               parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def get_message(message):
    await caseChoose(message)


@dp.message_handler(state=getGdz.getLesson)
async def getLesson(message: types.Message, state: FSMContext):
    try:
        lesson = int(message.text)
    except ValueError:
        await state.finish()
        await caseChoose(message)
        # await bot.send_message(message.chat.id,
        #                       text=Lang(5),
        #                       parse_mode='Markdown')
        #Parameters.delCount += 2

    else:
        await state.update_data(lesson=lesson)
        await message.answer(Lang(6))
        await getGdz.getNumber.set()


@dp.message_handler(state=getGdz.getNumber)
async def getNumber(message: types.Message, state: FSMContext):
    try:
        number = int(message.text)
    except ValueError:
        await state.finish()
        await caseChoose(message)
        # await bot.send_message(message.chat.id,
        #                       text=Lang(5),
        #                       parse_mode='Markdown')
        #Parameters.delCount += 2
    else:
        await state.update_data(number=number)
        data = await state.get_data()
        await bot.send_message(message.chat.id,
                               text=Lang(7),
                               parse_mode='Markdown')
        Parameters.lesson = data.get("lesson")
        Parameters.number = data.get("number")
        photo = siteReq(Parameters.lesson, Parameters.number)
        if photo == -1:
            await bot.send_message(message.chat.id,
                                   text=Lang(8),
                                   parse_mode='Markdown')
        else:
            try:
                await bot.send_photo(message.chat.id,
                                     photo=photo,
                                     reply_markup=arrows)
            except PhotoDimensions:
                fileByte = io.BytesIO(photo)
                fileByte.name = f"{Parameters.number}.jpg"
                await bot.send_document(message.chat.id,
                                        fileByte,
                                        reply_markup=arrows)
            for i in range(2):
                await bot.delete_message(message.chat.id, message.message_id+i)
            for i in range(1, Parameters.delCount):
                await bot.delete_message(message.chat.id, message.message_id-i)
            Parameters.delCount = 5
        await state.finish()


@dp.callback_query_handler(text_contains='Предыдущиий номер')
async def prevNumber(call: types.CallbackQuery):
    Parameters.number -= 1
    photo = siteReq(Parameters.lesson, Parameters.number)
    if photo == -1:
        Parameters.lesson -= 1
        Parameters.number = 1
        photo = siteReq(Parameters.lesson, Parameters.number)
    photoByte = io.BytesIO(photo)
    try:
        await bot.edit_message_media(
            types.InputMediaPhoto(photoByte),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=arrows)
    except PhotoDimensions:
        photoByte = io.BytesIO(photo)
        photoByte.name = f'{Parameters.number}.jpg'
        await bot.edit_message_media(
            types.InputMediaDocument(photoByte),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=arrows)
    await call.answer()


@dp.callback_query_handler(text_contains='Удалить')
async def delt(call: types.CallbackQuery):
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id)


@dp.callback_query_handler(text_contains='Следующий номер')
async def nextNumber(call: types.CallbackQuery):
    Parameters.number += 1
    photo = siteReq(Parameters.lesson, Parameters.number)
    if photo == -1:
        Parameters.lesson += 1
        Parameters.number = 1
        photo = siteReq(Parameters.lesson, Parameters.number)
    photoByte = io.BytesIO(photo)
    try:
        await bot.edit_message_media(
            types.InputMediaPhoto(photoByte),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=arrows)
    except PhotoDimensions:
        photoByte = io.BytesIO(photo)
        photoByte.name = f'{Parameters.number}.jpg'
        await bot.edit_message_media(
            types.InputMediaDocument(photoByte),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=arrows)
    await call.answer()


'''@dp.callback_query_handler(text_contains='rus')
async def rus(call: types.CallbackQuery):
    Parameters.lang = 'Russian'
    Parameters.d[str(call.message.chat.id)] = 'Russian'
    await bot.send_message(call.message.chat.id,
                           text='*✅Чтобы изменить язык* кнопок внизу нажмите /start',
                           parse_mode='Markdown')
    await call.answer()


@dp.callback_query_handler(text_contains='en')
async def rus(call: types.CallbackQuery):
    Parameters.lang = 'English'
    Parameters.d[str(call.message.chat.id)] = 'English'
    await bot.send_message(call.message.chat.id,
                           text='*✅To change the language* of the buttons at the bottom, press /start',
                           parse_mode='Markdown')
    await call.answer()


@dp.callback_query_handler(text_contains='gay')
async def rus(call: types.CallbackQuery):
    Parameters.lang = 'roflRus'
    Parameters.d[str(call.message.chat.id)] = 'roflRus'
    await bot.send_message(call.message.chat.id,
                           text='*✅Всё, заебумба* только теперь ёбни по /start, чтоб хуйни снизу обновились',
                           parse_mode='Markdown')
    await call.answer()'''

if __name__ == '__main__':
    logging.info('Bot started...')
executor.start_polling(dp)
