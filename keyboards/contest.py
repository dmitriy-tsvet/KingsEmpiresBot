from aiogram import types

kb_contest = types.InlineKeyboardMarkup()

btn_capture = types.InlineKeyboardButton(
    text="⚔ Захват", callback_data="select_capture_territory"
)

btn_doings = types.InlineKeyboardButton(
    text="⏰ События", callback_data="doings"
)

btn_camp = types.InlineKeyboardButton(
    text="🏕 Лагерь", callback_data="select_camp"
)

kb_contest.row(btn_camp, btn_doings)
kb_contest.add(btn_capture)

btn_back = types.InlineKeyboardButton(
    text="назад", callback_data="back_contest"
)

kb_back = types.InlineKeyboardMarkup()
kb_back.add(btn_back)

kb_capture = types.InlineKeyboardMarkup()

btn_explore = types.InlineKeyboardButton(
    text="🗺 Разведка (25 💰)", callback_data="back_contest"
)

btn_start_capture = types.InlineKeyboardButton(
    text="⚔ Захватить", callback_data="start_capture"
)
kb_capture.add(btn_start_capture)
kb_capture.add(btn_explore)
kb_capture.add(btn_back)
