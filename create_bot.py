from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='5924096654:AAEVom8UILPL45nsRornVAhgsmOuGg5dmZY')
dp = Dispatcher(bot, storage=storage)