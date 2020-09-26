import arcade
import math

from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Constants.Game import (
    SPRITE_SCALING_PLAYER,
    DOWN_FACING,
    UP_FACING,
    RIGHT_FACING,
    LEFT_FACING,
    SPRITE_SIZE)
from Constants.Animation import WALK_CYCLE_LENGTH, IDLE_CYCLE_LENGTH

from Core.Character import Character


class PlayerCharacter(Character):
    """ Player Sprite"""

    def __init__(self, position, game_resources):

        # Set up parent class
        super().__init__(position)
        self.main_path = "Graphics/Character_animation/player_animation/player_animation_down_idle"
        self.load_textures()

        #store game resources
        self.game_resources = game_resources


    def on_mouse_motion(self, x, y, dx, dy):
        # Figure out if we need to flip face up or down or left or right
        if (self.center_y < (y + self.game_resources.view_bottom)
            and self.character_face_direction == DOWN_FACING):
            self.character_face_direction = UP_FACING
        elif (self.center_y > (y + self.game_resources.view_bottom)
            and self.character_face_direction == UP_FACING):
            self.character_face_direction = DOWN_FACING
        if (
            self.center_x < (x + self.game_resources.view_left)
            and self.character_face_direction_horizontal == LEFT_FACING
        ):
            self.character_face_direction_horizontal = RIGHT_FACING
        elif (
            self.center_x > x + self.game_resources.view_left
            and self.character_face_direction_horizontal == RIGHT_FACING
        ):
            self.character_face_direction_horizontal = LEFT_FACING
