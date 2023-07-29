# Импортируем библиоетки
# pip install aiogram

import os
import datetime
import requests
import math
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from TOKEN import token
from user_keyboards import commands_default_keyboard

# Инициализируем бота
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


class Dialog(StatesGroup):
    wait_city = State()


@dp.message_handler(commands=['start'])
@dp.message_handler(text=['Начать', 'Старт'])
async def start_command(message: types.Message):
    await message.reply('Привет, кодеры!\nНапишите мне название города и я пришлю вам погоду', reply_markup=commands_default_keyboard)
    await Dialog.wait_city.set()


@dp.message_handler(commands=['/send_city'])
@dp.message_handler(state=Dialog.wait_city)
async def get_city(message: Message, state: FSMContext):
    name_of_city = message.text
    name_of_city = name_of_city.strip().lower()
    url = f'http://api.openweathermap.org/data/2.5/weather?q={name_of_city}&lang=ru&units=metric&appid=56a1127e15eec70e9830ad373111e01c'
    try:
        response = requests.get(f"{url}")
        data = response.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"])

        length_of_the_day = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    except:
        await message.reply("Проверьте название города!")

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    weather_description = data["weather"][0]["main"]

    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        # если эмодзи для погоды нет, выводим другое сообщение
        wd = "Посмотри в окно, я не понимаю, что там за погода..."

    await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                        f"Погода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n"
                        f"Влажность: {humidity}%\nДавление: {math.ceil(pressure/1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
                        f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                        f"Хорошего дня!")


# @dp.message_handler()
# async def get_weather(message: types.Message):
#     name_of_city = await bot.await_answer
#     url = f'http://api.openweathermap.org/data/2.5/weather?q={name_of_city}&lang=ru&units=metric&appid=56a1127e15eec70e9830ad373111e01c'

#     async def cmd_dialog_name(message: types.Message):
#         await Dialog.wait_name.set()
#         await message.reply("Человечишка, напиши мне свое жалкое мнение")

#     @dp.message_handler(state=Dialog.wait_city)
#     async def get_city(message: Message, state: FSMContext):
#         otvet = search_pass_name(message.text)
#         await message.answer(text=otvet)
#         await state.reset_state()

#     try:
#         response = requests.get(f"{url}")
#         data = response.json()
#         city = data["name"]
#         cur_weather = data["main"]["temp"]
#         humidity = data["main"]["humidity"]
#         pressure = data["main"]["pressure"]
#         wind = data["wind"]["speed"]

#         sunrise_timestamp = datetime.datetime.fromtimestamp(
#             data["sys"]["sunrise"])
#         sunset_timestamp = datetime.datetime.fromtimestamp(
#             data["sys"]["sunset"])

#         length_of_the_day = datetime.datetime.fromtimestamp(
#             data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
#     except:
#         await message.reply("Проверьте название города!")

#     code_to_smile = {
#         "Clear": "Ясно \U00002600",
#         "Clouds": "Облачно \U00002601",
#         "Rain": "Дождь \U00002614",
#         "Drizzle": "Дождь \U00002614",
#         "Thunderstorm": "Гроза \U000026A1",
#         "Snow": "Снег \U0001F328",
#         "Mist": "Туман \U0001F32B"
#     }

#     weather_description = data["weather"][0]["main"]

#     if weather_description in code_to_smile:
#         wd = code_to_smile[weather_description]
#     else:
#         # если эмодзи для погоды нет, выводим другое сообщение
#         wd = "Посмотри в окно, я не понимаю, что там за погода..."

#     await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
#                         f"Погода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n"
#                         f"Влажность: {humidity}%\nДавление: {math.ceil(pressure/1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
#                         f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
#                         f"Хорошего дня!")


if __name__ == '__main__':
    executor.start_polling(dp)
