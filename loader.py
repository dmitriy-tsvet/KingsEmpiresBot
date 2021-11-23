from aiogram import Bot, Dispatcher, types
import aiohttp
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config


PROXY_URL = "socks5://45.89.18.242:11951"
PROXY_AUTH = aiohttp.BasicAuth(
    login="xH6y1z", password="871xvl90fD"
)


bot = Bot(
    token=config.BOT_TOKEN,
    parse_mode=types.ParseMode.HTML,
)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
