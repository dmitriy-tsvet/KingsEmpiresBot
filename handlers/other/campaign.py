import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram import exceptions
from sqlalchemy import or_

import random
import keyboards
import states
from loader import dp
from utils.classes import kb_constructor, paint, capture, transaction
from utils.db_api import tables, db_api
from utils.misc.read_file import read_txt_file
from utils.misc.regexps import CampaignRegexp
from utils.classes import timer
from utils.models import base, ages
from utils.misc.operation_with_lists import subtract_nums_list


@dp.message_handler(state="*", commands="campaign")
async def territory_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    session = db_api.CreateSession()

    campaign: tables.Campaign = session.db.query(
        tables.Campaign).filter_by(user_id=user_id).first()

    townhall: tables.TownHall = session.db.query(
        tables.TownHall).filter_by(user_id=user_id).first()

    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

    base_campaigns = ages.Age.get_all_campaigns()
    owned_territories = [i for i, x in enumerate(campaign.territory_owned) if x is True]
    base_units = ages.Age.get_all_units()

    units_str = ""
    for index in units.units_type:
        if index is None:
            continue

        base_unit = base_units[index]
        unit_emoji = re.findall(r"\W+", base_unit.name)[0]
        units_str += "- x{} {}\n".format(
            units.units_count[units.units_type.index(index)], unit_emoji
        )

    paint.PaintMap.paint_campaign(campaign=campaign, townhall=townhall)

    with open("data/img/campaign/map.jpg", 'rb') as photo:
        await message.answer_photo(
            photo=photo,
        )

    msg_text = read_txt_file("text/campaign/campaign")
    campaign_msg = await message.answer(
        text=msg_text.format(
            len(owned_territories), len(base_campaigns), sum(units.units_count),
            units_str
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
async def back_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    campaign_msg: types.Message = data.get("campaign_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()

    campaign: tables.Campaign = session.db.query(
        tables.Campaign).filter_by(user_id=user_id).first()

    base_campaigns = ages.Age.get_all_campaigns()

    msg_text = read_txt_file("text/campaign/campaign")

    await campaign_msg.edit_text(
        text=campaign_msg.html_text,
        reply_markup=keyboards.campaigns.kb_campaign,
        disable_web_page_preview=True

    )
    session.close()


@dp.callback_query_handler(state="*", regexp=CampaignRegexp.menu)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    campaign_msg: types.Message = data.get("campaign_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()
    territory_index = re.findall(r"territory_(\d+)", callback.data)

    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

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
                        text=msg_text
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


@dp.callback_query_handler(state="*", regexp=CampaignRegexp.select_territory)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    campaign_msg: types.Message = data.get("campaign_msg")

    if data.get("user_id") != user_id:
        msg_text = read_txt_file("text/hints/foreign_button")
        return await callback.answer(msg_text)

    session = db_api.CreateSession()
    base_campaigns = ages.Age.get_all_campaigns()

    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()

    select_territory = re.findall(r"campaign_territory_(\d+)", callback.data)
    if select_territory:
        territory_index = int(select_territory[0])

        # keyboard = kb_constructor.StandardKeyboard(
        #     user_id=user_id).create_select_units_keyboard()
        msg_text = read_txt_file("text/campaign/select_units")
        await campaign_msg.edit_text(
            text=msg_text.format(
                sum(units.units_count)
            ),
            reply_markup=keyboards.campaigns.kb_back_campaign
        )

        await state.update_data({
            "campaign_territory_index": territory_index
        })
        await states.Campaign.select_units.set()
    session.close()


@dp.message_handler(state=states.Campaign.select_units)
async def capture_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    campaign_msg: types.Message = data.get("campaign_msg")

    session = db_api.CreateSession()

    units: tables.Units = session.db.query(
        tables.Units).filter_by(user_id=user_id).first()
    base_campaigns = ages.Age.get_all_campaigns()
    base_campaign = base_campaigns[data.get("campaign_territory_index")]

    try:
        campaign_msg.message_id
    except AttributeError:
        return
    
    if campaign_msg.message_id == message.reply_to_message.message_id:
        select_units_count = re.findall(r"(\d+)\s*", message.text)[0]
        select_units_count = int(select_units_count)

        if select_units_count > sum(units.units_count):
            await message.reply(
                text="<code>у вас нету столько воинов</code>\n"
                     "<i>подробнее </i>")
            session.close()
            return
        elif select_units_count <= 0:
            await message.reply(
                text="<code>слишком мало юнитов</code>\n"
                     "<i>подробнее </i>")
            session.close()
            return

        units_count = list(units.units_count)
        # remaining_units_count = [
        #     units_count - select_units_count for units_count, select_units_count in zip(
        #         units_count, select_units_count
        #     )]

        base_units = ages.Age.get_all_units()
        new_base_units = [base_units[i] for i in units.units_type if i is not None]

        real_units_count = sum(
            [i[1].weight * select_units_count for i in enumerate(new_base_units)]
        )

        msg_text = read_txt_file("text/campaign/start_capture")

        await campaign_msg.edit_text(
            text=msg_text.format(
                base_campaign.name,
                select_units_count,
                sum(base_campaign.units_count),
                base_campaign.territory_size,
                transaction.Purchase.get_price(base_campaign.income)
            ),
            reply_markup=keyboards.campaigns.kb_start_capture
        )
        await state.update_data({
            "select_units_count": select_units_count,
            "real_units_count": real_units_count
        })
        await state.reset_state(with_data=False)

    session.close()


@dp.callback_query_handler(state="*", regexp=CampaignRegexp.start_capture)
async def capture_handler(callback: types.CallbackQuery, state: FSMContext):
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
            data.get("real_units_count"),
            curnt_campaign.real_units_count
        ).is_win()

        new_capture = {
            "territory_index": data.get("campaign_territory_index"),
            "timer": timer.Timer.set_timer(curnt_campaign.time_capture_sec),
            "win": win_status
        }
        if not campaign.territory_captures:
            campaign.territory_captures = new_capture
            units.real_units_count -= data.get("real_units_count")
            units_count = subtract_nums_list(data.get("select_units_count"), units.units_count)
            units.units_count = units_count

        msg_text = read_txt_file("text/campaign/capture_info")
        await campaign_msg.edit_text(
            text=msg_text.format(
                *timer.Timer.get_left_time(new_capture["timer"])
            )
        )

    session.close()

