import math

from Core.LevelGenerator.shapes import Rect


class Level:
	def __init__(self, width, height, mode="bsp"):
		if mode != "bsp":
			raise Exception("Only handles bsp mode atm")

		self.width = width
		self.height = height

		self.rooms = []
		self.tunnels = []
		self.tiles = [[1 for y in range(height)] for x in range(width)]

	def create_room(self, room: Rect):
		self.rooms.append(room)

		# set all tiles within a rectangle to 0
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.tiles[x][y] = 0

	def create_hor_tunnel(self, x1_raw, x2_raw, y_raw):
		x1 = math.floor(x1_raw)
		x2 = math.floor(x2_raw)
		y = math.floor(y_raw)

		start = min(x1, x2)
		end = max(x1, x2) + 1

		self.tunnels.append(Rect(y, start, end - start, 1))

		for x in range(start, end):
			self.tiles[x][y] = 0

	def create_vir_tunnel(self, y1_raw, y2_raw, x_raw):
		y1 = math.floor(y1_raw)
		y2 = math.floor(y2_raw)
		x = math.floor(x_raw)

		start = min(y1, y2)
		end = max(y1, y2) + 1

		self.tunnels.append(Rect(x, start, 1, end - start))

		for y in range(start, end):
			self.tiles[x][y] = 0
