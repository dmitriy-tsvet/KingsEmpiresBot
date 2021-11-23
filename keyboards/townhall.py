from aiogram import types


btn_get_energy = types.InlineKeyboardButton(
    text="+ ⚡", callback_data="get_energy"
)

btn_get_graviton = types.InlineKeyboardButton(
    text="+ 🧬", callback_data="get_graviton"
)

btn_storage = types.InlineKeyboardButton(
    text="🍯 склад", callback_data="storage"
)

btn_progress = types.InlineKeyboardButton(
    text="✨ прогресс", callback_data="progress"
)


kb_progress = types.InlineKeyboardMarkup()

# btn_age = types.InlineKeyboardButton(
#     text="▲ Век", callback_data="next_age"
# )
#

btn_one_progress = types.InlineKeyboardButton(
    text="+ 🧬", callback_data="upgrade_one"
)

btn_all_progress = types.InlineKeyboardButton(
    text="+ 🧬🧬", callback_data="upgrade_all"
)

btn_open_tech = types.InlineKeyboardButton(
    text="открыть", callback_data="unlock_tech"
)

btn_back_townhall = types.InlineKeyboardButton(
    text="назад", callback_data="back_townhall"
)

btn_next_age = types.InlineKeyboardButton(
    text="🌟 Бронзовый Век", callback_data="unlock_age"
)

kb_storage = types.InlineKeyboardMarkup()
# kb_storage.add(btn_back_townhall)

