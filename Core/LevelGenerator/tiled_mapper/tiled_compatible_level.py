from typing import AnyStr, Dict, List

from pytiled_parser.objects import ObjectLayer

from Core.LevelGenerator.tiled_mapper.constants import all_open_floor_tiles


def generate_tiled_compatible_level(width, height):
    level = dict()
    level["Walls"] = [[0 for y in range(height)] for x in range(width)]
    level["Floor"] = [[0 for y in range(height)] for x in range(width)]
    level["Lighting"] = [[0 for y in range(height)] for x in range(width)]

    return level


def place_tile_into_level_layer(level, tile_id, x, y):
    """
    Given a tile ID, associates it with a given layer in the level
    :param level: Level to add the tile to
    :param tile_id: Tile ID to assign to coordinates
    :param x: X coordinate of the new tile
    :param y: Y coordinate of the new tile
    :return: Nothing, it mutates the input (like a savage)
    """
    if tile_id in all_open_floor_tiles:
        level["Floor"][x][y] = tile_id
        return

    level["Walls"][x][y] = tile_id


def merge_level_layer_with_offset(
    parent: Dict[AnyStr, List[List[int]]],
    child: Dict[AnyStr, List[List[int]]],
    offset_x: int,
    offset_y: int,
    layer: AnyStr,
):

    child_width = len(child[layer])
    child_height = len(child[layer][0])

    # Copy in the generated room into the correct offset of the map
    for x in range(0, child_width):
        for y in range(0, child_height):
            # TODO: Why do we have to reverse the X and Y coordinates here? Did we fuck up somewhere else?
            parent[layer][offset_y + y][offset_x + x] = child[layer][x][y]


def merge_levels_with_offset(
    parent: Dict[AnyStr, List[List[int]]],
    child: Dict[AnyStr, List[List[int]]],
    offset_x: int,
    offset_y: int,
):
    """
    Combines together two levels, adjusting for an offset.
    The child is placed at the given offset inside of the parent.
    :param parent: Larger map
    :param child: Smaller map (or of equal size)
    :param offset_x: X Offset in the parent for the smaller map to be merged. Set to zero if you dont want an offset
    :param offset_y: Y Offset in the parent for the smaller map to be merged. Set to zero if you dont want an offset
    :return: Mutates inputs
    """
    for layer in child.keys():
        if parent[layer] is None:
            raise Exception("Unable to merge maps because of missing layer")

        merge_level_layer_with_offset(parent, child, offset_x, offset_y, layer)


if __name__ == "__main__":
    level = generate_tiled_compatible_level(2, 3)
    print(level)
