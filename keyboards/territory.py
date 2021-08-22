from aiogram import types

btn_back_territory = types.InlineKeyboardButton(
    text="назад", callback_data="back_territory"
)

btn_next = types.InlineKeyboardButton(
    text="дальше", callback_data="waiting_capture"
)

kb_territory = types.InlineKeyboardMarkup()

btn_capture = types.InlineKeyboardButton(
    text="⚔ Захват", callback_data="capture"
)

btn_get_tax = types.InlineKeyboardButton(
    text="+ 💰", callback_data="get_tax"
)

kb_territory.add(btn_get_tax)
kb_territory.add(btn_capture)


kb_waiting_capture = types.InlineKeyboardMarkup()

btn_start_capture = types.InlineKeyboardButton(
    text="⚔ Начать Захват!", callback_data="start_capture"
)

kb_waiting_capture.add(btn_start_capture)
kb_waiting_capture.add(btn_back_territory)

kb_capturing = types.InlineKeyboardMarkup()
kb_capturing.add(btn_back_territory)

kb_riot = types.InlineKeyboardMarkup()
btn_suppress_riot = types.InlineKeyboardButton(
    text="🩸 Подавить восстание", callback_data="suppress_riot"
)

btn_lose_riot = types.InlineKeyboardButton(
    text="сдаться", callback_data="lose_riot"
)

kb_riot.add(btn_suppress_riot)
kb_riot.add(btn_lose_riot)

