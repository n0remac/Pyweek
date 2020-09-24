from typing import List, Dict, AnyStr

from Core.LevelGenerator.bsp_tree import generate_bsp_level, ascii_print_level
from Core.LevelGenerator.room_generation import generate_room, generate_tunnel

from Core.LevelGenerator.shapes import Rect
from Core.LevelGenerator.tiled_mapper.tiled_compatible_level import (
    generate_tiled_compatible_level,
    merge_levels_with_offset,
)


def place_room(room: Rect, output_level: Dict[AnyStr, List[List[int]]]):
    # Note: This function is not referentially transparent and relies on side effects to mutate output_level
    room_width = (room.x2 - room.x1) * 3
    room_height = (room.y2 - room.y1) * 3

    # All rooms are 3x the size in the game versus the generator to allow hallways to have all tile types
    room_tiles = generate_room(room_width, room_height)

    merge_levels_with_offset(output_level, room_tiles, room.x1 * 3, room.y1 * 3)

    return output_level


def place_tunnel(tunnel, output_level):
    # Note: This function is not referentially transparent and relies on side effects to mutate output_level
    tunnel_width = (tunnel.x2 - tunnel.x1) * 3
    tunnel_height = (tunnel.y2 - tunnel.y1) * 3

    x1 = tunnel.x1 * 3

    # Fix offset of vertical tunnels
    if tunnel_height > tunnel_width:
        tunnel_height = tunnel_height - 1
        tunnel_width = tunnel_width + 1
    else:
        tunnel_width = tunnel_width - 1
        tunnel_height = tunnel_height + 1
        x1 = x1 - 1

    # TODO: Merge this with the place_room function because it is almost the same function
    generated_tunnel = generate_tunnel(tunnel_width, tunnel_height)

    merge_levels_with_offset(output_level, generated_tunnel, x1, tunnel.y1 * 3 - 1)

    return output_level


def generate_game_level(width, height):
    bsp_level = generate_bsp_level(width, height)

    # Uncomment if you're debugging the level
    # ascii_print_level(bsp_level)

    output_level = generate_tiled_compatible_level(width * 3, height * 3)

    # Place all rooms into the map
    for room in bsp_level.rooms:
        place_room(room, output_level)

    # TODO: Fix this logic because it's totally broken
    for tunnel in bsp_level.tunnels:
        place_tunnel(tunnel, output_level)

    return output_level


if __name__ == "__main__":
    test_parent = generate_tiled_compatible_level(18, 18)
    place_room(Rect(1, 1, 5, 5), test_parent)
    # map = generate_game_level(50, 50)
    print(test_parent)
