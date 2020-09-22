import arcade
import math

from Constants.Game import SPRITE_SIZE, SPRITE_SCALING_PLAYER
from Constants.Physics import PLAYER_MOVEMENT_SPEED

class Enemy(arcade.Sprite):

    def __init__(self, x, y, path, walls):
        self.x = x
        self.y = y
        self.speed = PLAYER_MOVEMENT_SPEED
        self.path = path
        self.obstacles = walls.layers[0].layer_data

        # Create enemy sprite
        self.enemy_sprite = arcade.Sprite(
            "Graphics/Character_animation/monsters_idle/skeleton1/v1/skeleton_v1_1.png", SPRITE_SCALING_PLAYER,
        )
        # Set enemy location
        enemy_grid_x = self.x + 8
        enemy_grid_y = self.y + 3
        self.enemy_sprite.center_x = SPRITE_SIZE * enemy_grid_x + SPRITE_SIZE / 2
        self.enemy_sprite.center_y = SPRITE_SIZE * enemy_grid_y + SPRITE_SIZE / 2

    def draw(self):
        if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)

    def on_update(self, path):
        self.path = path
        # print(self.path)