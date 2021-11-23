from aiogram import types

kb_help = types.InlineKeyboardMarkup()

btn_article = types.InlineKeyboardButton(
    text="✨ тык", url="https://telegra.ph/Kings-of-Empires-Bot-11-13"
)

kb_help.add(btn_article)


