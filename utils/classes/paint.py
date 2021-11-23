from PIL import Image, ImageFont, ImageDraw
import time, random
from utils.misc import read_file
from utils.db_api import tables
from utils.models import models, ages


class PaintMap:
    @staticmethod
    def paint_contest(contest: tables.Contest):
        with Image.open("data/img/contest/location.jpg") as photo:
            background = photo.copy()

        clan_id_1 = contest.clan_id_1
        clan_id_2 = contest.clan_id_2
        indexes = [i for i, x in enumerate(contest.territory_owners)]

        for index in indexes:
            if contest.territory_owners[index] == clan_id_1:
                with Image.open('data/img/contest/{}_{}.png'.format(
                    contest.colors[clan_id_1], index+1
                )) as captured_territory:
                    background.paste(captured_territory, (0, 0), captured_territory)

            if contest.territory_owners[index] == clan_id_2:
                with Image.open('data/img/contest/{}_{}.png'.format(
                    contest.colors[clan_id_2], index+1
                )) as captured_territory:
                    background.paste(captured_territory, (0, 0), captured_territory)

        background.save('data/img/contest/map.jpg', quality=95)

    @staticmethod
    def paint_campaign(campaign: tables.Campaign, townhall: tables.TownHall):

        with Image.open("data/img/campaign/base_map.jpg") as photo:
            background = photo.copy()

        territories = [i for i in enumerate(campaign.territory_owned)]
        for territory in territories:
            territory_owned = territory[1]
            index = territory[0]

            base_age: models.Age = ages.Age.get(townhall.age)
            with Image.open(base_age.townhall_img) as photo:
                townhall_img = photo.copy()
                size = 400, 325
                townhall_img.thumbnail(size, Image.ANTIALIAS)

            background.paste(townhall_img, (845, 520), townhall_img)

            if territory_owned is True:
                with Image.open("data/img/campaign/{}.png".format(index + 1)) as captured_territory:
                    background.paste(captured_territory, (0, 0), captured_territory)

        background.save('data/img/campaign/map.jpg', quality=95)



