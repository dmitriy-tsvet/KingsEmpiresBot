#
# import states
#
# async def check_user_registration(message, state):
#     user_id = message.from_user.id
#     player_data = get_townhall_table(user_id)
#
#     if player_data is None:
#         reply_msg = await message.reply(
#             text="🏳️ Для начала назови\n"
#                  "свою страну, ответив\n"
#                  "на это сообщение.\n\n"
#                  "<i>Формат:\n"
#                  "a-z, 0-9, нижний прочерк,\n"
#                  "без пробелов</i>",
#         )
#         await state.update_data({"reply_msg": reply_msg})
#         await states.Reg.first()
#         return True
#
#     return False

# async def check_user_registration(message, state):
#     user_id = message.from_user.id
#     player_data = await get_townhall_table(user_id)
#
#     if player_data is None:
#         reply_msg = await message.reply(
#             text="🏳️ Для начала назови\n"
#                  "свою страну, ответив\n"
#                  "на это сообщение.\n\n"
#                  "<i>Формат:\n"
#                  "a-z, 0-9, нижний прочерк,\n"
#                  "без пробелов</i>",
#         )
#         await state.update_data({"reply_msg": reply_msg})
#         await states.Reg.first()
#         return True
#
#     return False


