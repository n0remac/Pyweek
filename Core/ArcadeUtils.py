from typing import Tuple

from pytiled_parser.objects import TileMap

from Constants.Game import SPRITE_SCALING_TILES


def convert_from_tiled_coordinates(map: TileMap, location: Tuple[int, int]):
    x = location[0] * SPRITE_SCALING_TILES
    y = (map.map_size.height * map.tile_size[1] - location[1]) * SPRITE_SCALING_TILES

    return x, y
