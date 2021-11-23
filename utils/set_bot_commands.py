from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("townhall", "🏕 ратуша"),
            types.BotCommand("buildings", "🏠 постройки"),
            types.BotCommand("manufacture", "⚒ производство"),
            types.BotCommand("units", "🏹 юниты"),
            types.BotCommand("campaign", "⭐ кампания"),
            types.BotCommand("clan", "🔰 клан"),
            types.BotCommand("contest", "⚔ война"),
            types.BotCommand("market", "💰 рынок"),
            types.BotCommand("shop", "💎 магазин"),
            types.BotCommand("help", "помощь"),
        ]
    )
