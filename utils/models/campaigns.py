from utils.models import unit, product, base
from enum import Enum


class Campaigns(Enum):
    Luya = base.Campaign(
        name="🌊 Luya",
        income=[262, 0],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[25, 30],
        time_capture_sec=120,
        territory_size=5
    )

    Broleron = base.Campaign(
        name="🌾 Broleron",
        income=[162, 50],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[50, 50],
        time_capture_sec=300,
        territory_size=2
    )

    Greathia = base.Campaign(
        name="🌳 Greathia",
        income=[95, 125],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[74, 0],
        time_capture_sec=300,
        territory_size=3
    )

    Totha = base.Campaign(
        name="🌊 Totha",
        income=[300, 200],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[100, 40],
        time_capture_sec=300,
        territory_size=4
    )

    Peburg = base.Campaign(
        name="⛰ Peburg",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[200, 50],
        time_capture_sec=300,
        territory_size=4
    )

    Enulan = base.Campaign(
        name="🌳 Enulan",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[70, 230],
        time_capture_sec=300,
        territory_size=5
    )

    Reorin = base.Campaign(
        name="🌪 Reorin",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[300, 50],
        time_capture_sec=300,
        territory_size=5
    )

    Mevia = base.Campaign(
        name="🌳 Mevia",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[400, 50],
        time_capture_sec=300,
        territory_size=4
    )

    Drapia = base.Campaign(
        name="⛰ Drapia",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[400, 500],
        time_capture_sec=300,
        territory_size=6
    )

    Veoborg = base.Campaign(
        name="🌳 Veoborg",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[200, 200],
        time_capture_sec=300,
        territory_size=4
    )

    Slizia = base.Campaign(
        name="🌾 Slizia",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[400, 300],
        time_capture_sec=300,
        territory_size=7
    )

    Kawen = base.Campaign(
        name="🌳 Kawen",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[300, 400],
        time_capture_sec=300,
        territory_size=6
    )

    Hesea = base.Campaign(
        name="🌾 Hesea",
        income=[1000, 1000],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[400, 400],
        time_capture_sec=300,
        territory_size=3
    )

    WestRuins = base.Campaign(
        name="🏔 West Ruins",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[300, 200],
        time_capture_sec=300,
        territory_size=6
    )

    Dorpuweth = base.Campaign(
        name="🌳 Dorpuweth",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[500, 500],
        time_capture_sec=300,
        territory_size=8
    )

    Widelands = base.Campaign(
        name="❄ Widelands",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[500, 500],
        time_capture_sec=300,
        territory_size=8
    )

    Araburg = base.Campaign(
        name="🏔 Araburg",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[500, 500],
        time_capture_sec=300,
        territory_size=9
    )

    DeepingVale = base.Campaign(
        name="🌵 Deeping Vale",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[500, 500],
        time_capture_sec=300,
        territory_size=9
    )

    Rivenwood = base.Campaign(
        name="🍂 Rivenwood",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[500, 500],
        time_capture_sec=300,
        territory_size=10
    )

    ContinentCoast = base.Campaign(
        name="⛵ Continent Coast",
        income=[25, 25],
        units_type=[unit.StoneMilitia, unit.BronzeArcher],
        units_count=[500, 500],
        time_capture_sec=300,
        territory_size=9
)
