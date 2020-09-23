import math
from typing import List, Dict, AnyStr

from Core.LevelGenerator.bsp_tree import generate_bsp_level
from Core.LevelGenerator.room_generation import generate_room, generate_tunnel

from Core.LevelGenerator.shapes import Rect
from Core.LevelGenerator.tiled_mapper.tiled_compatible_level import generate_tiled_compatible_level, \
    merge_levels_with_offset


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

    # TODO: Merge this with the place_room function because it is almost the same function
    generated_tunnel = generate_tunnel(tunnel_width, tunnel_height)

    merge_levels_with_offset(output_level, generated_tunnel, tunnel.x1, tunnel.y1)

    return output_level


def generate_tunnels_between_rooms_from_base_tunnel(rooms: List[Rect], tunnel: Rect):
    intersecting_rooms = []

    for room in rooms:
        if tunnel.intersect(room):
            intersecting_rooms.append(room)

    # TODO: Sort the rooms by a single axis
    output_tunnel_chunks = []

    # Check for vertical alignment
    tunnel_is_vertical = tunnel.x2 - tunnel.x1 == 1

    # Returns only one axis of the room. This algorithm requires that rooms do not intersect to work.
    def get_room_sort_dimension(sort_room):
        if tunnel_is_vertical:
            return sort_room.y1
        return sort_room.x1

    intersecting_rooms.sort(key=get_room_sort_dimension)

    for i in range(0, len(intersecting_rooms)):
        # If we're on the final room, skip it.
        if i + 1 == len(intersecting_rooms):
            break

        # Grab the current and next room to create a tunnel between
        room_1 = intersecting_rooms[i]
        room_2 = intersecting_rooms[i + 1]

        if tunnel_is_vertical:
            # Get the center of the room, offset by 1 to align it
            tunnel_x = math.floor((room_1.x2 - room_1.x1) / 2) - 1
            tunnel_y = room_1.y2
            tunnel_width = 3
            tunnel_height = room_2.y1 - room_1.y2
            output_tunnel_chunks.append(Rect(
                tunnel_x,
                tunnel_y,
                tunnel_width,
                tunnel_height
            ))
            break

        # Get the center of the room, offset by 1 to align it
        tunnel_x = math.floor((room_1.y2 - room_1.y1) / 2) - 1
        tunnel_y = room_1.x2
        tunnel_width = room_2.x1 - room_1.x2
        tunnel_height = 3
        output_tunnel_chunks.append(Rect(
            tunnel_x,
            tunnel_y,
            tunnel_width,
            tunnel_height
        ))

    return output_tunnel_chunks


def generate_game_level(width, height):
    bsp_level = generate_bsp_level(width, height)

    output_level = generate_tiled_compatible_level(width * 3, height * 3)

    # Place all rooms into the map
    for room in bsp_level.rooms:
        place_room(room, output_level)

    # TODO: Fix this logic because it's totally broken
    # for tunnel in bsp_level.tunnels:
    #     # splits up a tunnel into "chunks" that exist between rooms.
    #     # the BSP algorithm can generate tunnels that intersect with rooms, so this prevents that problem
    #     # TODO: tunnels can overlap as well and form 90 degree tunnels between rooms
    #     tunnel_chunks = generate_tunnels_between_rooms_from_base_tunnel(bsp_level.rooms, tunnel)
    #
    #     for tchunk in tunnel_chunks:
    #         place_tunnel(tchunk, output_level)

    return output_level


if __name__ == "__main__":
    map = generate_game_level(50, 50)
    print(map)
