from aiogram import types

btn_get_tax = types.InlineKeyboardButton(
    text="+ 💰", callback_data="get_money"
)
btn_get_food = types.InlineKeyboardButton(
    text="+ 🍇", callback_data="get_food"
)
btn_get_stock = types.InlineKeyboardButton(
    text="+ 🌲", callback_data="get_stock"
)

btn_get_energy = types.InlineKeyboardButton(
    text="+ ⚡", callback_data="get_energy"
)

btn_get_graviton = types.InlineKeyboardButton(
    text="+ 🧬", callback_data="get_graviton"
)

btn_population = types.InlineKeyboardButton(
    text="📦 склад", callback_data="storage"
)

btn_progress = types.InlineKeyboardButton(
    text="✨ прогресс", callback_data="progress"
)


kb_progress = types.InlineKeyboardMarkup()

btn_age = types.InlineKeyboardButton(
    text="▲ Век", callback_data="next_age"
)

btn_back_townhall = types.InlineKeyboardButton(
    text="назад", callback_data="back_townhall"
)

kb_progress.add(btn_age)
kb_progress.add(btn_back_townhall)

kb_storage = types.InlineKeyboardMarkup()
kb_storage.add(btn_back_townhall)