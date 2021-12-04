from aiogram import types

kb_none_clan = types.InlineKeyboardMarkup()

btn_invitations = types.InlineKeyboardButton(
    text="📋 Приглашения", callback_data="clan_invitation"
)
btn_rating = types.InlineKeyboardButton(
    text="⭐ Рейтинг", callback_data="clans_rating"
)
btn_create_clan = types.InlineKeyboardButton(
    text="📯 Создать", callback_data="create_clan"
)


kb_none_clan.add(btn_create_clan, btn_rating)
kb_none_clan.add(btn_invitations)


kb_leader_clan = types.InlineKeyboardMarkup()

btn_war = types.InlineKeyboardButton(
    text="⚔ Война", callback_data="clan_war"
)
btn_get_units = types.InlineKeyboardButton(
    text="🏹 Запросить Воинов", callback_data="clan_tavern"
)
btn_members = types.InlineKeyboardButton(
    text="🧙🏻‍♂ Участники", callback_data="clan_members"
)
btn_settings = types.InlineKeyboardButton(
    text="⚙ Настройки", callback_data="clan_settings"
)
kb_leader_clan.add(btn_war)
kb_leader_clan.row(btn_members, btn_settings)

kb_recruit_clan = types.InlineKeyboardMarkup()

kb_recruit_clan.add(btn_members)

kb_back = types.InlineKeyboardMarkup()

btn_back = types.InlineKeyboardButton(
    text="назад", callback_data="back_clan_msg"
)
kb_back.add(btn_back)


btn_back_invitation = types.InlineKeyboardButton(
    text="назад", callback_data="back_invitation"
)

btn_back_members = types.InlineKeyboardButton(
    text="назад", callback_data="back_clan_members"
)


kb_leave_clan = types.InlineKeyboardMarkup()

btn_yes_leave = types.InlineKeyboardButton(
    text="да", callback_data="yes_leave_clan"
)

btn_no_leave = types.InlineKeyboardButton(
    text="нет", callback_data="no_leave_clan"
)

kb_leave_clan.row(btn_yes_leave, btn_no_leave)

kb_search_contest = types.InlineKeyboardMarkup()
btn_search_contest = types.InlineKeyboardButton(
    text="🔎 Поиск", callback_data="start_search_contest"
)

kb_search_contest.add(btn_search_contest)
kb_search_contest.add(btn_back)

kb_cancel_contest = types.InlineKeyboardMarkup()
btn_cancel_search_contest = types.InlineKeyboardButton(
    text="Отмена", callback_data="cancel_search_contest"
)
kb_cancel_contest.add(btn_cancel_search_contest)
kb_cancel_contest.add(btn_back)
