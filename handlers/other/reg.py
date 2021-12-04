import re
import states

from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsReplyFilter

from utils.misc.read_file import read_txt_file
from utils.classes import table_setter, kb_constructor
from utils.models import ages, base
from utils.db_api import db_api, tables


@dp.message_handler(IsReplyFilter(True), state=states.Reg.input_name_country)
@dp.throttled(rate=1)
async def registration_handler(message: types.Message, middleware_data, state: FSMContext):
    user_id = message.from_user.id
    user_mention = message.from_user.get_mention()

    if message.reply_to_message.message_id == middleware_data:
        result1 = re.findall(r"[a-zA-Z_а-яА-Я]+", message.text)
        result2 = re.findall(r"[a-zA-Z_а-яА-Я0-9]+", message.text)[:1]

        if not result1:
            return await message.reply(
                "Попробуй ещё раз.\n\n"
                "<i>Примеры: </i><code>NameCountry,\n"
                "Name_Country, МояСтрана</code>"
            )

        else:
            country_name = result2[0]

            session = db_api.CreateSession()

            new_table = table_setter.TableSetter(user_id=user_id)
            new_table.set_stone_age(message, country_name)

            townhall: tables.TownHall = session.db.query(
                tables.TownHall).filter_by(user_id=user_id).first()
            buildings: tables.Buildings = session.db.query(
                tables.Buildings).filter_by(user_id=user_id).first()
            clan_member: tables.ClanMember = session.db.query(
                tables.ClanMember).filter_by(user_id=user_id).join(tables.Clan).first()

            age_model: base.Age = ages.Age.get(townhall.age)

            await state.reset_state(with_data=False)

            if clan_member is None:
                msg_text = read_txt_file("text/townhall/townhall_none_clan")
                user_clan = ""
            else:
                msg_text = read_txt_file("text/townhall/townhall_in_clan")
                user_clan = "{}".format(
                    clan_member.clan.name,
                )

            base_buildings = ages.Age.get_all_buildings()
            all_population = 0
            for building_num in buildings.buildings:
                if type(building_num) is int:
                    building = base_buildings[building_num]
                    if type(building) is base.HomeBuilding:
                        all_population += building.capacity

            with open(age_model.townhall_img, 'rb') as sticker:
                await message.answer_sticker(sticker=sticker)

            keyboard = kb_constructor.StandardKeyboard(
                user_id=user_id).create_townhall_keyboard()
            townhall_msg = await message.answer(
                text=msg_text.format(
                    townhall.country_name,
                    townhall.age,
                    townhall.population,
                    all_population,
                    user_clan,
                    user_mention),
                reply_markup=keyboard
            )
            await state.set_data({
                "user_id": user_id,
                "townhall_msg": townhall_msg,
            })
            session.close()
