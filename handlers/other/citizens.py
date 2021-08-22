from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter

from utils.misc.read_file import read_txt_file
from utils.db_api import db_api, tables
from utils.ages import models, ages_list
from utils.classes import kb_constructor, transaction, timer
import keyboards
import states
import re


@dp.message_handler(chat_id=-1001316092745, state="*", commands="citizens")
@dp.throttled(rate=1)
async def citizens_handler(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    session = db_api.Session(user_id=user_id)
    session.open_session()
    citizens_table: tables.Citizens = session.built_in_query(tables.Citizens)
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)

    time_left = timer.CitizenTimer.get_create_timer(citizens_table)

    keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
    keyboard = keyboard.create_citizens_keyboard(0)

    msg_text = read_txt_file("text/citizens")
    edit_msg = await message.answer(
        msg_text.format(
            citizens_table.population,
            citizens_table.capacity,
            *time_left,
            citizens_table.creation_queue
        ),
        reply_markup=keyboard
    )
    await state.update_data({
        "edit_msg": edit_msg
    })
    await states.Citizens.menu.set()
    session.close_session()


@dp.callback_query_handler(state=states.Citizens.menu)
async def citizens_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    edit_msg: types.Message = data.get("edit_msg")

    # sessions
    session = db_api.Session(user_id=user_id)
    session.open_session()

    citizens_table: tables.Citizens = session.built_in_query(tables.Citizens)
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)

    keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)

    age_model: models.Age = ages_list.AgesList.get_age_model(townhall_table.age)

    page_move = re.findall(r"page_(\d+)", callback.data)
    create_people = re.findall(r"create_people_(\d+)", callback.data)

    if page_move:
        page = int(page_move[0])
        keyboard = keyboard.create_citizens_keyboard(page)
        await edit_msg.edit_reply_markup(keyboard)

    elif create_people:
        creation_count = int(create_people[0])
        population = citizens_table.population
        creation_queue = citizens_table.creation_queue

        if creation_count + (population+creation_queue) > citizens_table.capacity:
            session.close_session()
            return await callback.answer("🏠 Мало места! Нужно больше домов.")

        base_price = age_model.citizen.create_price
        new_price = list(map(lambda x: x*creation_count, base_price))

        result = transaction.Transaction().subtract_resources(
            new_price, townhall_table
        )

        if result:
            citizens_table.creation_queue += creation_count
            timer.CitizenTimer.set_create_timer(
                citizens_table=citizens_table,
                create_time_sec=age_model.citizen.create_time_sec,
                creation_count=creation_count
            )

            msg_text = read_txt_file("text/citizens")
            time_left = timer.CitizenTimer.get_create_timer(citizens_table)
            edit_msg = await edit_msg.edit_text(
                text=msg_text.format(
                    citizens_table.population,
                    citizens_table.capacity,
                    *time_left,
                    citizens_table.creation_queue
                ),
                reply_markup=edit_msg.reply_markup
            )
            await state.update_data({"edit_msg": edit_msg})
        else:
            result = transaction.Transaction().get_max_create_num(base_price, townhall_table)
            if result != 0:
                await callback.message.reply(
                    "Тебе хватает только на <b>x{}</b> 👨🏼‍🌾".format(result))
            else:
                await callback.message.reply(
                    "У тебя закончились ресурсы."
                )

    elif callback.data == "citizens_info":
        msg_text = read_txt_file("text/citizens_info")
        await edit_msg.edit_text(
            text=msg_text,
            reply_markup=keyboards.citizens.kb_citizens_info
        )

    elif callback.data == "back_citizens":
        await edit_msg.edit_text(
            text=edit_msg.text,
            reply_markup=edit_msg.reply_markup
        )

    await callback.answer()
    session.close_session()


@dp.message_handler(IsReplyFilter(True), state=states.Citizens.menu)
@dp.throttled(rate=2)
async def reply_menu_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    edit_msg = data.get("edit_msg")

    session = db_api.Session(user_id=user_id)
    session.open_session()

    citizens_table: tables.Citizens = session.built_in_query(tables.Citizens)
    townhall_table: tables.TownHall = session.built_in_query(tables.TownHall)

    age_model: models.Age = ages_list.AgesList.get_age_model(townhall_table.age)

    if message.reply_to_message.message_id == edit_msg.message_id:
        make_unit = re.findall(r"(\d+)", message.text)

        if make_unit:
            creation_count = int(make_unit[0])
            population = citizens_table.population
            creation_queue = citizens_table.creation_queue

            if creation_count + (population + creation_queue) > citizens_table.capacity:
                session.close_session()
                return await message.reply("🏠 Мало места! Нужно больше домов.")

            base_price = age_model.citizen.create_price
            new_price = list(map(lambda x: x * creation_count, base_price))

            result = transaction.Transaction().subtract_resources(
                new_price, townhall_table
            )

            if result:
                citizens_table.creation_queue += creation_count
                timer.CitizenTimer.set_create_timer(
                    citizens_table=citizens_table,
                    create_time_sec=age_model.citizen.create_time_sec,
                    creation_count=creation_count
                )

                msg_text = read_txt_file("text/citizens")
                time_left = timer.CitizenTimer.get_create_timer(citizens_table)
                edit_msg = await edit_msg.edit_text(
                    text=msg_text.format(
                        citizens_table.population,
                        citizens_table.capacity,
                        *time_left,
                        citizens_table.creation_queue
                    ),
                    reply_markup=edit_msg.reply_markup
                )
                await state.update_data({"edit_msg": edit_msg})
            else:
                result = transaction.Transaction().get_max_create_num(base_price, townhall_table)
                if result != 0:
                    await message.reply(
                        "Тебе хватает только на <b>x{}</b> 👨🏼‍🌾".format(result))
                else:
                    await message.reply("У тебя закончились ресурсы.")

    session.close_session()
