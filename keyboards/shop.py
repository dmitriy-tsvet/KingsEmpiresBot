from aiogram import types

kb_shop = types.InlineKeyboardMarkup()

btn_items = types.InlineKeyboardButton(
    text="🍶 Предметы", callback_data="shop"
)

btn_money = types.InlineKeyboardButton(
    text="💰 Монеты", callback_data="shop"
)

btn_stock = types.InlineKeyboardButton(
    text="⚒ Ресурсы", callback_data="shop"
)

btn_donate = types.InlineKeyboardButton(
    text="💎 Донат", callback_data="shop"
)

kb_shop.add(btn_items)
kb_shop.row(btn_money, btn_stock)
kb_shop.add(btn_donate)
