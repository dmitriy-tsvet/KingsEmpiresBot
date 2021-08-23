from aiogram import types


btn_back_menu_units = types.InlineKeyboardButton(
    text="назад", callback_data="back_menu_units"
)


kb_about_unit = types.InlineKeyboardMarkup()

btn_upgrade_unit = types.InlineKeyboardButton(
    text="▲ Уровень", callback_data="upgrade_unit"
)

kb_about_unit.add(btn_upgrade_unit)
kb_about_unit.add(btn_back_menu_units)
