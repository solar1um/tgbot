import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from bs4 import BeautifulSoup
import requests



current_date = datetime.today().date()
print(current_date)

number = {
    1: 'АИ-100',
    2: 'АИ-98',
    3: 'B-Power 92',
    4: 'АИ-92',
    5: 'ДТ',
    6: 'СУГ',
}

URL = "https://bpetroleum.kg/rus/retail/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

res = []
i = 1
while i < 6:
    res.append(" ".join([number[i], '= ' + list(soup.findAll('table')[-1].findAll('tr')[i])[1].text + 'сом']))
    i = i + 1


res.append(str(current_date) + '\nЦены взяты с оффициального сайта BishkekPetroleum  \n(https://bpetroleum.kg/) ')
prices = "\n\n".join(res)
print(prices)


logging.basicConfig(level=logging.INFO)

API_TOKEN = '6277259561:AAEe2h4PpmPF0OLZTQgmQQdF9seFSda5QHw'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_kb_full.add(InlineKeyboardButton('Цены на бензин', callback_data='button_pressed'))
    await bot.send_message(chat_id=message.chat.id, text="Привет! Чтоб узнать цены на бензин нажми на кнопку!", reply_markup=inline_kb_full)

@dp.callback_query_handler(lambda c: c.data == 'button_pressed')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, prices)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



