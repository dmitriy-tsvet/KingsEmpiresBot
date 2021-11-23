import re
import random
import json
import copy

from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import IsReplyFilter
from aiogram.utils import exceptions

from utils.db_api.db_api2 import get_territory_table, update_table_data, get_townhall_table, get_units_table
from utils.misc.timer import set_capture_timer, get_time_left, get_tax_timer
from keyboards.campaigns import *
from states.territory import Territory
from utils.misc.read_file import read_txt_file
from utils.war_system import fight, riot
from utils.checkers import check_user_registration


@dp.message_handler(chat_id=615311497, state="*", commands="territory")
@dp.throttled(rate=1)
async def territory_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    territory_owned_temp = []

    if await check_user_registration(message, state) is True:
        return

    current_state = await state.get_state()

    if current_state == "Territory:riot":
        try:
            await message.delete()
        except exceptions.MessageCantBeDeleted:
            pass
        return

    territory_table = await get_territory_table(user_id)
    territory_names = territory_table["territory_names"]
    territory_owned = territory_table["territory_owned"]
    territory_state = territory_table["territory_state"]
    capturing_territory = territory_table["captured_territory"]
    territory_units = territory_table["territory_units"]

    # random_riot = random.choices([0, 1], [10, 90])[0]
    # if random_riot == 1:
    #     result = await riot(territory_owned, territory_units)
    #
    #     if result is not None:
    #         riot_msg = await message.answer(
    #             "В городе {} произошло восстание,\n"
    #             "если его не подавить, город будет утерян.\n\n"
    #             "Для подавления восстания\n"
    #             "нужно {} воинов.".format(
    #                 result["riot_territory"], result["units"],
    #             ),
    #             reply_markup=kb_riot
    #         )
    #         await state.set_data({
    #             "riot_msg": riot_msg,
    #             "riot_territory": result["riot_territory"],
    #             "units": result["units"]
    #         })
    #         await Territory.riot.set()
    #         return

    for i in territory_owned:
        if i is None:
            owner = "свободно"
            territory_owned_temp.append(owner)

        else:
            owner = "👑"
            territory_owned_temp.append(owner)

    if territory_state == "capture" and capturing_territory is not None:
        index = territory_names.index(capturing_territory)
        territory_owned_temp.remove(territory_owned_temp[index])
        territory_owned_temp.insert(index, "⚔ захват")

    random_territory_emoji = random.choices(["⛰", "🌲", "🌳", "🌊", "🧊", "🌋"], k=6)
    count_captured_territories = territory_owned_temp.count("👑")

    msg_text = read_txt_file("territory_start")
    edit_msg = await message.answer(
        text=msg_text.format(
            *random_territory_emoji,
            *territory_names,
            *territory_owned_temp,
            count_captured_territories
        ),
        reply_markup=kb_territory
    )

    await state.update_data({
        "edit_msg": edit_msg,
    })

    await Territory.menu.set()


@dp.callback_query_handler(state=Territory.menu)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    edit_msg = data.get("edit_msg")

    townhall_table = await get_townhall_table(user_id)

    territory_table = await get_territory_table(user_id)
    capture_timer = await get_time_left(territory_table["capture_timer"])
    territory_names = territory_table["territory_names"]
    territory_taxes = territory_table["territory_taxes"]
    territory_owned = territory_table["territory_owned"]
    territory_units = territory_table["territory_units"]
    territory_state = territory_table["territory_state"]
    fight_state = territory_table["fight_state"]

    if callback.data == "capture":

        if capture_timer > 0:
            await edit_msg.edit_text(
                text="<b>⚔ Территория</b>\n"
                     "<code>◄ Захват территории. ►</code>\n\n"
                     "Вы захватываете территорию.\n\n"
                     "<code>Осталось: {} мин.</code>".format(capture_timer),
                reply_markup=kb_lobby
            )

            return await Territory.lobby.set()

        elif capture_timer <= 0 and territory_state == "capture":

            if fight_state == "win":
                await edit_msg.edit_text(
                    text="<b>⚔ Территория</b>\n"
                         "<code>◄ Захват территории. ►</code>\n\n"
                         "Вы захватили территорию!\n\n",
                    reply_markup=kb_lobby
                )

            else:
                await edit_msg.edit_text(
                    text="<b>⚔ Территория</b>\n"
                         "<code>◄ Захват территории. ►</code>\n\n"
                         "Вы проиграли сражение!\n\n",
                    reply_markup=kb_lobby
                )

            await update_table_data(
                user_id=user_id,
                data={
                    "territory_state": None,
                    "fight_state": None,
                    "captured_territory": None
                },
                table="territory"
            )
            return await Territory.lobby.set()

        y = 0
        kb_capture_clone = copy.deepcopy(kb_capture_territories)

        for i in territory_names:
            btn_text = i

            index = territory_names.index(i)
            if territory_owned[index] is not None:
                btn_text = "—"

            btn_territory = types.InlineKeyboardButton(
                text=btn_text, callback_data=i
            )

            if y == 2:
                y = 1
                kb_capture_clone.add(
                    btn_territory
                )
                continue
            kb_capture_clone.insert(
                btn_territory
            )
            y += 1

        kb_capture_clone.add(btn_back_menu_territory)

        await edit_msg.edit_text(
            text="<b>⚔ Территория</b>\n"
                 "<code>◄ Подготовка захвата. ►</code>\n\n"
                 "<i>Выберите территорию для захвата.</i>\n"
                 "▸▹▹",
            reply_markup=kb_capture_clone
        )

        await state.update_data({
            "territory_names": territory_names,
            "territory_taxes": territory_taxes,
            "territory_owned": territory_owned,
            "territory_units": territory_units,

        })
        await Territory.select_territory.set()

    elif callback.data == "get_tax":
        if territory_state == "capture":
            return await callback.answer(
                "Нельзя собрать налог, во время захвата."
            )

        tax = await get_tax_timer(user_id)

        money = townhall_table["money"] + tax
        await update_table_data(
            user_id=user_id,
            data={
                "money": money
            })

        await callback.answer("+ {} 💰".format(tax))


@dp.callback_query_handler(state=Territory.riot)
async def riot_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    units_need = data.get("units")
    riot_territory = data.get("riot_territory")
    riot_msg = data.get("riot_msg")

    user_id = callback.from_user.id

    units_table = await get_units_table(user_id)
    player_units = units_table["units_count"]

    territory_table = await get_territory_table(user_id)
    territory_names = territory_table["territory_names"]
    territory_owned = territory_table["territory_owned"]
    index = territory_names.index(riot_territory)

    if callback.data == "suppress_riot":

        if player_units >= units_need:
            await callback.answer("")
            player_units -= units_need
            await update_table_data(
                user_id=user_id,
                data={
                    "units_count": player_units
                },
                table="units"
            )
            await riot_msg.edit_text(
                "Вы успешно подавили восстание!"
            )
            await Territory.menu.set()

        else:
            await callback.answer("Вам не хватает воинов.")

    elif callback.data == "lose_riot":
        await callback.answer("")
        territory_owned.remove(riot_territory)
        territory_owned.insert(index, None)
        territory_owned = json.dumps(territory_owned, ensure_ascii=False)

        await update_table_data(
            user_id=user_id,
            data={
                "territory_owned": territory_owned
            },
            table="territory"
        )
        await riot_msg.edit_text(
            "Территория {} была потеряна.".format(riot_territory)
        )

        await Territory.menu.set()


@dp.callback_query_handler(state=Territory.lobby)
async def capture_in_process_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")

    if callback.data == "back_menu_territory":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup
        )
        await Territory.menu.set()
        return


@dp.callback_query_handler(state=Territory.select_territory)
async def capture_territory_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")

    if callback.data == "back_menu_territory":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup
        )
        await Territory.menu.set()
        return

    territory_names = data.get("territory_names")
    territory_owned = data.get("territory_owned")

    if callback.data in (territory_names and territory_owned):
        return await callback.answer(
            "Недоступно"
        )

    replied_msg = await edit_msg.edit_text(
        text="<b>⚔ Территория</b>\n"
             "<code>◄ Подготовка захвата. ►</code>\n\n"
             "💂 Бойцов | 0\n\n"
             "<i>Напишите кол-во бойцов, ответив\n"
             "на это сообщение или выберите.</i>\n"
             "▸▸▹",
        reply_markup=kb_units_count_select
    )

    await state.update_data({
        "replied_msg": replied_msg,
        "territory": callback.data,
        "selected_player_units": 0
    })
    await Territory.select_count_units.set()


@dp.callback_query_handler(state=Territory.select_count_units)
async def count_units_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")
    territory = data.get("territory")
    user_id = callback.from_user.id

    territory_names = data.get("territory_names")
    territory_taxes = data.get("territory_taxes")
    territory_units = data.get("territory_units")
    selected_player_units = data.get("selected_player_units")

    units_table = await get_units_table(user_id)
    player_units = units_table["units_count"]

    index = territory_names.index(territory)

    if callback.data == "add_one_unit":
        selected_player_units += 1
    elif callback.data == "add_ten_units":
        selected_player_units += 10
    elif callback.data == "add_hundred_units":
        selected_player_units += 100

    if selected_player_units > player_units:
        return await callback.answer("У вас нету такого кол-ва воинов.")

    await state.update_data({
        "index": index,
        "player_units": player_units,
        "selected_player_units": selected_player_units
    })

    if callback.data == "capture_ready":
        if selected_player_units == 0:
            await callback.answer(
                "Вам нужен хотя-бы 1 боец!",
                show_alert=True
            )
            return

        msg_text = read_txt_file("territory_info")
        await edit_msg.edit_text(
            text=msg_text.format(
                territory, territory_taxes[index],
                territory_units[index], selected_player_units
            ),
            reply_markup=kb_start_capture,
        )

        await Territory.capture_territory.set()
        return

    await edit_msg.edit_text(
        text="<b>⚔ Территория</b>\n"
             "<code>◄ Подготовка захвата. ►</code>\n\n"
             "💂 Бойцов | {}\n\n"
             "<i>Напишите кол-во бойцов, ответив\n"
             "на это сообщение или выберите.</i>\n"
             "▸▸▹".format(selected_player_units),
        reply_markup=kb_units_count_select,
    )


@dp.message_handler(IsReplyFilter(True), state=Territory.select_count_units)
@dp.throttled(rate=1)
async def count_units_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    edit_msg = data.get("edit_msg")
    replied_msg = data.get("replied_msg")

    if message.reply_to_message.message_id != replied_msg.message_id:
        return

    user_id = message.from_user.id
    units_table = await get_units_table(user_id)
    player_units = units_table["units_count"]

    selected_player_units = data.get("selected_player_units")
    if selected_player_units is None:
        selected_player_units = 0

    num_selected_units = re.findall(r"\d+", message.text)

    if not num_selected_units:
        return
    else:
        num_selected_units = int(num_selected_units[0])

    if num_selected_units > player_units:
        return await message.reply("У вас нету такого кол-ва воинов.")

    selected_player_units += num_selected_units

    await state.update_data({"selected_player_units": selected_player_units})

    await edit_msg.edit_text(
        text="<b>⚔ Территория</b>\n"
             "<code>◄ Подготовка захвата. ►</code>\n\n"
             "💂 Бойцов | {}\n\n"
             "<i>Напишите кол-во бойцов, ответив\n"
             "на это сообщение или выберите.</i>\n"
             "▸▸▹".format(selected_player_units),
        reply_markup=kb_units_count_select,
    )


@dp.callback_query_handler(state=Territory.capture_territory)
async def count_units_handler(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    edit_msg = data.get("edit_msg")

    if callback.data == "cancel_capture":
        await edit_msg.edit_text(
            text=edit_msg.html_text,
            reply_markup=edit_msg.reply_markup
        )
        return await Territory.menu.set()

    if callback.data == "start_capture":
        territory_owned = data.get("territory_owned")
        territory_units = data.get("territory_units")

        territory = data.get("territory")
        player_units = data.get("player_units")
        selected_player_units = data.get("selected_player_units")
        player_units -= selected_player_units

        index = data.get("index")

        winner = await fight(player_units, territory_units[index])
        timer = await set_capture_timer(user_id)

        if winner == "attacker":
            territory_owned.remove(territory_owned[index])
            territory_owned.insert(index, territory)
            territory_owned = json.dumps(territory_owned, ensure_ascii=False)

            await update_table_data(
                user_id=user_id,
                data={
                    "territory_owned": territory_owned,
                    "fight_state": "win",
                    "territory_state": "capture",
                    "captured_territory": territory
                },
                table="territory")
        else:
            await update_table_data(
                user_id=user_id,
                data={
                    "territory_state": "capture",
                    "captured_territory": territory,

                },
                table="territory")

        await update_table_data(
            user_id=user_id,
            data={
                "units_count": player_units,
            },
            table="units")

        await edit_msg.edit_text(
            text="<b>⚔ Территория</b>\n"
                 "<code>◄ Захват территории. ►</code>\n\n"
                 "Вы захватываете {}.\n\n"
                 "Захват будет окончен,"
                 "через: {} мин.".format(territory, timer),
            reply_markup=kb_lobby
        )
        await Territory.lobby.set()
        return
