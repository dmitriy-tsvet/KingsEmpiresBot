from aiogram import types

btn_back_campaign = types.InlineKeyboardButton(
    text="назад", callback_data="back_campaign"
)

btn_next = types.InlineKeyboardButton(
    text="дальше", callback_data="campaign_waiting_capture"
)

kb_campaign = types.InlineKeyboardMarkup()

btn_capture = types.InlineKeyboardButton(
    text="⚔ Захват", callback_data="campaign_capture"
)

kb_back_campaign = types.InlineKeyboardMarkup()
kb_back_campaign.add(btn_back_campaign)

kb_campaign.row(btn_capture)

kb_start_capture = types.InlineKeyboardMarkup()
btn_capture = types.InlineKeyboardButton(
    text="⚔ Начать Захват!", callback_data="campaign_start_capture"
)
kb_start_capture.add(btn_capture)
kb_start_capture.add(btn_back_campaign)
