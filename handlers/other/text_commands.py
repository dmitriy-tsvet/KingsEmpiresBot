from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
import re
from utils.misc.read_file import read_txt_file

from utils.db_api import tables, db_api
from utils.misc.operation_with_lists import subtract_nums_list, add_nums_list

forwarding_units = r"отправить (\d+)\s(воинов|воина)"


@dp.message_handler(filters.IsReplyFilter(True), regexp=forwarding_units, state="*")
async def forwarding_units_handler(message: types.Message, state: FSMContext):
    replied_user_id = message.reply_to_message.from_user.id
    user_id = message.from_user.id

    print(await state.get_state())
    replied_mention = message.reply_to_message.from_user.get_mention()
    mention = message.from_user.get_mention()

    is_bot = message.reply_to_message.from_user.is_bot
    if replied_user_id != user_id and not is_bot:

        count_forward_units = int(re.findall(r"(\d+)", message.text)[0])

        if count_forward_units < 1:
            return message.reply(
                "😿 А почему так мало?"
            )

        session_1 = db_api.Session(user_id=user_id)
        session_2 = db_api.Session(user_id=replied_user_id)

        session_1.open_session()
        session_2.open_session()

        units_table_1: tables.Units = session_1.built_in_query(tables.Units)
        units_table_2: tables.Units = session_2.built_in_query(tables.Units)

        if count_forward_units > units_table_1.all_unit_counts:
            await message.reply("У тебя нету такого количества воинов.")
        else:
            units_table_1.all_unit_counts -= count_forward_units
            units_count_1 = list(units_table_1.unit_counts)
            units_table_1.unit_counts = subtract_nums_list(
                count_forward_units, units_count_1
            )
            units_table_2.all_unit_counts += count_forward_units
            units_count_2 = list(units_table_2.unit_counts)

            units_table_2.unit_counts = add_nums_list(
                count_forward_units, units_count_2
            )

            sticker = read_txt_file("sticker/forward_units")

            await message.answer_sticker(sticker=sticker)
            await message.answer(
                "<i>{} высылает боевую поддержку {},\n"
                "в размере 💂 {} воинов.</i>".format(
                    mention, replied_mention, count_forward_units
                ))

        session_1.close_session()
        session_2.close_session()
