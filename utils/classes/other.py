from enum import Enum


class ListNamesResources(str, Enum):
    food = "🍇 Провизия"
    stock = "🌲 Сырье"
    energy = "⚡ Энергия"
    graviton = "🧬 Гравитон"


class ListEmojiResources(str, Enum):
    food = "🍇"
    stock = "🌲"
    energy = "⚡"
    graviton = "🧬"
