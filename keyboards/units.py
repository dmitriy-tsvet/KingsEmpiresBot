from aiogram import types

kb_back_units = types.InlineKeyboardMarkup()

btn_back_units = types.InlineKeyboardButton(
    text="назад", callback_data="back_units"
)

kb_back_units.add(btn_back_units)