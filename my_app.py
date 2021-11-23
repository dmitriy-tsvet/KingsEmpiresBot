from flask import Flask
from flask import request
from pydantic import BaseModel
from pydantic.class_validators import root_validator
import json
from PIL import Image
import asyncio

app = Flask(__name__)


class SquareTerritory(BaseModel):
    square_1: list = None            # | 1 2 |
    square_2: list = None            # | 3 4 |
    square_3: list = None
    square_4: list = None


class PaintMap:
    @staticmethod
    def paint(colors: SquareTerritory, img_name: str):
        square = Image.open(f"static/map/{img_name}_original.jpeg")
        square = square.convert("RGBA")

        c1 = colors.square_1
        color_square_1 = Image.new('RGBA', (100, 100), (c1[0], c1[1], c1[2], c1[3]))
        name_square_1 = Image.new('RGBA', (100, 100), (c1[0], c1[1], c1[2], c1[3]))

        c2 = colors.square_2
        color_square_2 = Image.new('RGBA', (100, 100), (c2[0], c2[1], c2[2], c1[3]))

        c3 = colors.square_3
        color_square_3 = Image.new('RGBA', (100, 100), (c3[0], c3[1], c3[2], c3[3]))

        c4 = colors.square_4
        color_square_4 = Image.new('RGBA', (100, 100), (c4[0], c4[1], c4[2], c4[3]))

        square.paste(color_square_1, (0, 0), color_square_1) # up left
        square.paste(color_square_2, (0, 100), color_square_2) # down left
        square.paste(color_square_3, (100, 0), color_square_3) # up right
        square.paste(color_square_4, (100, 100), color_square_4) # down right

        square.paste(color_square_1, (0, 0), color_square_1) # up left
        square.paste(color_square_2, (0, 100), color_square_2) # down left
        square.paste(color_square_3, (100, 0), color_square_3) # up right
        square.paste(color_square_4, (100, 100), color_square_4) # down right

        square = square.convert('RGB')
        square.save(f"static/map/{img_name}.jpeg")


class MainTerritory(BaseModel):
    square_1: SquareTerritory = None            # | 1  2  3  4  |
    square_2: SquareTerritory = None            # | 5  6  7  8  |


    @root_validator()
    def paint_validate(cls, values):
        for img_name, colors in values.items():
            if colors:
                PaintMap.paint(colors, img_name)
        return values


@app.route(f"/generate_map_color", methods=['POST'])
def generate_map_color():
    data = json.loads(request.data)
    territories = MainTerritory(**data)
    return "200"


# @app.route("/", methods=['GET'])
# def get_main():
#     return '<img src="static/map/square_1.jpeg">'

app.run()

