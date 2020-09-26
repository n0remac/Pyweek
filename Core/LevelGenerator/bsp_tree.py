import random
from typing import List, Tuple

from Core.LevelGenerator.common import split_leaf, create_rooms, create_hall, get_room, InvalidTunnelException
from Core.LevelGenerator.leaf import Leaf
from Core.LevelGenerator.graph import populate_subgraph
from Core.LevelGenerator.level import Level

# TODO: Take this level generator and feed the output into a Tiled converter.


def ascii_print_level(level: Level):
    for y in range(0, level.height):
        row = ""
        for x in range(0, level.width):
            if level.tiles[x][y][0] == 0:
                char_str = str(level.tiles[x][y][1])
                if len(char_str) == 1:
                    char_str = "  " + char_str
                if len(char_str) == 2:
                    char_str = " " + char_str

                row += "," + char_str + ","
            elif level.tiles[x][y][0] == 2:
                row += " ... "
            else:
                row += " ### "

        # Super basic way to print the level in ASCII
        print(row)


def generate_bsp_level(map_width, map_height):
    # TODO: Allow passing seed

    # Creates an empty 2D array or clears existing array
    level_instance = Level(map_height, map_height)

    leafs = []

    root_leaf = Leaf(0, 0, map_width, map_height, None)
    leafs.append(root_leaf)

    split_successfully = True
    # loop through all leaves until they can no longer split successfully
    while split_successfully:
        split_successfully = False
        for leaf in leafs:
            if (leaf.child_1 is None) and (leaf.child_2 is None):
                if (
                    (leaf.width > leaf.MAX_LEAF_SIZE)
                    or (leaf.height > leaf.MAX_LEAF_SIZE)
                    or (random.random() > 0.8)
                ):
                    if split_leaf(leaf):  # try to split the leaf
                        leafs.append(leaf.child_1)
                        leafs.append(leaf.child_2)
                        split_successfully = True

    # TODO: Finish an algorithm to connect all rooms.
    # Or maybe just add warps to the "second" room?
    all_end_leafs: List[Leaf] = []
    leaf_pairs: List[Tuple[Leaf, Leaf]] = []

    # Python is so weird
    leaf_id = dict()
    leaf_id["id"] = 0

    def child_has_no_children(leaf: Leaf):
        return leaf.child_1 is None and leaf.child_2 is None

    def recurse_leaf(leaf: Leaf):
        leaf.id = leaf_id["id"]
        leaf_id["id"] += 1
        if leaf.child_1 is None and leaf.child_2 is None:
            all_end_leafs.append(leaf)

        if leaf.child_1:
            recurse_leaf(leaf.child_1)

        if leaf.child_2:
            recurse_leaf(leaf.child_2)

        if leaf.child_1 and leaf.child_2:
            if child_has_no_children(leaf.child_1) and child_has_no_children(leaf.child_2):
                leaf_pairs.append((leaf.child_1, leaf.child_2))

    recurse_leaf(root_leaf)

    # Attaches a room to every end leaf (and skips hallway logic)
    for end_leaf in all_end_leafs:
        create_rooms(level_instance, end_leaf)

    # Creates hallways between siblings
    for leaf_pair in leaf_pairs:
        try:
            create_hall(level_instance, leaf_pair[0], leaf_pair[1])
        except InvalidTunnelException:
            continue

    def collect_children(parent: Leaf):
        children = []

        if parent.child_1:
            children.append(parent.child_1)
            children = children + collect_children(parent.child_1)

        if parent.child_2:
            children.append(parent.child_2)
            children = children + collect_children(parent.child_2)

        return children

    def get_other_child(parent: Leaf, child: Leaf):
        if parent.child_1 == child:
            return parent.child_2

        return parent.child_1

    def connect_cousins(cousin_leaf: Leaf):
        parent = cousin_leaf.parent

        other_child = get_other_child(parent, cousin_leaf)

        other_cousins = collect_children(other_child)

        cousins_with_rooms = filter(lambda c: c.room is not None, other_cousins)

        for another_cousin in cousins_with_rooms:
            try:
                create_hall(level_instance, cousin_leaf, another_cousin)
            except InvalidTunnelException:
                # Safe exception to ignore because it just means we couldn't connect to any of our cousins
                continue

    # merge cousins
    for end_leaf in all_end_leafs:
        # don't add connections for leafs that already have some.
        # TODO: potentially add them but only if they don't already have a bunch?
        if len(end_leaf.connections) >= 1:
            continue

        connect_cousins(end_leaf)

    all_parent_leafs = filter(lambda l: l.room is None, all_end_leafs)


    for unconnected_leaf in filter(lambda l: len(l.connections) == 0, all_end_leafs):
        for another_node in all_end_leafs:
            try:
                create_hall(level_instance, unconnected_leaf, another_node)
            except InvalidTunnelException:
                # Safe exception to ignore because it just means we couldn't connect to any of our cousins
                continue

    # Commented out because these tunnels won't work for the game. They pass through other rooms.
    # create_rooms(level_instance, root_leaf)

    node_to_graph = populate_subgraph(leafs)

    level_instance.node_to_graph = node_to_graph
    level_instance.end_leafs = all_end_leafs

    return level_instance


# Test script for if you want to generate a level for fun
if __name__ == "__main__":
    level = generate_bsp_level(80, 80)
