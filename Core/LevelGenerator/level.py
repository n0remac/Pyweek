import math
from typing import List, Any

from Core.LevelGenerator.shapes import Rect


class Level:
    rooms: List[Rect]
    tunnels: List[Rect]

    def __init__(self, width, height, mode="bsp"):
        if mode != "bsp":
            raise Exception("Only handles bsp mode atm")

        self.width = width
        self.height = height

        self.rooms = []
        self.tunnels = []
        self.tiles = [[[1, -1] for y in range(height)] for x in range(width)]

    def create_room(self, room: Rect, room_id: int):
        self.rooms.append(room)

        # set all tiles within a rectangle to 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y][0] = 0
                self.tiles[x][y][1] = room_id

    def create_hor_tunnel(self, x1_raw, x2_raw, y_raw):
        x1 = math.floor(x1_raw)
        x2 = math.floor(x2_raw)
        y = math.floor(y_raw)

        start = min(x1, x2)
        end = max(x1, x2) + 1

        tunnel = Rect(start, y, end - start, 1)

        self.tunnels.append(tunnel)

        for x in range(start, end):
            self.tiles[x][y][0] = 2

        return tunnel

    def create_vir_tunnel(self, y1_raw, y2_raw, x_raw):
        y1 = math.floor(y1_raw)
        y2 = math.floor(y2_raw)
        x = math.floor(x_raw)

        start = min(y1, y2)
        end = max(y1, y2)

        tunnel = Rect(x, start, 1, end - start)

        self.tunnels.append(tunnel)

        for y in range(start, end):
            self.tiles[x][y][0] = 2

        return tunnel
