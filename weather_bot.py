import logging
import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# инициализация
bot = Bot(token=" -токен бота- ")
dp = Dispatcher(bot)

# создание словаря
conversation_state = {}

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    """Send a message when the command /start is issued."""
    await message.reply("Привет! Отправь /weather для запуска бота.")

@dp.message_handler(commands='weather')
async def get_weather(message: types.Message):
    """Get the weather in the city specified in the command"""
    # запись состояния в словарь
    conversation_state[message.from_user.id] = "waiting_for_city"
    await message.reply("Отправь название города чтобы получить текущую погоду.")

@dp.message_handler()
async def get_city(message: types.Message):
    """Get the weather for the city specified in a separate message"""
    # проверка названия
    if conversation_state.get(message.from_user.id) == "waiting_for_city":
        # название города
        city = message.text
        # объявление API ключа как переменную
        os.environ["2c254a2efb0b9008ce295e94a0939a2f"] = "2c254a2efb0b9008ce295e94a0939a2f"
        api_key = os.environ["2c254a2efb0b9008ce295e94a0939a2f"]
        # запрос к Openweathermap API
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru"
        response = requests.get(url)
        # проверка статуса ответа
        if response.status_code == 200:
            # погодные данные
            data = response.json()
            temperature = round(data["main"]["temp"] - 273.15)
            description = data["weather"][0]["description"]
            # ответ бота
            text = f"В {city} сейчас {temperature}°C и {description}. \nПоехали?"
            # посылка сообщения
            await message.reply(text=text)
        else:
            # сообщение об ошибке
            await message.reply("Error: city not found")
        # сброс состояния диалога
        conversation_state[message.from_user.id] = None

if __name__ == '__main__':
    # запуск бота
    executor.start_polling(dp)