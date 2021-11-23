import typing

import keyboards
import states
import re
import copy
import random

from loader import dp
from aiogram import types
from aiogram.dispatcher import filters
from aiogram import exceptions

from aiogram.dispatcher import FSMContext
from utils.misc.read_file import read_txt_file
from utils.db_api import tables, db_api
from utils.models import ages, models
from utils.classes import kb_constructor, timer, transaction
from utils.war_system import fight
from utils.misc.operation_with_lists import subtract_nums_list
from sqlalchemy import asc, desc, and_
from utils.misc.regexps import ClanRegexp

from data import config


@dp.message_handler(state="*", commands="clan")
async def territory_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    # sessions
    session = db_api.CreateSession()

    # tables data
    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).join(tables.Clan).first()

    if clan_member is None:
        msg_text = read_txt_file("text/clan/without_clan")
        clan_msg = await message.answer(
            text=msg_text,
            reply_markup=keyboards.clan.kb_none_clan
        )
        await state.update_data({
            "user_id": user_id,
            "clan_msg": clan_msg
        })

        session.close()
        return

    clan_members: typing.List[tables.ClanMember] = session.db.query(
        tables.ClanMember).filter_by(clan_id=clan_member.clan_id).all()

    clan_creator: tables.User = session.db.query(
        tables.User).filter_by(user_id=clan_member.clan.creator).first()

    keyboard = kb_constructor.StandardKeyboard(user_id=user_id).create_clan_keyboard()
    msg_text = read_txt_file("text/clan/in_clan")
    clan_msg = await message.answer(
        text=msg_text.format(
            clan_member.clan.name,
            clan_member.clan.description[:21],
            clan_member.clan.rating,
            clan_creator.first_name,
            len(clan_members),
            clan_member.rank),
        reply_markup=keyboard
    )

    await state.update_data({
        "user_id": user_id,
        "clan_msg": clan_msg
    })
    session.close()


@dp.callback_query_handler(state="*", regexp=ClanRegexp.back)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    clan_msg: types.Message = data.get("clan_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    await clan_msg.edit_text(
        text=clan_msg.html_text,
        reply_markup=clan_msg.reply_markup,
    )


@dp.callback_query_handler(state="*", regexp=ClanRegexp.without_clan)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    clan_msg: types.Message = data.get("clan_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    # sessions
    session = db_api.CreateSession()

    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()

    if callback.data == "create_clan":
        if townhall.money >= 5000:
            townhall.money -= 5000
        else:
            await callback.answer(
                "Вам не хватает {} 💰".format(
                    5000 - townhall.money)
            )
            session.close()
            return

        clan_msg = await clan_msg.edit_text(
            text="Придумайте названия для своего клана.\n"
                 "<i>Ответив на это сообщение.</i>"
        )
        await state.update_data({
            "message_id": clan_msg.message_id
        })
        await states.Clan.set_name.set()

    elif callback.data == "clans_rating":
        clan_table: typing.List[tables.Clan] = session.db.query(
            tables.Clan).order_by(desc(tables.Clan.rating)).all()

        text = ""
        num = 1
        for clan in clan_table[:10]:
            text += "{}. {} [ {} ⭐ ]\n".format(num, clan.name, clan.rating)
            num += 1

        await clan_msg.edit_text(
            text=text,
            reply_markup=keyboards.clan.kb_back
        )

    elif callback.data == "clan_invitation":
        keyboard = kb_constructor.PaginationKeyboard(user_id=user_id)
        keyboard = keyboard.create_invitation_keyboard()

        msg_text = read_txt_file("text/clan/clan_invitations")
        clan_invitation_msg = await clan_msg.edit_text(
            text=msg_text,
            reply_markup=keyboard
        )
        await state.update_data({
            "clan_invitation_msg": clan_invitation_msg
        })

    session.close()


@dp.callback_query_handler(regexp=ClanRegexp.menu)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    clan_msg: types.Message = data.get("clan_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).join(tables.Clan).first()

    clan_members: typing.List[tables.ClanMember] = session.db.query(
        tables.ClanMember).filter_by(clan_id=clan_member.clan_id).all()

    clans_search: typing.List[tables.Clan] = session.db.query(
        tables.Clan).filter(and_(
        tables.Clan.state == "search", tables.Clan.clan_id != clan_member.clan_id)).all()

    if callback.data == "clan_war":
        if clan_member.clan.state == "search":

            if clans_search:
                clan_1: tables.Clan = clan_member.clan
                clan_2: tables.Clan = random.choice(clans_search)

                clan_1.state = "contest"
                clan_2.state = "contest"

                new_contest = tables.Contest(
                    clan_id_1=clan_1.clan_id,
                    clan_id_2=clan_2.clan_id,
                    recent_log=["Война началась."],
                    log=["Война началась."],
                    state_timer=None,
                    territory_names=["Russia", "Germany"],
                    territory_owners=[None, None],
                    territory_units=[0, 0],
                    territory_captures=[None, None],
                    clans_rating=[0, 0],
                    colors=["blue", "red"]
                )
                session.db.add(new_contest)
                msg_text = read_txt_file("text/clan/contest")
                await clan_msg.edit_text(
                    text=msg_text.format(clan_member.clan.contest_count),
                    reply_markup=keyboards.clan.kb_back
                )
                session.close()
                return

            msg_text = read_txt_file("text/clan/search_contest")
            await clan_msg.edit_text(
                text=msg_text.format(clan_member.clan.contest_count),
                reply_markup=keyboards.clan.kb_cancel_contest
            )
        elif clan_member.clan.state == "contest":
            msg_text = read_txt_file("text/clan/contest")
            await clan_msg.edit_text(
                text=msg_text.format(clan_member.clan.contest_count),
                reply_markup=keyboards.clan.kb_back
            )
        elif clan_member.clan.state == "ending":
            msg_text = read_txt_file("text/clan/ending_contest")
            await clan_msg.edit_text(
                text=msg_text.format(clan_member.clan.contest_count),
                reply_markup=keyboards.clan.kb_back
            )
        else:
            msg_text = read_txt_file("text/clan/none_contest")
            await clan_msg.edit_text(
                text=msg_text.format(clan_member.clan.contest_count),
                reply_markup=keyboards.clan.kb_search_contest
            )

    elif callback.data == "clan_members":
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_members_keyboard()

        msg_text = read_txt_file("text/clan/members")

        clan_members_msg = await clan_msg.edit_text(
            text=msg_text.format(
                clan_member.clan.name,
                clan_member.clan.description[:21],
                len(clan_members),
            ),
            reply_markup=keyboard
        )

        await state.update_data({
            "clan_members_msg": clan_members_msg
        })

    elif callback.data == "clan_settings":
        await callback.answer("В разработке...")

    await callback.answer()
    session.close()


@dp.callback_query_handler(state="*", regexp=ClanRegexp.invitation_page)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    clan_msg: types.Message = data.get("clan_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    keyboard = kb_constructor.PaginationKeyboard(
        user_id=user_id
    )

    page_move = re.findall(r"invitation_page_(\d+)", callback.data)[0]
    page = int(page_move)

    keyboard = keyboard.create_invitation_keyboard(page)
    try:
        msg_text = read_txt_file("text/clan/clan_invitations")
        await clan_msg.edit_text(
            text=msg_text,
            reply_markup=keyboard
        )
    except exceptions.MessageNotModified:
        pass


@dp.callback_query_handler(state="*", regexp=ClanRegexp.invitation)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    clan_msg: types.Message = data.get("clan_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    invitation = re.findall(r"open_invitation_(\d+)", callback.data)
    accept_invitation = re.findall(r"accept_invitation_(\d+)", callback.data)
    cancel_invitation = re.findall(r"cancel_invitation_(\d+)", callback.data)

    session = db_api.CreateSession()

    if invitation:
        invitation_id = int(invitation[0])
        clan_invitation_table: tables.ClanInvitation = session.db.query(
            tables.ClanInvitation).filter_by(id=invitation_id).join(tables.Clan).first()

        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_invitation_keyboard(invitation_id=invitation_id)

        await clan_msg.edit_text(
            text="{}\n\n"
                 "Рейтинг: \n"
                 "Лидер: \n"
                 "Участников: \n"
                 "Осталось: ".format(clan_invitation_table.clan.name),
            reply_markup=keyboard
        )
    elif accept_invitation:
        invitation_id = int(accept_invitation[0])
        clan_invitation_table: tables.ClanInvitation = session.db.query(
            tables.ClanInvitation).filter_by(id=invitation_id).join(tables.Clan).first()

        if clan_invitation_table.clan.creator == user_id:
            rank = "Лидер"
        else:
            rank = "Рекрут"

        new_clan_member = tables.ClanMember(
            clan_id=clan_invitation_table.clan_id,
            user_id=user_id,
            rank=rank,
            money_donate=0,
            units_donate=0
        )
        session.db.add(new_clan_member)

        session.db.query(tables.ClanInvitation).filter_by(
            id=invitation_id).delete()

        session.db.commit()
        await callback.answer("Вы вступили в клан!")

        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_invitation_keyboard()

        msg_text = read_txt_file("text/clan/clan_invitations")
        await clan_msg.edit_text(
            text=msg_text,
            reply_markup=keyboard
        )

    elif cancel_invitation:
        invitation_id = int(cancel_invitation[0])
        session.db.query(tables.ClanInvitation).filter_by(
            id=invitation_id).delete()

        session.db.commit()

        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_invitation_keyboard()

        msg_text = read_txt_file("text/clan/clan_invitations")
        await clan_msg.edit_text(
            text=msg_text,
            reply_markup=keyboard
        )

    session.close()


@dp.callback_query_handler(regexp=ClanRegexp.get_clan_units)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    clan_msg: types.Message = data.get("clan_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    keyboard = kb_constructor.PaginationKeyboard(
        user_id=user_id
    )

    session = db_api.CreateSession()

    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()

    if callback.data == "get_clan_units":
        msg_text = read_txt_file("text/clan/get_clan_units")
        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_get_clan_units_keyboard()

        sticker = read_txt_file("sticker/get_clan_units")
        await callback.message.answer_sticker(sticker=sticker)
        await callback.message.answer(
            text=msg_text.format(townhall.country_name, callback.from_user.get_mention()),
            reply_markup=keyboard
        )

    session.close()


@dp.callback_query_handler(regexp=ClanRegexp.member)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    clan_msg: types.Message = data.get("clan_msg")
    clan_members_msg: types.Message = data.get("clan_members_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).first()

    clan_member_id = re.findall(r"check_clan_member_(\d+)", callback.data)
    raise_member = re.findall(r"raise_clan_member_(\d+)", callback.data)
    kick_member = re.findall(r"kick_clan_member_(\d+)", callback.data)

    if clan_member_id:
        member_id = int(clan_member_id[0])

        checked_clan_member: tables.ClanMember = session.db.query(
            tables.ClanMember).filter_by(id=member_id).join(tables.User).first()

        keyboard = kb_constructor.StandardKeyboard(
            user_id=user_id).create_member_keyboard(member_id, clan_member)

        msg_text = read_txt_file("text/clan/member")
        await clan_msg.edit_text(
            text=msg_text.format(
                checked_clan_member.user.first_name,
                checked_clan_member.rank,
                checked_clan_member.money_donate,
                checked_clan_member.units_donate
            ),
            reply_markup=keyboard
        )
    elif raise_member:
        member_id = int(raise_member[0])
        checked_clan_member: tables.ClanMember = session.db.query(
            tables.ClanMember).filter_by(id=member_id).first()

        if checked_clan_member.rank == "Рекрут":
            checked_clan_member.rank = "Старейшина"
        elif checked_clan_member.rank == "Старейшина":
            checked_clan_member.rank = "Заместитель"

        session.db.commit()

        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_members_keyboard()
        await clan_msg.edit_text(
            text=clan_members_msg.html_text,
            reply_markup=keyboard
        )

    elif kick_member:
        member_id = int(kick_member[0])

        session.db.query(
            tables.ClanMember).filter_by(id=member_id).delete()
        session.db.commit()

        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_members_keyboard()

        await clan_msg.edit_text(
            text=clan_members_msg.html_text,
            reply_markup=keyboard
        )
    elif callback.data == "leave_clan":
        await clan_msg.edit_text(
            text="Вы уверены,\n что хотите покинуть клан?",
            reply_markup=keyboards.clan.kb_leave_clan
        )
    elif callback.data == "yes_leave_clan":
        session.db.query(
            tables.ClanMember).filter_by(user_id=user_id).delete()
        session.db.commit()

        await clan_msg.edit_text(
            text="Клан",
            reply_markup=keyboards.clan.kb_none_clan
        )
    elif callback.data == "no_leave_clan":
        await clan_msg.edit_text(
            text=clan_msg.html_text,
            reply_markup=clan_msg.reply_markup
        )

    await callback.answer()
    session.close()


@dp.callback_query_handler(regexp=ClanRegexp.contest)
async def townhall_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    clan_msg: types.Message = data.get("clan_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    clan_member: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).join(tables.Clan).first()

    if callback.data == "start_search_contest":
        msg_text = read_txt_file("text/clan/search_contest")
        await clan_msg.edit_text(
            text=msg_text,
            reply_markup=keyboards.clan.kb_cancel_contest
        )
        clan_member.clan.state = "search"

    elif callback.data == "cancel_search_contest":
        msg_text = read_txt_file("text/clan/none_contest")
        await clan_msg.edit_text(
            text=msg_text,
            reply_markup=keyboards.clan.kb_search_contest
        )
        clan_member.clan.state = None

    session.close()


@dp.message_handler(filters.IsReplyFilter(True), state=states.Clan.set_name)
async def set_clan_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    if message.reply_to_message.message_id == data.get("message_id"):
        session = db_api.CreateSession()
        clan_name = message.text    # need check regx

        new_clan = tables.Clan(
            name=clan_name,
            rating=0,
            description="Описание.",
            money=0,
            units=0,
            creator=user_id
        )
        session.db.add(new_clan)
        session.db.commit()

        created_clan: tables.Clan = session.db.query(
            tables.Clan).filter_by(creator=user_id).first()

        if created_clan is not None:
            new_clan_member = tables.ClanMember(
                clan_id=created_clan.clan_id,
                user_id=user_id,
                clan_units=0,
                rank="Лидер"
            )
            session.db.add(new_clan_member)

        await message.reply(
            "Вы успешно создали клан: {}".format(clan_name)
        )
        await state.reset_state(with_data=False)
        session.close()


@dp.message_handler(filters.IsReplyFilter(True), regexp=ClanRegexp.invite, state="*")
async def invite_user_clan_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    replied_user = message.reply_to_message.from_user

    session = db_api.CreateSession()
    clan_member_table: tables.ClanMember = session.filter_by_user_id(
        user_id=user_id, table=tables.ClanMember
    )
    if clan_member_table is None:
        return

    if clan_member_table.rank in ("Лидер", "Заместитель", "Старейшина"):

        invited_clan_member_table: tables.ClanMember = session.filter_by_user_id(
            user_id=replied_user.id, table=tables.ClanMember
        )
        invited_user_table: tables.User = session.filter_by_user_id(
            user_id=replied_user.id, table=tables.User)

        invited_clan_invitation_table: tables.ClanInvitation = session.db.query(
            tables.ClanInvitation).filter_by(
            clan_id=clan_member_table.clan_id, user_id=replied_user.id).first()

        if invited_user_table is None or invited_clan_invitation_table is not None:
            return

        if (invited_clan_member_table is None) and (not replied_user.is_bot):

            time_set = timer.Timer.set_timer(86400)
            new_invitation = tables.ClanInvitation(
                user_id=replied_user.id,
                clan_id=clan_member_table.clan_id,
                timer=time_set
            )
            session.db.add(new_invitation)

    session.close()


@dp.message_handler(regexp=ClanRegexp.donate, state="*")
async def clan_donate_handler(message: types.Message, state: FSMContext):

    user_id = message.from_user.id

    session = db_api.CreateSession()
    clan_member_table: tables.ClanMember = session.db.query(
        tables.ClanMember).filter_by(user_id=user_id).join(tables.Clan).first()

    if clan_member_table is None:
        return

    townhall_table: tables.TownHall = session.filter_by_user_id(
        user_id=user_id, table=tables.TownHall)

    units_table: tables.Units = session.filter_by_user_id(
        user_id=user_id, table=tables.Units)

    clan_donate = re.findall(r"клан\s+(казна|армия)\s+(\d+)", message.text)[0]
    donate_count = int(clan_donate[1])

    if clan_donate[0] == "казна" and townhall_table.money >= donate_count:
        townhall_table.money -= donate_count
        clan_member_table.money_donate += donate_count
        clan_member_table.clan.money += donate_count
        await message.reply("{} пожертвовал в клан {} 💰.".format(
            message.from_user.mention, donate_count))

    elif clan_donate[0] == "армия" and units_table.all_unit_counts >= donate_count:
        units_table.all_unit_counts -= donate_count
        unit_counts: list = subtract_nums_list(
            donate_count, list(units_table.unit_counts))
        units_table.unit_counts = unit_counts
        clan_member_table.units_donate += donate_count
        clan_member_table.clan.units += donate_count
        await message.reply("{} выслал поддержку клану {} 💂.".format(
            message.from_user.mention, donate_count))

    session.close()
