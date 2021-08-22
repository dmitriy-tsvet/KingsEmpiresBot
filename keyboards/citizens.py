from aiogram import types

btn_info = types.InlineKeyboardButton(
    text="🔅 инфо", callback_data="citizens_info"
)

btn_back = types.InlineKeyboardButton(
    text="назад", callback_data="back_citizens"
)

kb_citizens_info = types.InlineKeyboardMarkup()
kb_citizens_info.add(btn_back)




