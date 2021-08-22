from loader import dp, bot
from aiogram import types
from filters.is_join_group import IsGroupJoin
from utils.misc.read_file import read_txt_file


@dp.my_chat_member_handler(IsGroupJoin(True))
async def join_group_handler(my_chat_member: types.ChatMemberUpdated):

    sticker = read_txt_file("sticker/join_group")
    await bot.send_sticker(
        my_chat_member.chat.id,
        sticker=sticker
    )

    msg_text = read_txt_file("text/join_group")
    await bot.send_message(
        my_chat_member.chat.id,
        text=msg_text
    )


