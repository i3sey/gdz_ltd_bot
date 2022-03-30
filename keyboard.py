from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

######################################################
start = types.ReplyKeyboardMarkup(resize_keyboard=True) # СОЗДАЕМ ВООБЩЕ ОСНОВУ ДЛЯ КНОПОК

info = types.KeyboardButton("Информация")            # ДОБАВЛЯЕМ КНОПКУ ИНФОРМАЦИИ
stats = types.KeyboardButton("Статистика")            # ДОБАВЛЯЕМ КНОПКУ СТАТИСТИКИ
let = types.KeyboardButton("Получить гдз")


start.add(let)
start.add(info, stats) #ДОБАВЛЯЕМ ИХ В БОТА

stats = InlineKeyboardMarkup()    # СОЗДАЁМ ОСНОВУ ДЛЯ ИНЛАЙН КНОПКИ
stats.add(InlineKeyboardButton(f'Да', callback_data = 'join')) # СОЗДАЁМ КНОПКУ И КАЛБЭК К НЕЙ
stats.add(InlineKeyboardButton(f'Нет', callback_data = 'cancle')) # СОЗДАЁМ КНОПКУ И КАЛБЭК К НЕЙ

arrows = InlineKeyboardMarkup() #сделал листалку
arrows.add(
    InlineKeyboardButton(f'⬅️', callback_data = 'prev'),
    InlineKeyboardButton(f'❌', callback_data = 'delt'),
    InlineKeyboardButton(f'➡️', callback_data = 'next')
    )