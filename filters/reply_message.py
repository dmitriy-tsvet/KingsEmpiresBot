from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsReplyMessage(BoundFilter):
    key = 'is_reply'

    def __init__(self, is_reply):
        self.is_reply = is_reply

    async def check(self, msg: types.Message):
        if msg.reply_to_message and self.is_reply:
            return {'reply': msg.reply_to_message}
        elif not msg.reply_to_message and not self.is_reply:
            return True
