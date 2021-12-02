from aiogram import Bot, Dispatcher, types
import aiohttp
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config


# PROXY_URL = ""
# PROXY_AUTH = aiohttp.BasicAuth(
#     login="", password=""
# )


bot = Bot(
    token=config.BOT_TOKEN,
    parse_mode=types.ParseMode.HTML,
)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
