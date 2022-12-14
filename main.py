import logging
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import filters

import os
import subprocess

from logic_module import get_time, new_user, update_time_used, get_statistics, get_timetable
from keyboards_module import generate_default_keyboard, system_phrases


API_TOKEN = os.environ["API_TOKEN_fts"]
WEBHOOK_PATH = ""
WEBHOOK_URL = subprocess.check_output('curl -s localhost:4040/api/tunnels/fuck_the_school_bot | jq -r .public_url',
                                      shell=True).decode('utf-8')[:-1]
print(WEBHOOK_URL)
WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 5001

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


# states
class Form(StatesGroup):
    active = State()


# -----------   HANDLERS   -----------
# Initial handler
@dp.message_handler(state=None)
async def start(message: types.Message):
    new_user(message)
    await bot.send_message(message.chat.id, "Вечер добрый. можешь нажать на кнопку внизу или написать мне любой"
                                            " другой лабуды и узнаешь сколько тебе еще тут отбывать",
                           reply_markup=generate_default_keyboard())

    await Form.active.set()


# Statistics handler
@dp.message_handler(commands=['fts'], user_id=186167695, state="*")
async def start(message: types.Message):
    statistics = get_statistics()
    await bot.send_message(message.chat.id, statistics, parse_mode="html", reply_markup=generate_default_keyboard())


# Time schedule handler
@dp.message_handler(filters.Text(equals=system_phrases["timetable"]), state=Form.active)
async def get_time_handler(message: types.Message):
    answer = get_timetable()
    await bot.send_message(message.chat.id, answer, parse_mode="html", reply_markup=generate_default_keyboard())
    update_time_used(message)


# Default handler
@dp.message_handler(state=Form.active)
async def get_time_handler(message: types.Message):
    answer = get_time()
    await bot.send_message(message.chat.id, answer, parse_mode="html", reply_markup=generate_default_keyboard())
    update_time_used(message)


# -----------END OF HANDLERS-----------
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down ..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
