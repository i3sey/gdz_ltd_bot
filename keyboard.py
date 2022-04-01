from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

######################################################
start = types.ReplyKeyboardMarkup(resize_keyboard=True) # создаем основы для кнопок
arrows = InlineKeyboardMarkup() 
stats = InlineKeyboardMarkup()    

info = types.KeyboardButton("Информация")            #    Добавляем кнопку информации
let = types.KeyboardButton("Получить гдз")           #    Основная кнопка
creator = types.KeyboardButton("Создатель")          #    тут я

start.add(let)                    #добавляем их в прорядке правильном
start.add(info, creator) 

stats.add(InlineKeyboardButton(f'Да', callback_data = 'Да')) # А тут кнопочки инлайновые, с каллбеком
stats.add(InlineKeyboardButton(f'Нет', callback_data = 'Нет')) 


#TODO:
#заменить неинформативные эмодзи на цифры уроков:

arrows.add(
    InlineKeyboardButton(f'⬅️', callback_data = 'Предыдущиий номер'),
    InlineKeyboardButton(f'❌', callback_data = 'Удалить'),
    InlineKeyboardButton(f'➡️', callback_data = 'Следующий номер')
    )
arrows.add(
    InlineKeyboardButton(f'⬅️', callback_data = 'Предыдущии урок'),
    InlineKeyboardButton(f'➡️', callback_data = 'Следующий урок')
)