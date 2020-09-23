from __future__ import annotations

import random

from Core.LevelGenerator.level import Level
from Core.LevelGenerator.shapes import Rect


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
			create_hall(level, get_room(leaf.child_1), get_room(leaf.child_2))

	else:
		# Create rooms in the end branches of the bsp tree
		w = random.randint(leaf.ROOM_MIN_SIZE, min(leaf.ROOM_MAX_SIZE, leaf.width - 1))
		h = random.randint(leaf.ROOM_MIN_SIZE, min(leaf.ROOM_MAX_SIZE, leaf.height - 1))
		x = random.randint(leaf.x, leaf.x + (leaf.width - 1) - w)
		y = random.randint(leaf.y, leaf.y + (leaf.height - 1) - h)

		# TODO: Make this side-effect free
		leaf.room = Rect(x, y, w, h)
		level.create_room(leaf.room)


def create_hall(level: Level, room1: Rect, room2: Rect):
	"""
	Connect two rooms by hallways
	:param level: Instance of the level to add the hallway for
	:param room1: First room to connect
	:param room2: Second room to connect
	"""
	x1, y1 = room1.center()
	x2, y2 = room2.center()
	# 50% chance that a tunnel will start horizontally
	if random.randint(0, 1) == 1:
		level.create_hor_tunnel(x1, x2, y1)
		level.create_vir_tunnel(y1, y2, x2)

	else:  # else it starts vertically
		level.create_vir_tunnel(y1, y2, x1)
		level.create_hor_tunnel(x1, x2, y2)


def split_leaf(leaf: Leaf):
	"""
	Slits a leaf into 2 children to partition the space using a BSP tree
	:param leaf: Leaf to split into two spaces
	:return: Boolean value of if the leaf split
	"""
	# begin splitting the leaf into two children
	if (leaf.child_1 is not None) or (leaf.child_2 is not None):
		return False  # This leaf has already been split

	'''
	==== Determine the direction of the split ====
	If the width of the leaf is >25% larger than the height,
	split the leaf vertically.
	If the height of the leaf is >25 larger than the width,
	split the leaf horizontally.
	Otherwise, choose the direction at random.
	'''
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

	split = random.randint(leaf.MIN_LEAF_SIZE, max_leaf)  # determine where to split the leaf

	if split_horizontally:
		leaf.child_1 = Leaf(leaf.x, leaf.y, leaf.width, split)
		leaf.child_2 = Leaf(leaf.x, leaf.y + split, leaf.width, leaf.height - split)
	else:
		leaf.child_1 = Leaf(leaf.x, leaf.y, split, leaf.height)
		leaf.child_2 = Leaf(leaf.x + split, leaf.y, leaf.width - split, leaf.height)

	return True


def get_room(leaf: Leaf):
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


class Leaf:
	"""
	Used for the BSP tree algorithm
	TODO: Make this a non-mutable data structure so that the algorithms have to generate new leafs instead of modifying
	this one directly.
	TODO: Move the constants to somewhere else, or at least make them configurable.
	"""

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.MIN_LEAF_SIZE = 10
		self.MAX_LEAF_SIZE = 24
		self.ROOM_MAX_SIZE = 15
		self.ROOM_MIN_SIZE = 6
		self.child_1 = None
		self.child_2 = None
		self.room = None
		self.hall = None
