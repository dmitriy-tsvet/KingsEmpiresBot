from aiogram import types

kb_buildings = types.InlineKeyboardMarkup()

btn_home_buildings = types.InlineKeyboardButton(
    text="🏡 жилье", callback_data="home_buildings"
)
btn_food_buildings = types.InlineKeyboardButton(
    text="🍇 провизия", callback_data="food_buildings"
)
btn_stock_buildings = types.InlineKeyboardButton(
    text="🌲 сырье", callback_data="stock_buildings"
)
btn_energy_buildings = types.InlineKeyboardButton(
    text="⚡ энергия", callback_data="energy_buildings"
)
btn_graviton_buildings = types.InlineKeyboardButton(
    text="🧬 гравитон", callback_data="graviton_buildings"
)
#
# kb_buildings.add(btn_home_buildings)
# kb_buildings.add(btn_food_buildings)
# kb_buildings.add(btn_stock_buildings)
# kb_buildings.add(btn_energy_buildings)
# kb_buildings.add(btn_graviton_buildings)

btn_back_buildings = types.InlineKeyboardButton(
    text="назад", callback_data="back_buildings"
)

kb_about_building = types.InlineKeyboardMarkup()
btn_upgrade_building = types.InlineKeyboardButton(
    text="▲ Уровень", callback_data="upgrade_building"
)

btn_back_some_buildings = types.InlineKeyboardButton(
    text="назад", callback_data="back_some_buildings"
)

kb_about_building.add(btn_upgrade_building)
kb_about_building.add(btn_back_some_buildings)


