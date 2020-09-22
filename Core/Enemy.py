import arcade
import math

from Constants.Game import SPRITE_SIZE, SPRITE_SCALING_PLAYER
from Constants.Physics import PLAYER_MOVEMENT_SPEED

class Enemy(arcade.Sprite):

    def __init__(self, x, y, end_x, end_y):
        self.x = x
        self.y = y
        self.speed = PLAYER_MOVEMENT_SPEED
        self.end_x = end_x
        self.end_y = end_y

        # Create enemy sprite
        self.enemy_sprite = arcade.Sprite(
            "Graphics/Character_animation/monsters_idle/skeleton1/v1/skeleton_v1_1.png", SPRITE_SCALING_PLAYER,
        )
        # Set enemy location
        enemy_grid_x = self.x + 8
        enemy_grid_y = self.y + 3
        self.enemy_sprite.center_x = SPRITE_SIZE * enemy_grid_x + SPRITE_SIZE / 2
        self.enemy_sprite.center_y = SPRITE_SIZE * enemy_grid_y + SPRITE_SIZE / 2

    def draw(self, x, y):
        self.on_update(x, y)

    def on_update(self, x, y):
        if self.enemy_sprite.center_x < x:
            self.enemy_sprite.center_x = self.enemy_sprite.center_x + .5
        elif self.enemy_sprite.center_x > x:
            self.enemy_sprite.center_x = self.enemy_sprite.center_x - .5

        if self.enemy_sprite.center_y < y:
            self.enemy_sprite.center_y = self.enemy_sprite.center_y + .5
        elif self.enemy_sprite.center_y > y:
            self.enemy_sprite.center_y = self.enemy_sprite.center_y - .5