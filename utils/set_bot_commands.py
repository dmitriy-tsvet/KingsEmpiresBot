from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
<<<<<<< HEAD
            types.BotCommand("townhall", "🏕 ратуша"),
            types.BotCommand("finance", "🏦 бюджет"),
            types.BotCommand("citizens", "👨🏼‍🌾 население"),
            types.BotCommand("buildings", "🏠 здания"),
=======
            types.BotCommand("townhall", "townhall"),
            types.BotCommand("citizens", "citizens"),
            types.BotCommand("buildings", "buildings"),
>>>>>>> 161839955fcc74a00b051e02eda6b4cb554a5326
            types.BotCommand("territory", "⚔ территория"),
            types.BotCommand("units", "💂 войска"),
            types.BotCommand("market", "⚖ рынок"),
            types.BotCommand("help", "помощь"),
        ]
    )
