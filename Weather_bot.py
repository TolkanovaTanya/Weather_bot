import telebot
from telebot import types
import requests
import pyowm
from pyowm.utils.config import get_default_config


config_dict = get_default_config()
config_dict['language'] = 'ru'

open_weather_token = pyowm.OWM('636007d9a2150514dccbeb0c99ea67f2',config_dict)
token = '5560830260:AAF93mcx8e2K9Rm9L249jcqbJ3P8VndEcWo'
bot=telebot.TeleBot(token)
weather_token = '636007d9a2150514dccbeb0c99ea67f2'

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать погоду? Напиши город.', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def prognoz(message):
    try:
        owt=open_weather_token.weather_manager()
        owt.weather_at_place(message.text)
        city = message.text

        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=netric")

        pogoda = r.json()
        bot.send_message(message.chat.id,
                             f"Погодные условия: {pogoda['weather'][0]['description']}\nТемпература:{pogoda['main']['temp']}C°\nВидимость:{str(pogoda['visibility'])}м\n"
                             f"Максимальная температура:{pogoda['main']['temp_max']}C°\nМинимальная температура:{pogoda['main']['temp_min']}C°\nВетер:{pogoda['wind']['speed']}м/с\nВлажность:{pogoda['main']['humidity']}%\n"
                             f"Давление:{pogoda['main']['pressure']}мм.рт.ст")

    except:

        bot.send_message(message.chat.id, 'Такого города не существует')

bot.polling(none_stop=True, interval=0)