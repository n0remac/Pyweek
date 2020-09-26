from typing import List, Dict, AnyStr, Optional

from pytiled_parser.objects import TiledObject, OrderedPair, Size

from Constants.Game import SPRITE_IMAGE_SIZE
from Core.LevelGenerator.bsp_tree import generate_bsp_level, ascii_print_level
from Core.LevelGenerator.level import Level
from Core.LevelGenerator.room_generation import generate_room, generate_tunnel, warps, get_tile_from_list

from Core.LevelGenerator.shapes import Rect
from Core.LevelGenerator.tiled_mapper.tiled_compatible_level import (
    generate_tiled_compatible_level,
    merge_levels_with_offset,
)


def place_room(room: Rect, warp_next: Optional[int], warp_dest_room: Rect, output_level: Dict[AnyStr, List[List[int]]]):
    # Note: This function is not referentially transparent and relies on side effects to mutate output_level
    room_width = (room.x2 - room.x1) * 3
    room_height = (room.y2 - room.y1) * 3

    # All rooms are 3x the size in the game versus the generator to allow hallways to have all tile types
    room_tiles = generate_room(room_width, room_height)

    merge_levels_with_offset(output_level, room_tiles, room.x1 * 3, room.y1 * 3)

    if warp_next is not None:
        if "Warps" not in output_level:
            output_level["Warps"] = []

        # Warp to location, with a slight offset
        warp_to_x = (warp_dest_room.x1 + ((warp_dest_room.x2 - warp_dest_room.x1) / 2)) * 3 * SPRITE_IMAGE_SIZE + 32
        warp_to_y = (warp_dest_room.y1 + ((warp_dest_room.y2 - warp_dest_room.y1) / 2)) * 3 * SPRITE_IMAGE_SIZE + 32

        properties_dict = dict()
        properties_dict["warp_to_id"] = warp_next
        properties_dict["warp_to_location"] = (warp_to_x, warp_to_y)
        output_level["Warps"].append(TiledObject(
            id_ = 1000 + warp_next,
            gid=get_tile_from_list(warps),
            size=Size(width=SPRITE_IMAGE_SIZE, height=SPRITE_IMAGE_SIZE),
            location = OrderedPair(
                x=(room.x1 * 3 + round(room_width / 2)) * SPRITE_IMAGE_SIZE,
                y=(room.y1 * 3 + round(room_height / 2)) * SPRITE_IMAGE_SIZE
            ),
            properties=properties_dict
        ))

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


def get_room_by_leaf_id(bsp_level: Level, leaf_id: int) -> Rect:
    for leaf in bsp_level.end_leafs:
        if leaf.id == leaf_id:
            return leaf.room

    raise Exception("leaf ID not found")


def generate_game_level(width, height):
    bsp_level = generate_bsp_level(width, height)

    # Uncomment if you're debugging the level
    # ascii_print_level(bsp_level)

    output_level = generate_tiled_compatible_level(width * 3, height * 3)

    # list of sub-graphs representing connected rooms
    # crazy casts are to give us unique values, but we need it to be a list so that we can sort it
    graph_numbers = list(set(bsp_level.node_to_graph.values()))

    # sort it again so that we can put stuff at the "start"
    graph_numbers.sort()

    graph_id_to_nodes = dict()

    # creates a lookup of graph ID to list of nodes
    for node_id in bsp_level.node_to_graph:
        node_graph_id = bsp_level.node_to_graph[node_id]

        if node_graph_id not in graph_id_to_nodes:
            graph_id_to_nodes[node_graph_id] = []

        graph_id_to_nodes[node_graph_id].append(node_id)

    room_to_warp_map = dict()

    starting_room_id = None

    # place warps
    # TODO: Make sure first sub-graph always has more than 1 node, just in case
    for graph_id_index in range(0, len(graph_numbers) - 1):
        graph_id = graph_numbers[graph_id_index]
        leaf_ids = graph_id_to_nodes[graph_id]

        if graph_id_index == 0:
            starting_room_id = leaf_ids[0]

        end_room = leaf_ids[-1]

        next_graph = graph_id_to_nodes[graph_numbers[graph_id_index + 1]]

        # connect last room to the first room in next graph
        room_to_warp_map[end_room] = next_graph[0]

        # connect first room to the last room in this graph
        room_to_warp_map[next_graph[0]] = end_room

    # Place all rooms into the map
    for leaf in bsp_level.end_leafs:
        warp_to_id: Optional[int] = None

        if leaf.id == starting_room_id:
            width = (leaf.room.x2 - leaf.room.x1) * 3
            height = (leaf.room.y2 - leaf.room.y1) * 3
            # Ultra hack-job to get the start location in the Tiled coordinate system...
            output_level["start_location"] = [TiledObject(
                id_ = 999,
                gid=get_tile_from_list(warps),
                size=Size(width=SPRITE_IMAGE_SIZE, height=SPRITE_IMAGE_SIZE),
                location = OrderedPair(
                    x=(leaf.room.x1 * 3 + round(width / 2)) * SPRITE_IMAGE_SIZE,
                    y=(leaf.room.y1 * 3 + round(height / 2)) * SPRITE_IMAGE_SIZE
                )
            )]

        if leaf.id in room_to_warp_map:
            warp_to_id = room_to_warp_map[leaf.id]
            warp_to_location = get_room_by_leaf_id(bsp_level, warp_to_id)

        place_room(leaf.room, warp_to_id, warp_to_location, output_level)


    # TODO: Fix this logic because it's totally broken
    for tunnel in bsp_level.tunnels:
        place_tunnel(tunnel, output_level)

    return output_level


if __name__ == "__main__":
    test_parent = generate_tiled_compatible_level(18, 18)
    place_room(Rect(1, 1, 5, 5), test_parent)
    # map = generate_game_level(50, 50)
    print(test_parent)
