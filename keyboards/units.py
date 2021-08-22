from aiogram import types

kb_test = types.InlineKeyboardMarkup()

btn_create_1_unit = types.InlineKeyboardButton(
    text="🔨", callback_data="create_1_unit"
)

btn_1 = types.InlineKeyboardButton(
    text="32 🏹", callback_data="create_1_unit"
)

btn_2 = types.InlineKeyboardButton(
    text="🔒", callback_data="create_1_unit"
)

btn_3 = types.InlineKeyboardButton(
    text="🔒", callback_data="create_1_unit"
)
btn_4 = types.InlineKeyboardButton(
    text="🔒", callback_data="create_1_unit"
)

btn_6 = types.InlineKeyboardButton(
    text="⏱", callback_data="create_1_unit"
)

btn_7 = types.InlineKeyboardButton(
    text="+", callback_data="create_1_unit"
)
btn_8 = types.InlineKeyboardButton(
    text="—", callback_data="create_1_unit"
)

btn_9 = types.InlineKeyboardButton(
    text="—", callback_data="create_1_unit"
)

btn_10 = types.InlineKeyboardButton(
    text="—", callback_data="create_1_unit"
)


kb_test.row(btn_create_1_unit, btn_1, btn_2, btn_3, btn_4)
kb_test.row(btn_6, btn_7, btn_8, btn_9, btn_10)

btn_back_menu_units = types.InlineKeyboardButton(
    text="назад", callback_data="back_menu_units"
)

kb_creating_units = types.InlineKeyboardMarkup()
btn_create_1_unit = types.InlineKeyboardButton(
    text="+1", callback_data="create_1_unit"
)

btn_create_10_unit = types.InlineKeyboardButton(
    text="+10", callback_data="create_10_unit"
)

btn_create_100_unit = types.InlineKeyboardButton(
    text="+100", callback_data="create_100_unit"
)

kb_creating_units.row(btn_create_1_unit, btn_create_10_unit, btn_create_100_unit)
kb_creating_units.add(btn_back_menu_units)

kb_about_unit = types.InlineKeyboardMarkup()

btn_upgrade_unit = types.InlineKeyboardButton(
    text="▲ Уровень", callback_data="upgrade_unit"
)

kb_about_unit.add(btn_upgrade_unit)
kb_about_unit.add(btn_back_menu_units)
