from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("townhall", "⛺ ратуша"),
            types.BotCommand("buildings", "🏠 здания"),
            types.BotCommand("territory", "⚔ территория"),
            types.BotCommand("units", "💂 войска"),
            types.BotCommand("help", "помощь"),
        ]
    )
