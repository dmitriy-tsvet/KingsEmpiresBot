import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from sqlalchemy import or_

import random
import keyboards
import states
from loader import dp
from utils.classes import kb_constructor, paint, capture
from utils.db_api import tables, db_api
from utils.misc.read_file import read_txt_file
from utils.classes.regexps import ContestRegexp
from utils.classes import timer

color = {
    "red": "❤",
    "blue": "💙"
}


@dp.message_handler(state="*", commands="contest")
async def territory_handler(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    user_id = message.from_user.id

    session = db_api.CreateSession()

    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).join(tables.Clan).first()

    if clan_member is None:
        msg_text = read_txt_file("text/contest/without_clan")
        session.close()
        return await message.reply(msg_text)
    elif clan_member.clan.state != "contest":
        msg_text = read_txt_file("text/contest/none_contest")
        session.close()
        return await message.reply(msg_text)

    contest: tables.Contest = session.db.query(
        tables.Contest).filter(or_(
            tables.Contest.clan_id_1 == clan_member.clan_id,
            tables.Contest.clan_id_2 == clan_member.clan_id)
    ).first()

    territory_capturing = [i for i in contest.territory_captures if i is not None]
    territory_captures = list(contest.territory_captures)
    territory_owners = list(contest.territory_owners)
    territory_units = list(contest.territory_units)

    for capture in territory_capturing:
        time_left = timer.Timer.get_left_time(capture["timer"])
        if time_left[0] == 0:

            if capture["win"]:
                recent_log = list(contest.recent_log)

                log = list(contest.log)

                if len(recent_log) >= 6:
                    recent_log.remove(recent_log[0])

                clans = [contest.clan_id_1, contest.clan_id_2]
                new_log = "{} {} ({}) захватил(а) {}".format(
                    color[contest.colors[clans.index(clan_member.clan_id)]],
                    message.from_user.get_mention(), clan_member.clan.name,
                    contest.territory_names[territory_captures.index(capture)]
                )
                recent_log.append(new_log)
                log.append(new_log)

                contest.recent_log = recent_log
                contest.log = log

                territory_owners[territory_captures.index(capture)] = clan_member.clan_id
                territory_units[territory_captures.index(capture)] = capture["units_count"]
                territory_captures[territory_captures.index(capture)] = None

                contest.territory_captures = territory_captures
                contest.territory_owners = territory_owners
                contest.territory_units = territory_units

            else:
                recent_log = list(contest.recent_log)
                log = list(contest.log)

                if len(recent_log) >= 6:
                    recent_log.remove(recent_log[0])

                clans = [contest.clan_id_1, contest.clan_id_2]
                new_log = "{} {} ({}) проиграл(а) на {}".format(
                    color[contest.colors[clans.index(clan_member.clan_id)]],
                    message.from_user.get_mention(), clan_member.clan.name,
                    contest.territory_names[territory_captures.index(capture)]
                )
                recent_log.append(new_log)
                log.append(new_log)
                contest.recent_log = recent_log
                contest.log = log

                territory_captures[territory_captures.index(capture)] = None
                contest.territory_captures = territory_captures

    text_log = ""
    for i in contest.recent_log:
        text_log += "- {}\n".format(i)

    paint.PaintMap.paint_contest(contest=contest)

    with open("data/img/contest/map.jpg", 'rb') as photo:
        sticker_msg = await message.answer_photo(
            photo=photo,
        )

    msg_text = read_txt_file("text/contest/contest")

    contest_msg = await sticker_msg.reply(
        text=msg_text.format(
            color[contest.colors[0]],
            contest.clan_1.name,
            color[contest.colors[1]],
            contest.clan_2.name,
            text_log
        ),
        reply_markup=keyboards.contest.kb_contest
    )
    await state.update_data({
        "user_id": user_id,
        "contest_msg": contest_msg
    })
    session.close()


@dp.callback_query_handler(state="*", regexp=ContestRegexp.back)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    contest_msg: types.Message = data.get("contest_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    if callback.data == "back_contest":
        await contest_msg.edit_text(
            text=contest_msg.html_text,
            reply_markup=contest_msg.reply_markup,
        )
    await callback.answer()


@dp.callback_query_handler(state="*", regexp=ContestRegexp.capture)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    contest_msg: types.Message = data.get("contest_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()
    territory_index = re.findall(r"territory_(\d+)", callback.data)

    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).first()

    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

    contest: tables.Contest = session.db.query(
        tables.Contest).filter(or_(
            tables.Contest.clan_id_1 == clan_member.clan_id,
            tables.Contest.clan_id_2 == clan_member.clan_id)
    ).first()

    if callback.data == "select_capture_territory":
        lose_dialogs = [
            "Силы врага превосходят нас, мы\n"
            "теряем много бойцов.", "У нас много потерь..."
        ]
        win_dialogs = [
            "Глядите на этих трусов, они\n"
            "бегут с поля битвы.", "У них нет шансов."
        ]

        type_dialog = {
            True: win_dialogs,
            False: lose_dialogs
        }

        for capture in contest.territory_captures:
            if capture is None:
                continue

            index = contest.territory_captures.index(capture)
            if capture["user_id"] == user_id:
                dialog = random.choice(type_dialog[capture["win"]])

                msg_text = read_txt_file("text/contest/capturing")
                await contest_msg.edit_text(
                    text=msg_text.format(
                        contest.territory_names[index],
                        dialog,
                        *timer.Timer.get_left_time(capture["timer"])
                    ),
                    reply_markup=keyboards.contest.kb_back
                )
                return
        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_contest_territories_keyboard()

        msg_text = read_txt_file("text/contest/select_territory")
        await contest_msg.edit_text(
            text=msg_text.format(msg_text),
            reply_markup=keyboard
        )

    elif territory_index:
        index = int(territory_index[0])

        msg_text = read_txt_file("text/contest/select_units")
        all_unit_counts = sum(units.units_count)
        capture_units_msg = await contest_msg.edit_text(
            text=msg_text.format(
                all_unit_counts,
            ),
            reply_markup=keyboards.contest.kb_back
        )
        await state.update_data({
            "capture_units_count": 0,
            "territory_index": index,
            "capture_units_msg": capture_units_msg
        })
        await states.Contest.set_capture_units.set()

    session.close()


@dp.message_handler(IsReplyFilter(True), state=states.Contest.set_capture_units, regexp=r"(\d+)")
async def set_capture_units_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    contest_msg: types.Message = data.get("contest_msg")
    territory_index = data.get("territory_index")
    count = int(message.text)

    if count < 1:
        return
    session = db_api.CreateSession()

    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).first()

    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

    contest: tables.Contest = session.db.query(
        tables.Contest).filter(or_(
            tables.Contest.clan_id_1 == clan_member.clan_id,
            tables.Contest.clan_id_2 == clan_member.clan_id)
    ).first()

    all_unit_counts = sum(units.units_count) + clan_member.clan_units
    if count > all_unit_counts:
        await message.reply(
            text="У тебя только x{} 💂".format(all_unit_counts)
        )
        return session.close()

    msg_text = read_txt_file("text/contest/start_capture")

    keyboard = kb_constructor.StandardKeyboard(
        user_id=user_id).create_start_capture_keyboard(
        contest.territory_units[territory_index])

    await contest_msg.edit_text(
        text=msg_text.format(
            contest.territory_names[territory_index],
            contest.territory_units[territory_index],
            count
        ),
        reply_markup=keyboard
    )

    await state.update_data({
        "capture_units_count": data["capture_units_count"] + count
    })

    await message.delete()
    await states.Contest.start_capture.set()
    session.close()


@dp.callback_query_handler(state=states.Contest.start_capture)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    contest_msg: types.Message = data.get("contest_msg")
    territory_index = data.get("territory_index")
    capture_units_count = data.get("capture_units_count")
    user_id = callback.from_user.id
    session = db_api.CreateSession()
    explore = re.findall(r"explore_price_(\d+)", callback.data)

    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()

    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).join(tables.Clan).first()

    contest: tables.Contest = session.db.query(
        tables.Contest).filter(or_(
            tables.Contest.clan_id_1 == clan_member.clan_id,
            tables.Contest.clan_id_2 == clan_member.clan_id)).first()

    if callback.data == "start_capture":
        if contest.territory_captures[territory_index] is not None:
            session.close()
            return callback.answer(
                text="Упс, кто-то уже начала захват этой территории."
            )

        time_set = timer.Timer.set_timer(60)

        win_status: bool = capture.Capture(
            capture_units_count,
            contest.territory_units[territory_index]
        ).is_win()

        capture_log = {
            "user_id": user_id,
            "units_count": capture_units_count,
            "timer": time_set,
            "win": win_status
        }

        recent_log = list(contest.recent_log)
        log = list(contest.log)

        if len(recent_log) >= 6:
            recent_log.remove(recent_log[0])

        clans = [contest.clan_id_1, contest.clan_id_2]
        new_log = "{} {} ({}) <b>начал(а) захват</b> {}".format(
            color[contest.colors[clans.index(clan_member.clan_id)]],
            callback.from_user.get_mention(), clan_member.clan.name,
            contest.territory_names[territory_index]
        )
        recent_log.append(new_log)
        log.append(new_log)
        contest.recent_log = recent_log
        contest.log = log

        territory_captures = list(contest.territory_captures)
        territory_captures[territory_index] = capture_log
        contest.territory_captures = territory_captures

        await contest_msg.edit_text(
            text=contest_msg.text,
            reply_markup=contest_msg.reply_markup
        )
        await state.reset_state(with_data=False)

    elif explore:
        explore_price = int(explore[0])
        if townhall.money < explore_price:
            session.close()
            msg_text = read_txt_file("text/hints/few_money")
            return await callback.answer(msg_text)

        townhall.money -= explore_price
        percent = capture.Capture(
            capture_units_count, contest.territory_units[territory_index]
        ).scouting()
        return await callback.answer("{} %".format(percent))

    session.close()


@dp.callback_query_handler(state="*", regexp=ContestRegexp.camp)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    contest_msg: types.Message = data.get("contest_msg")

    if data.get("user_id") != user_id:
        return await callback.answer("Не трогай чужое!")

    session = db_api.CreateSession()
    camp= re.findall(r"camp_(\d+)", callback.data)

    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).first()

    contest: tables.Contest = session.db.query(
        tables.Contest).filter(or_(
            tables.Contest.clan_id_1 == clan_member.clan_id,
            tables.Contest.clan_id_2 == clan_member.clan_id)
    ).first()

    if callback.data == "select_camp":
        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_camp_keyboard()

        camps_msg = await contest_msg.edit_text(
            text="Ваши лагеря.",
            reply_markup=keyboard
        )
        await state.update_data({
            "camps_msg": camps_msg
        })
        # await states.Contest.set_capture_units.set()
    elif camp:
        index = int(camp[0])
        await contest_msg.edit_text(
            text="🏕 Лагерь {}\n"
                 "Юнитов: {}".format(contest.territory_names[index], contest.territory_units[index]),
            reply_markup=keyboards.contest.kb_back
        )
        await state.update_data({
            "camp_index": index
        })
        await states.Contest.add_units_in_camp.set()


@dp.message_handler(IsReplyFilter(True), state=states.Contest.add_units_in_camp, regexp=r"(\d+)")
async def set_capture_units_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    contest_msg: types.Message = data.get("contest_msg")
    count = int(message.text)
    camp_index = data.get("camp_index")

    if count < 1:
        return

    session = db_api.CreateSession()

    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).first()

    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

    contest: tables.Contest = session.db.query(
        tables.Contest).filter(or_(
            tables.Contest.clan_id_1 == clan_member.clan_id,
            tables.Contest.clan_id_2 == clan_member.clan_id)
    ).first()
    all_unit_counts = sum(units.units_count)
    if count > all_unit_counts:
        await message.reply(
            text="У тебя только x{} 💂".format(all_unit_counts)
        )
        return session.close()

    territory_units = list(contest.territory_units)
    territory_units[camp_index] += count
    contest.territory_units = territory_units
    session.db.commit()

    await contest_msg.edit_text(
        text="🏕 Лагерь {}\n"
             "Юнитов: {}".format(
            contest.territory_names[camp_index],
            contest.territory_units[camp_index]),
        reply_markup=keyboards.contest.kb_back
    )

    session.close()
