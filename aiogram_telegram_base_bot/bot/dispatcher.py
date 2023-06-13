from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aioredis import Redis

from settings import BOT_TOKEN, REDIS_URL


storage = RedisStorage.from_url(REDIS_URL) if REDIS_URL else MemoryStorage()
redis: Redis = Redis.from_url(REDIS_URL)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=storage)

