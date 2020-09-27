from typing import Optional, Dict


class Leaf:
    """
    Used for the BSP tree algorithm
    TODO: Make this a non-mutable data structure so that the algorithms have to generate new leafs instead of modifying
    this one directly.
    TODO: Move the constants to somewhere else, or at least make them configurable.
    """

    def __init__(self, x, y, width, height, parent):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.MIN_LEAF_SIZE = 11
        self.MAX_LEAF_SIZE = 18
        self.child_1 = None
        self.child_2 = None
        self.parent = parent
        self.room = None
        self.connections = dict()
        self.id = -1
