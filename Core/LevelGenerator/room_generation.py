# Used for the areas that the player is able to navigate
import random
from typing import Optional, List

from Core.LevelGenerator.tiled_mapper.constants import *
from Core.LevelGenerator.tiled_mapper.tiled_compatible_level import (
    generate_tiled_compatible_level,
)


def get_tile_from_list(tile_list):
    # All of the values are off by one because the Tiled editor UI is annoying... Just hack it here. #yolo
    return random.choice(tile_list) + 1


def generate_room(width, height):
    # TODO: Need offset?
    level = generate_tiled_compatible_level(width, height)
    walls = level["Walls"]
    floors = level["Floor"]
    lights = level["Lighting"]

    # Set corners
    walls[0][0] = get_tile_from_list(top_left_outer_wall_tile_ids)
    walls[width - 1][0] = get_tile_from_list(top_right_outer_wall_tile_ids)
    walls[0][height - 1] = get_tile_from_list(bottom_left_outer_wall_tile_ids)
    walls[width - 1][height - 1] = get_tile_from_list(bottom_right_outer_wall_tile_ids)

    # Set top and bottom walls
    for i in range(1, width - 1):
        walls[i][0] = get_tile_from_list(top_outer_wall_tile_ids)
        walls[i][height - 1] = get_tile_from_list(bottom_outer_wall_tile_ids)

    # Set left and right walls
    for i in range(1, height - 1):
        walls[0][i] = get_tile_from_list(left_outer_wall_tile_ids)
        walls[width - 1][i] = get_tile_from_list(right_outer_wall_tile_ids)

    # Set top and bottom inner floor
    for i in range(1, width - 2):
        floors[i][1] = get_tile_from_list(top_inner_floor_tile_ids)
        floors[i][height - 2] = get_tile_from_list(bottom_inner_floor_tile_ids)

    # Set left and right inner floor
    for i in range(1, height - 2):
        floors[1][i] = get_tile_from_list(left_inner_floor_tile_ids)
        floors[width - 2][i] = get_tile_from_list(right_inner_floor_tile_ids)

    # Set floor corners
    floors[1][1] = get_tile_from_list(top_left_inner_floor_tile_ids)
    floors[width - 2][1] = get_tile_from_list(top_right_inner_floor_tile_ids)
    floors[1][height - 2] = get_tile_from_list(bottom_left_inner_floor_tile_ids)
    floors[width - 2][height - 2] = get_tile_from_list(
        bottom_right_inner_floor_tile_ids
    )

    # Fill open floor tiles
    for y in range(2, height - 2):
        for x in range(2, width - 2):
            floors[x][y] = get_tile_from_list(open_floor_tile_ids)

    # throw a few lights around each room for fun
    lights[2][2] = get_tile_from_list(light_fixtures)
    lights[width - 3][2] = get_tile_from_list(light_fixtures)
    lights[2][height - 3] = get_tile_from_list(light_fixtures)
    lights[width - 3][height - 3] = get_tile_from_list(light_fixtures)

    return level


def generate_tunnel(width, height):

    # TODO: Need offset?
    level = generate_tiled_compatible_level(width, height)
    walls = level["Walls"]
    floors = level["Floor"]

    # vertical tunnel
    if height > width:
        # set corner pieces of tunnel
        walls[0][0] = get_tile_from_list(top_left_outer_vertical_tunnel_wall_ids)
        walls[width - 1][0] = get_tile_from_list(
            top_right_outer_vertical_tunnel_wall_ids
        )
        walls[0][height - 1] = get_tile_from_list(
            bottom_right_outer_vertical_tunnel_wall_ids
        )
        walls[width - 1][height - 1] = get_tile_from_list(
            bottom_left_outer_vertical_tunnel_wall_ids
        )

        # set left right side walls
        for y in range(1, height - 1):
            walls[0][y] = get_tile_from_list(left_outer_wall_tile_ids)
            walls[width - 1][y] = get_tile_from_list(right_outer_wall_tile_ids)

        # set open floor for the middle of the tunnel
        for x in range(1, width - 1):
            for y in range(0, height):
                floors[x][y] = get_tile_from_list(open_floor_tile_ids)

        return level

    # set corner pieces of tunnel
    walls[0][0] = get_tile_from_list(top_left_outer_horizontal_tunnel_wall_ids)
    walls[width - 1][0] = get_tile_from_list(top_right_outer_horizontal_tunnel_wall_ids)
    walls[0][height - 1] = get_tile_from_list(
        bottom_right_outer_horizontal_tunnel_wall_ids
    )
    walls[width - 1][height - 1] = get_tile_from_list(
        bottom_left_outer_horizontal_tunnel_wall_ids
    )

    # set top bottom side walls
    for x in range(1, width - 1):
        walls[x][0] = get_tile_from_list(top_outer_wall_tile_ids)
        walls[x][height - 1] = get_tile_from_list(bottom_outer_wall_tile_ids)

    # set open floor for the middle of the tunnel
    for x in range(0, width):
        for y in range(1, height - 1):
            floors[x][y] = get_tile_from_list(open_floor_tile_ids)

    return level
