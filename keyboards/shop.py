from aiogram import types

kb_shop = types.InlineKeyboardMarkup()

btn_items = types.InlineKeyboardButton(
    text="🗃 Сундуки", callback_data="shop_chest"
)

btn_money = types.InlineKeyboardButton(
    text="💰 Монеты", callback_data="shop_money"
)

btn_stock = types.InlineKeyboardButton(
    text="⚒ Ресурсы", callback_data="shop_stock"
)

btn_donate = types.InlineKeyboardButton(
    text="💎 Донат", callback_data="shop_donate"
)

kb_shop.add(btn_items)
kb_shop.row(btn_money, btn_stock)
kb_shop.add(btn_donate)

btn_back = types.InlineKeyboardButton(
    text="назад", callback_data="back_shop"
)

kb_donate = types.InlineKeyboardMarkup()

btn_go_to_donate = types.InlineKeyboardButton(
    text="купить 💎", url="https://t.me/KingsEmpiresDonateBot"
)

kb_donate.add(btn_go_to_donate)
kb_donate.add(btn_back)

kb_buy_chest = types.InlineKeyboardMarkup()

btn_buy_chest = types.InlineKeyboardButton(
    text="🔑 открыть", callback_data="buy_chest"
)

btn_back_chest = types.InlineKeyboardButton(
    text="назад", callback_data="back_chest"
)

kb_buy_chest.add(btn_buy_chest)
kb_buy_chest.add(btn_back_chest)

kb_url_private_chat = types.InlineKeyboardMarkup()
btn_url_private_chat = types.InlineKeyboardButton(
    text="перейти", url="https://t.me/KingsEmpiresBot"
)
kb_url_private_chat.add(btn_url_private_chat)