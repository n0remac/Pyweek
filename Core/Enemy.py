import arcade
import math

from Constants.Game import SPRITE_SIZE, SPRITE_SCALING_PLAYER
from Constants.Physics import PLAYER_MOVEMENT_SPEED


class Enemy(arcade.Sprite):
    def __init__(self, path, walls):
        super().__init__("Graphics/Character_animation/monsters_idle/skeleton1/v1/skeleton_v1_1.png", SPRITE_SCALING_PLAYER)
        self.speed = PLAYER_MOVEMENT_SPEED
        self.path = path
        self.obstacles = walls.layers[0].layer_data

    def draw(self):
        if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)

    def on_update(self, path, end):
        self.path = path
        if self.path and len(self.path) > 1:
            if self.path[0][0] < self.path[1][0]:
                self.center_x = self.center_x + 1
            elif self.path[0][0] > self.path[1][0]:
                self.center_x = self.center_x - 1

            if self.path[0][1] < self.path[1][1]:
                self.center_y = self.center_y + 1
            elif self.path[0][1] > self.path[1][1]:
                self.center_y = self.center_y - 1
