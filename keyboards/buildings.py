from aiogram import types

kb_build_info = types.InlineKeyboardMarkup()

btn_back_buildings = types.InlineKeyboardButton(
    text="назад", callback_data="back_buildings"
)

btn_build = types.InlineKeyboardButton(
    text="🔨 построить", callback_data="start_build"
)

btn_question = types.InlineKeyboardButton(
    text="?", callback_data="start_build"
)

kb_build_info.add(btn_build)
kb_build_info.add(btn_back_buildings)

kb_back = types.InlineKeyboardMarkup()
kb_back.add(btn_back_buildings)

kb_tree = types.InlineKeyboardMarkup()

btn_cut_down = types.InlineKeyboardButton(
    text="🪓 срубить", callback_data="cut_down"
)
kb_tree.add(btn_cut_down)
kb_tree.add(btn_back_buildings)


kb_fix_clan_building = types.InlineKeyboardMarkup()
btn_fix_clan_building = types.InlineKeyboardButton(
    text="🔨🏚 Починить (5000 💰)", callback_data="fix_clan_building"
)

kb_fix_clan_building.add(btn_fix_clan_building)
kb_fix_clan_building.add(btn_back_buildings)

kb_upgrade_clan_building = types.InlineKeyboardMarkup()
btn_upgrade_clan_building = types.InlineKeyboardButton(
    text="🔨✨ Улучшить ()", callback_data="upgrade_clan_building"
)

kb_upgrade_clan_building.add(btn_upgrade_clan_building)
kb_upgrade_clan_building.add(btn_back_buildings)
