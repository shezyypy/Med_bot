from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Дневник температуры')],
    [KeyboardButton(text='F.A.Q.'), KeyboardButton(text='Распространенные заболевания')]
], resize_keyboard=True)

diseases = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Грипп', callback_data='influenza'), InlineKeyboardButton(text='COVID-19', callback_data='covid')],
    [InlineKeyboardButton(text='Аллергия', callback_data='allergy'), InlineKeyboardButton(text='Диабет', callback_data='diabetes')],
    [InlineKeyboardButton(text='Гипертония', callback_data='hypertension'), InlineKeyboardButton(text='Сердечный приступ', callback_data='heart_attack')],
    [InlineKeyboardButton(text='Инсульт', callback_data='stroke'), InlineKeyboardButton(text='Астма', callback_data='asthma')],
    [InlineKeyboardButton(text='Ожирение', callback_data='obesity'), InlineKeyboardButton(text='Депрессия', callback_data='depression')]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='К списку болезней', callback_data='back')]
])