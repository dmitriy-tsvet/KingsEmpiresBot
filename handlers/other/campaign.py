import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import exceptions

import keyboards
from loader import dp
from utils.classes import kb_constructor, paint, capture, transaction
from utils.db_api import tables, db_api
from utils.misc.read_file import read_txt_file
from utils.classes.regexps import CampaignRegexp
from utils.classes import timer
from utils.models import ages


@dp.message_handler(state="*", commands="campaign")
async def campaign_command_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    session = db_api.CreateSession()

    campaign: tables.Campaign = session.db.query(
        tables.Campaign).filter_by(user_id=user_id).first()
    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()

    base_campaigns = ages.Age.get_all_campaigns()
    owned_territories = [i for i, x in enumerate(campaign.territory_owned) if x is True]

    campaign_str = ""
    numeration = 0

    for territory in enumerate(campaign.territory_owned):
        index = territory[0]
        value = territory[1]
        numeration += 1

        if not value:
            campaign_str += "{}. {}\n".format(
                numeration, base_campaigns[index].name
            )
            continue

        campaign_str += "{}. {} - ⭐\n".format(
            numeration, base_campaigns[index].name
        )

    paint.PaintMap.paint_campaign(campaign=campaign, townhall=townhall)

    with open("data/img/campaign/map.jpg", 'rb') as photo:
        await message.answer_photo(
            photo=photo,
        )

    msg_text = read_txt_file("text/campaign/campaign")
    campaign_msg = await message.answer(
        text=msg_text.format(
            len(owned_territories), len(base_campaigns),
            campaign_str
        ),
        reply_markup=keyboards.campaigns.kb_campaign,
        disable_web_page_preview=True
    )

    await state.update_data({
        "user_id": user_id,
        "campaign_msg": campaign_msg
    })

    session.close()


@dp.callback_query_handler(regexp=CampaignRegexp.back)
async def campaign_back_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    campaign_msg: types.Message = data.get("campaign_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    await campaign_msg.edit_text(
        text=campaign_msg.html_text,
        reply_markup=keyboards.campaigns.kb_campaign,
        disable_web_page_preview=True

    )
    await callback.answer()


@dp.callback_query_handler(state="*", regexp=CampaignRegexp.menu)
async def campaign_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    campaign_msg: types.Message = data.get("campaign_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    campaign: tables.Campaign = session.db.query(
        tables.Campaign).filter_by(user_id=user_id).first()

    buildings: tables.Buildings = session.db.query(
        tables.Buildings).filter_by(user_id=user_id).first()

    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()

    base_campaigns = ages.Age.get_all_campaigns()
    page_move = re.findall(r"campaign_page_(\d+)", callback.data)

    if page_move:
        page = int(page_move[0])
        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_campaign_keyboard(page)

        try:
            await campaign_msg.edit_reply_markup(
                reply_markup=keyboard
            )
        except exceptions.MessageNotModified:
            pass

    elif callback.data == "campaign_capture":
        if campaign.territory_captures:
            time_left = timer.Timer.get_left_time(campaign.territory_captures["timer"])

            if time_left[0] == 0:
                if campaign.territory_captures["win"] is True:
                    index = campaign.territory_captures["territory_index"]
                    territory_owners = list(campaign.territory_owned)
                    territory_owners[index] = True
                    campaign.territory_owned = territory_owners
                    base_campaign = base_campaigns[index]

                    curnt_buildings = list(buildings.buildings)
                    curnt_buildings += ["tree" for i in range(0, base_campaign.territory_size)]
                    buildings.buildings = curnt_buildings

                    townhall.money += base_campaign.income[0]
                    townhall.stock += base_campaign.income[1]

                    msg_text = read_txt_file("text/campaign/capture_win")
                    await campaign_msg.edit_text(
                        text=msg_text.format(
                            base_campaign.territory_size,
                            transaction.Purchase.get_price(base_campaign.income)),
                        reply_markup=keyboards.campaigns.kb_back_campaign
                    )

                elif campaign.territory_captures["win"] is False:
                    msg_text = read_txt_file("text/campaign/capture_lose")
                    await campaign_msg.edit_text(
                        text=msg_text,
                        reply_markup=keyboards.campaigns.kb_back_campaign
                    )
                campaign.territory_captures = {}
            else:
                msg_text = read_txt_file("text/campaign/capture_info")
                await campaign_msg.edit_text(
                    text=msg_text.format(*time_left),
                    reply_markup=keyboards.campaigns.kb_back_campaign
                )
            session.close()
            return

        keyboard = kb_constructor.PaginationKeyboard(
            user_id=user_id).create_campaign_keyboard()

        msg_text = read_txt_file("text/campaign/select_territory")
        await campaign_msg.edit_text(
            text=msg_text,
            reply_markup=keyboard,
        )

        await callback.answer()
        session.close()


@dp.callback_query_handler(state="*", regexp=CampaignRegexp.select_territory)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    campaign_msg: types.Message = data.get("campaign_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

    select_territory = re.findall(r"campaign_territory_(\d+)", callback.data)
    if select_territory:
        territory_index = int(select_territory[0])

        await state.update_data({
            "campaign_territory_index": territory_index
        })

        base_units = ages.Age.get_all_units()
        current_base_units = [base_units[i] for i in units.units_type if i is not None]

        units_count = [i for i in units.units_count if i != 0]

        if not units_count:
            await callback.answer("У вас нету армии.")
            session.close()
            return

        units_count = [i for i in units.units_count]
        player_unit_str = ""
        for unit_count in enumerate(units_count):
            index = unit_count[0]
            value = unit_count[1]

            if value == 0:
                continue

            unit_emoji = re.findall(r"\W+", current_base_units[index].name)[0]

            if index == len(units_count)-1:
                player_unit_str += "x{}{}".format(value, unit_emoji)
                break

            player_unit_str += "x{}{}, ".format(value, unit_emoji)

        base_campaigns = ages.Age.get_all_campaigns()
        base_campaign = base_campaigns[territory_index]

        campaign_units_count = [i for i in base_campaign.units_count if i != 0]
        campaign_units_str = ""

        for unit_count in enumerate(campaign_units_count):
            index = unit_count[0]
            value = unit_count[1]

            unit_emoji = re.findall(r"\W+", base_campaign.units_type[index].name)[0]

            if index == len(campaign_units_count) - 1:
                campaign_units_str += "x{}{}".format(value, unit_emoji)
                break

            campaign_units_str += "x{}{}, ".format(value, unit_emoji)

        msg_text = read_txt_file("text/campaign/start_capture")
        await campaign_msg.edit_text(
            text=msg_text.format(
                base_campaign.name,
                player_unit_str,
                campaign_units_str,
                base_campaign.territory_size,
                transaction.Purchase.get_price(base_campaign.income)
            ),
            reply_markup=keyboards.campaigns.kb_start_capture
        )

    session.close()


@dp.callback_query_handler(state="*", regexp=CampaignRegexp.start_capture)
async def campaign_capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    campaign_msg: types.Message = data.get("campaign_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    campaign: tables.Campaign = session.db.query(
        tables.Campaign).filter_by(user_id=user_id).first()
    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

    campaign_territory_index = data.get("campaign_territory_index")
    base_campaigns = ages.Age.get_all_campaigns()
    curnt_campaign = base_campaigns[campaign_territory_index]

    if callback.data == "campaign_start_capture":

        win_status: bool = capture.Capture(
            units.real_units_count,
            curnt_campaign.real_units_count
        ).is_win()

        new_capture = {
            "territory_index": data.get("campaign_territory_index"),
            "timer": timer.Timer.set_timer(curnt_campaign.time_capture_sec),
            "win": win_status
        }
        if not campaign.territory_captures:
            campaign.territory_captures = new_capture
            units.real_units_count = 0
            reset_units_count = [0 for i in units.units_count]
            units.units_count = reset_units_count

        msg_text = read_txt_file("text/campaign/capture_info")
        await campaign_msg.edit_text(
            text=msg_text.format(
                *timer.Timer.get_left_time(new_capture["timer"])
            ),
            reply_markup=keyboards.campaigns.kb_back_campaign
        )

    session.close()

