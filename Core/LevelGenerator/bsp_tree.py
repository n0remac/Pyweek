import random

from Core.LevelGenerator.common import Leaf, split_leaf, create_rooms
from Core.LevelGenerator.level import Level

# TODO: Take this level generator and feed the output into a Tiled converter.


def generate_bsp_level(map_width, map_height):
    # TODO: Allow passing seed

    # Creates an empty 2D array or clears existing array
    level_instance = Level(map_height, map_height)

    leafs = []

    root_leaf = Leaf(0, 0, map_width, map_height)
    leafs.append(root_leaf)

    split_successfully = True
    # loop through all leaves until they can no longer split successfully
    while split_successfully:
        split_successfully = False
        for leaf in leafs:
            if (leaf.child_1 is None) and (leaf.child_2 is None):
                if (leaf.width > leaf.MAX_LEAF_SIZE) or (leaf.height > leaf.MAX_LEAF_SIZE) or (random.random() > 0.8):
                    if split_leaf(leaf):  # try to split the leaf
                        leafs.append(leaf.child_1)
                        leafs.append(leaf.child_2)
                        split_successfully = True

    create_rooms(level_instance, root_leaf)

    return level_instance


# Test script for if you want to generate a level for fun
if __name__ == "__main__":
    level = generate_bsp_level(80, 80)

    for y in range(0, level.height):
        row = ""
        for x in range(0, level.width):
            if level.tiles[x][y] == 0:
                row += " "
            else:
                row += "#"

        # Super basic way to print the level in ASCII
        print(row)

