from aiogram import types

btn_my_products = types.InlineKeyboardButton(
    text="твоё", callback_data="my_products"
)

btn_buy_product = types.InlineKeyboardButton(
    text="купить", callback_data="buy_product"
)

btn_delete_product = types.InlineKeyboardButton(
    text="удалить", callback_data="delete_product"
)

btn_back_market = types.InlineKeyboardButton(
    text="назад", callback_data="back_market"
)
