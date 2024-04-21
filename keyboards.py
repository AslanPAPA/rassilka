from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#КНОПКА СТАРТ
Start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👤 Профиль', callback_data='profile')],
    [InlineKeyboardButton(text='🛒 Магазин', callback_data='InDev')],
    [InlineKeyboardButton(text='⚙️ Парсер', callback_data='parser')],
    [InlineKeyboardButton(text='📋 Инструкция', callback_data='instruction')],
    [InlineKeyboardButton(text='🛠️ Техническая поддержка', callback_data='InDev')]
])

#КНОПКА ПАРСИНГ
ChooseParsing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1️⃣ Парсинг сообщества ВК', callback_data='parsSoobVk')],
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToStart')]
])

#КНОПКА НАЗАД К ПАРСИНГ СООБЩЕСТВО ВК
backParsChoosePars = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backParsChoosePars')]
])

#КНОПКА ИНСТРУКЦИЯ
Instruction = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❓️ Как получить токен', callback_data='getToken')],
    [InlineKeyboardButton(text='❓️ Видео-инструкция', callback_data='getVideo')],
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToStart')]

])

#КНОПКА ПОЛУЧИТЬ ТОКЕН
GetToken = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToInstruction')]

])

#КНОПКА ПРОФИЛЬ
Profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🪪 Аккаунты', callback_data='accounts'),
     InlineKeyboardButton(text='💎 VIP', callback_data='InDev')],
    [InlineKeyboardButton(text='📜 Задания', callback_data='task'),
     InlineKeyboardButton(text='💵 Пополнить баланс', callback_data='InDev')],
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToStart')]
])

#КНОПКА АККАУНТЫ
Accounts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Добавить аккаунт', callback_data='addAcc')],
    [InlineKeyboardButton(text='🗑️ Удалить аккаунт', callback_data='gg')],
    [InlineKeyboardButton(text='️⬅️ НАЗАД', callback_data='backToPrfl')]
])

#КНОПКА НАЗАД К АККАУНТАМ
AddingAccount = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToAcc')]
])



#КНОПКИ ЗАДАНИЯ
Task = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💬 Рассылка', callback_data='rassilka'),
     InlineKeyboardButton(text='📝 Текст', callback_data='text')],
    [InlineKeyboardButton(text='⏳ Интервал', callback_data='InDev'),
     InlineKeyboardButton(text='⏯ Старт/Стоп', callback_data='InDev')],
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToPrfl')]
])
#КНОПКА ПРОДОЛЖИТЬ
Countinue = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ПРОДОЛЖИТЬ ➡️', callback_data='task')]
])

#КНОПКА НАЗАД К ЗАДАНИЯМ
backTask = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToTask')]
])

#КНОПКА РАССЫЛКА
Rassilka = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📩 Рассылка в ЛС', callback_data='RassInLs')],
    [InlineKeyboardButton(text='✉️ Рассылка по чатам', callback_data='RassInChats')],
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToTask')]
])

#РАССЫЛКА В ЛС
RassilkaInLs = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToRass')]
])
