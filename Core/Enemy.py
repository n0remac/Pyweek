import arcade
import math

from Constants.Game import SPRITE_SIZE, SPRITE_SCALING_PLAYER
from Constants.Physics import PLAYER_MOVEMENT_SPEED


class Enemy(arcade.Sprite):

    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        self.speed = PLAYER_MOVEMENT_SPEED
        self.path = [self.x, self.y]
        self.end = end

        # Create enemy sprite
        self.enemy_sprite = arcade.Sprite(
            "Graphics/Character_animation/monsters_idle/skeleton1/v1/skeleton_v1_1.png", SPRITE_SCALING_PLAYER,
        )
        # Set enemy location
        enemy_grid_x = 15
        enemy_grid_y = 8
        self.enemy_sprite.center_x = SPRITE_SIZE * enemy_grid_x + SPRITE_SIZE / 2
        self.enemy_sprite.center_y = SPRITE_SIZE * enemy_grid_y + SPRITE_SIZE / 2

        # print(self.enemy_sprite.center_x)

    def on_update(self):
        pass