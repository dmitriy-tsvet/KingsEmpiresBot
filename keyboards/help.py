from aiogram import types

kb_help = types.InlineKeyboardMarkup()

btn_article = types.InlineKeyboardButton(
    text="✨ тык", url="https://telegra.ph/Gajd-po-sozdaniyu-svoej-strany-07-18"
)

kb_help.add(btn_article)


