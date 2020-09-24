import arcade
import math

from Constants.Game import SPRITE_SIZE, SPRITE_SCALING_PLAYER
from Constants.Physics import PLAYER_MOVEMENT_SPEED


class Enemy(arcade.Sprite):
    def __init__(self, game_resources):
        super().__init__("Graphics/Character_animation/monsters_idle/skeleton1/v1/skeleton_v1_1.png", SPRITE_SCALING_PLAYER)
        self.game_resources = game_resources
        self.speed = PLAYER_MOVEMENT_SPEED
        self.path = [self.game_resources.player_sprite.center_x, self.game_resources.player_sprite.center_y]
        self.obstacles = self.game_resources.wall_list

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
