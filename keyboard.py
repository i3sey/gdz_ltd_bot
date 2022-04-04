from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

######################################################
start = types.ReplyKeyboardMarkup(resize_keyboard=True) # создаем основы для кнопок
arrows = InlineKeyboardMarkup()
stats = InlineKeyboardMarkup()

info = types.KeyboardButton("Информация")            #    Добавляем кнопку информации
let = types.KeyboardButton("Получить гдз")           #    Основная кнопка
creator = types.KeyboardButton("Создатель")          #    тут я

start.add(let)                    #добавляем их в прорядке правильном
start.add(info, creator)

stats.add(InlineKeyboardButton('Да', callback_data = 'Да')) # А тут кнопочки инлайновые, с каллбеком
stats.add(InlineKeyboardButton('Нет', callback_data = 'Нет'))


#TO-DO:
#заменить неинформативные эмодзи на цифры уроков:

arrows.add(
    InlineKeyboardButton('⬅️ Номер', callback_data = 'Предыдущиий номер'),
    InlineKeyboardButton('❌', callback_data = 'Удалить'),
    InlineKeyboardButton('Номер ➡️', callback_data = 'Следующий номер')
    )
arrows.add(
    InlineKeyboardButton('⬅️ Урок', callback_data = 'Предыдущии урок'),
    InlineKeyboardButton('Урок ➡️', callback_data = 'Следующий урок')
)
