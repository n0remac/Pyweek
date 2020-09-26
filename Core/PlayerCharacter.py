import arcade
import math

from Constants.Game import SPRITE_IMAGE_SIZE

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
        self.game_resources = game_resources
        self.main_path = "Graphics/Character_animation/Acolyte/player_animation_down_idle"
        self.load_textures()



    def on_mouse_motion(self, x, y, dx, dy):
        # Figure out if we need to flip face up or down or left or right
        player_x = math.floor(self.center_x / SPRITE_IMAGE_SIZE)
        view_x = math.floor(self.game_resources.view_left / SPRITE_IMAGE_SIZE)
        mouse_x =  math.floor(x / SPRITE_IMAGE_SIZE)

        if (
                player_x < mouse_x + view_x
            and self.character_face_direction_horizontal == LEFT_FACING
        ):
            self.character_face_direction_horizontal = RIGHT_FACING
        elif (
            player_x > mouse_x + view_x
            and self.character_face_direction_horizontal == RIGHT_FACING
        ):
            self.character_face_direction_horizontal = LEFT_FACING

    def update_animation(self, delta_time: float = 1 / 60):
        # Animation
        self.sub_texture += 1  # delta_time/60
        if self.sub_texture > (60 / self.frames):
            self.sub_texture -= 60 / self.frames
            self.cur_texture += 1
            self.frames = IDLE_CYCLE_LENGTH
            if self.cur_texture > (self.frames-1):
                self.cur_texture = 0
            # idle animation
            self.texture = self.idle_list[self.cur_texture][self.character_face_direction_horizontal]
