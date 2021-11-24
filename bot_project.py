import logging
import os
import re

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import aiogram.utils.markdown as fmt

logging.basicConfig(level=logging.INFO)
load_dotenv()
token = os.getenv("BOT_KEY")
user_data = {}
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        "метро Анино",
        "метро Китай-Город",
        "метро ВДНХ",
        "метро Митино",
        "метро Спартак",
        "метро Сокол",
    ]
    keyboard.add(*buttons)
    await message.answer('Выберите адрес склада:', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "метро Анино")
@dp.message_handler(lambda message: message.text == "метро Китай-Город")
@dp.message_handler(lambda message: message.text == "метро ВДНХ")
@dp.message_handler(lambda message: message.text == "метро Митино")
@dp.message_handler(lambda message: message.text == "метро Спартак")
@dp.message_handler(lambda message: message.text == "метро Сокол")
async def sklad_1_answer(message: types.Message):
    user_data['adress'] = message.text

    buttons = [
        types.InlineKeyboardButton(text='сезонные вещи', callback_data='сезонные вещи'),
        types.InlineKeyboardButton(text='другое', callback_data='другое')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer("Что хотите хранить?:", reply_markup=keyboard)


@dp.callback_query_handler(text='сезонные вещи')
async def send_msg(call: types.CallbackQuery):
    await call.message.answer('yyy', reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


@dp.callback_query_handler(text='другое')
async def send_msg_other(call: types.CallbackQuery):
    await call.message.answer(
        fmt.text(
            fmt.text(fmt.hunderline("Условия:\n\n")),
            fmt.text("599 руб - первый 1 кв.м., далее +150 руб за каждый кв. метр в месяц")
        ),
        reply_markup=types.ReplyKeyboardRemove()
    )
    buttons = [
        types.InlineKeyboardButton(
            text=f'ячейка {cell} кв м', callback_data=f'{cell}') for cell in [1, 3, 6, 10]
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard.add(*buttons)
    await call.message.answer("Выберите размер ячейки:", reply_markup=keyboard)
    await call.answer()


@ dp.callback_query_handler(text='1')
@ dp.callback_query_handler(text='3')
@ dp.callback_query_handler(text='6')
@ dp.callback_query_handler(text='10')
async def send_date(call: types.CallbackQuery):
    user_data['size_cell'] = call.data
    buttons = [
        types.InlineKeyboardButton(
            text=f"{month} мес", callback_data=f"{month}a") for month in range(1, 11)
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=4, resize_keyboard=True)
    keyboard.add(*buttons)
    await call.message.answer("Выберите срок аренды:", reply_markup=keyboard)
    await call.answer()


@ dp.callback_query_handler(text='1a')
@ dp.callback_query_handler(text='2a')
@ dp.callback_query_handler(text='3a')
@ dp.callback_query_handler(text='4a')
@ dp.callback_query_handler(text='5a')
@ dp.callback_query_handler(text='6a')
@ dp.callback_query_handler(text='7a')
@ dp.callback_query_handler(text='8a')
@ dp.callback_query_handler(text='9a')
@ dp.callback_query_handler(text='10a')
@ dp.callback_query_handler(text='11a')
@ dp.callback_query_handler(text='12a')
async def choice_month(call: types.CallbackQuery):
    user_data['rent'] = call.data
    month = re.findall(r'\d+', call.data)
    if user_data['size_cell'] == "1":
        price_one_month = 599
    else:
        price_one_month = ((int(user_data['size_cell']) - 1) * 150) + 599
    total_price = price_one_month * int(*month)
    buttons = [
        types.InlineKeyboardButton(
            text="Забронироавать", callback_data='ok')
    ]
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await call.message.answer(
        fmt.text(
            fmt.text(fmt.hunderline("Вы выбрали:")),
            fmt.text(f"\nРазмер ячейки:   {user_data['size_cell']} кв м"),
            fmt.text(f"\nСрок аренды:   {int(*month)} месяцев"),
            fmt.text(f"\nПо адресу:   {user_data['adress']}"),
            fmt.text(f"\nСтоимость итого:   {total_price} рублей"), sep="\n"
        ), reply_markup=keyboard)
    await call.answer()


@ dp.callback_query_handler(text='ok')
async def registration(call: types.CallbackQuery):
    await call.message.answer('хз', reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

