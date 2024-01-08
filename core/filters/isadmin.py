from aiogram.filters import BaseFilter
from aiogram.types import Message
import os
from Aiogram.games_bot.core.utils.dbconnect import Database

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message):
        db = Database(os.getenv('DATABASE'))
        users = db.select_user_id(message.from_user.id)
        return users[3] in os.getenv('ADMINS')