from __future__ import annotations

import math
import random
from typing import Optional

from Core.LevelGenerator.leaf import Leaf
from Core.LevelGenerator.level import Level
from Core.LevelGenerator.shapes import Rect


class InvalidTunnelException(Exception):
    pass


def create_rooms(level: Level, leaf: Leaf):
    """
    Goes through the BSP tree of leafs and creates rooms that fit inside of the boundaries
    :param level: Instance of the level to create the rooms and hallways inside of
    :param leaf: Leaf node to recursively follow to recurse the entire BSP tree
    """
    if leaf.child_1 or leaf.child_2:
        # recursively search for children until you hit the end of the branch
        if leaf.child_1:
            create_rooms(level, leaf.child_1)
        if leaf.child_2:
            create_rooms(level, leaf.child_2)

        if leaf.child_1 and leaf.child_2:
            create_hall(level, leaf.child_1, leaf.child_2)

    else:
        # Create rooms in the end branches of the bsp tree
        w = random.randint(math.floor(leaf.width / 2 + 1), min(leaf.MAX_LEAF_SIZE - 2, leaf.width - 1))
        h = random.randint(math.floor(leaf.height / 2 + 1), min(leaf.MAX_LEAF_SIZE - 2, leaf.height - 1))
        x = random.randint(leaf.x, leaf.x + (leaf.width - 1) - w)
        y = random.randint(leaf.y, leaf.y + (leaf.height - 1) - h)

        # TODO: Make this side-effect free
        leaf.room = Rect(x, y, w, h)
        level.create_room(leaf.room, leaf.id)


def are_vertically_aligned(room1: Rect, room2: Rect):

    # horizontally aligned
    if room2.y1 <= room1.y1 < room2.y2 - 1 or room1.y1 <= room2.y1 < room1.y2 - 1:
        return False

    # vertically aligned
    if room2.x1 <= room2.x1 < room2.x2 - 1 or room1.x1 <= room2.x1 < room1.x2 - 1:
        return True

    raise InvalidTunnelException("not aligned on any axis")


def add_connection_to_leaf(leaf1: Leaf, leaf2: Leaf, tunnel: Rect):
    leaf1.connections[leaf2.id] = (leaf2, tunnel)
    leaf2.connections[leaf1.id] = (leaf1, tunnel)


def create_hall(level: Level, leaf1: Leaf, leaf2: Leaf):
    """
    Connect two rooms by hallways.
    This algorithm works by detecting alignment between two rooms, then creating a hallway between the "overlap" of
    the rooms. It's pretty basic, but it works.
    :param level: Instance of the level to add the hallway for
    :param leaf1: First room to connect
    :param leaf2: Second room to connect
    """

    room1 = leaf1.room
    room2 = leaf2.room

    if room1 is None or room2 is None:
        return

    if leaf1.id is None or leaf2.id is None:
        raise Exception("Leafs are missing ids")

    # Don't re-add rooms
    if leaf2.id in leaf1.connections or leaf1.id in leaf2.connections:
        return

    x1, y1 = room1.center()
    x2, y2 = room2.center()

    vertically_aligned = are_vertically_aligned(room1, room2)

    if vertically_aligned:
        if room1.y2 < room2.y1:
            top = room1.y2
            bottom = room2.y1 + 1
        else:
            top = room2.y2
            bottom = room1.y1 + 1

        if x1 < x2:
            left = x1 + round((x2 - x1) / 2)
            if left - 1 < room2.x1:
                left = room2.x1 + 1
            elif left >= room1.x2:
                left = room1.x2 - 1
        else:
            left = x2 + round((x1 - x2) / 2)
            if left - 1 > room2.x2:
                left = room2.x2 + 1
            elif left <= room1.x1:
                left = room1.x1 - 1

        # don't create super long tunnels
        if bottom - top > leaf1.MAX_LEAF_SIZE / 2:
            return

        # dont produce invalid tunnels
        for room in level.rooms:
            if room.x1 < left < room.x2:
                if room.y1 > top and room.y2 < bottom:
                    raise InvalidTunnelException()

        tunnel = level.create_vir_tunnel(top, bottom, left)

        add_connection_to_leaf(leaf1, leaf2, tunnel)
        return

    if room1.x2 < room2.x1:
        left = room1.x2
        right = room2.x1
    else:
        left = room2.x2
        right = room1.x1

    if y1 < y2:
        top = y1 + round((y2 - y1) / 2)
        if top - 1 < room2.y1:
            top = room2.y1
        elif top >= room1.y2:
            top = room1.y2 - 1
    else:
        top = y2 + round((y1 - y2) / 2)
        if top > room2.y2:
            top = room2.y2 - 1
        elif top <= room1.y1:
            top = room1.y1


    # don't create super long tunnels
    if right - left > leaf1.MAX_LEAF_SIZE / 2:
        return

    # dont produce invalid tunnels
    for room in level.rooms:
        if room.y1 < top < room.y2:
            if room.x1 > left and room.x2 < right:
                raise InvalidTunnelException()

    tunnel = level.create_hor_tunnel(left, right, top)

    add_connection_to_leaf(leaf1, leaf2, tunnel)


def split_leaf(leaf: Leaf):
    """
    Slits a leaf into 2 children to partition the space using a BSP tree
    :param leaf: Leaf to split into two spaces
    :return: Boolean value of if the leaf split
    """
    # begin splitting the leaf into two children
    if (leaf.child_1 is not None) or (leaf.child_2 is not None):
        return False  # This leaf has already been split

    """
    ==== Determine the direction of the split ====
    If the width of the leaf is >25% larger than the height,
    split the leaf vertically.
    If the height of the leaf is >25 larger than the width,
    split the leaf horizontally.
    Otherwise, choose the direction at random.
    """
    split_horizontally = random.choice([True, False])
    if leaf.width / leaf.height >= 1.25:
        split_horizontally = False
    elif leaf.height / leaf.width >= 1.25:
        split_horizontally = True

    if split_horizontally:
        max_leaf = leaf.height - leaf.MIN_LEAF_SIZE
    else:
        max_leaf = leaf.width - leaf.MIN_LEAF_SIZE

    if max_leaf <= leaf.MIN_LEAF_SIZE:
        return False  # the leaf is too small to split further

    split = random.randint(
        leaf.MIN_LEAF_SIZE, max_leaf
    )  # determine where to split the leaf

    if split_horizontally:
        leaf.child_1 = Leaf(leaf.x, leaf.y, leaf.width, split, leaf)
        leaf.child_2 = Leaf(leaf.x, leaf.y + split, leaf.width, leaf.height - split, leaf)
    else:
        leaf.child_1 = Leaf(leaf.x, leaf.y, split, leaf.height, leaf)
        leaf.child_2 = Leaf(leaf.x + split, leaf.y, leaf.width - split, leaf.height, leaf)

    return True


def get_room(leaf: Leaf) -> Optional[Rect]:
    """
    Grabs the "room" associated with a given leaf.
    Note: Need to confirm the behavior of this because it will randomly pick a room if both are available.
    Not exactly sure how that affects the level generation.
    :param leaf: Leaf the try to locate the room for
    :return: Instance of the room, if one exists.
    """
    if leaf.room:
        return leaf.room

    else:
        room_1 = None
        room_2 = None
        if leaf.child_1:
            room_1 = get_room(leaf.child_1)
        if leaf.child_2:
            room_2 = get_room(leaf.child_2)

        if not leaf.child_1 and not leaf.child_2:
            # neither room_1 nor room_2
            return None

        elif not room_2:
            # room_1 and !room_2
            return room_1

        elif not room_1:
            # room_2 and !room_1
            return room_2

        # If both room_1 and room_2 exist, pick one
        # TODO: How does this work? Why not go left or right every time? Need to understand BSP trees better.
        elif random.random() < 0.5:
            return room_1
        else:
            return room_2


