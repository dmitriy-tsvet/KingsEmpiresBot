from loader import dp
from aiogram import types
from utils.models import base, ages
from utils.misc.read_file import read_txt_file
from keyboards.help import kb_help


@dp.message_handler(state="*", commands="help")
async def help_handler(message: types.Message):
    msg_text = read_txt_file("text/help")
    await message.answer(
        msg_text,
        reply_markup=kb_help
    )


@dp.message_handler(state="*", commands="products")
async def help_handler(message: types.Message):
    msg_text = read_txt_file("text/products")

    all_products = ages.Age.get_all_products()
    all_products_text = [product.name for product in all_products]
    text = ""
    for product in all_products_text:
        text += "▸ <i>{}</i>\n".format(product)

    await message.answer(
        msg_text.format(text)
    )


