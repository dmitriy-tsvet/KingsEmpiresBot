

class TownhallRegexp:
    menu = r"progress|storage|get_money|get_stock"
    progress = r"technology_(\d+)_(\d+)|upgrade_one|upgrade_all|unlock_tech|unlock_age|tree_page_(\d+)"
    storage = r"my_product_(\d+)"
    back = r"back_townhall"


class ClanRegexp:
    menu = r"clan_war|clan_tavern|clan_members|clan_settings"
    invitation = r"invitation_(\d+)"
    invitation_page = r"invitation_page_(\d+)"
    without_clan = r"clans_rating|create_clan|clan_invitation"
    get_clan_units = r"get_clan_units"
    back = r"back_clan"
    invite = r"Пригласить"
    member = r"clan_member|leave_clan|yes_leave_clan|no_leave_clan"
    donate = r"клан\s+(казна|армия)\s+(\d+)"
    contest = r"start_search_contest|cancel_search_contest"


class ContestRegexp:
    capture = r"select_capture_territory|territory_(\d+)"
    camp = r"select_camp|camp_(\d+)"
    back = r"back_contest"


class BuildingsRegexp:
    building = r"building_pos_(\d+)|build_info_(\d+)|start_build|building_page_(\d+)"
    clan_building = r"fix_clan_building|upgrade_clan_building"
    unlocked_buildings = r"unlocked_buildings_page_(\d+)"
    tree = r"tree_pos_(\d+)|cut_down"
    back = r"back_buildings"


class ManufactureRegexp:
    menu = r"building_manufacture_pos_(\d+)|create_product_(\d+)|manufacture_product_(\d+)"
    back = r"back_manufacture"


class CampaignRegexp:
    menu = r"campaign_capture|campaign_page_(\d+)"
    select_territory = r"campaign_territory_(\d+)"
    select_units = r"кампания \s+\d+"
    start_capture = r"campaign_start_capture"
    back = r"back_campaign"


class Market:
    menu = r"market_page_(\d+)|market_product_(\d+)|my_products"
    current_product = r"buy_product|delete_product"
    back = r"back_market"


class Units:
    back = r"back_units"
