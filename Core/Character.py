import arcade

from Constants.Game import (
    SPRITE_SCALING_PLAYER,
    DOWN_FACING,
    UP_FACING,
    RIGHT_FACING,
    LEFT_FACING,
    SPRITE_SIZE)
from Constants.Animation import WALK_CYCLE_LENGTH, IDLE_CYCLE_LENGTH


class Character(arcade.Sprite):
    """ Player Sprite"""

    def __init__(self, main_path=''):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = DOWN_FACING
        self.character_face_direction_horizontal = RIGHT_FACING

        # coords
        self.center_x = 0
        self.center_y = 0

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.sub_texture = 0
        self.frames = IDLE_CYCLE_LENGTH
        self.scale = SPRITE_SCALING_PLAYER
        self.idle_list=[]
        # Track our states (leaving this here in case we need to have like.  casting states and stuff)

        # --- Load Textures ---

        self.main_path = main_path

        # Set the initial texture
        self.texture = None


    def load_textures(self):
        # Load textures for idle standing
        for i in range(1, 5):
            self.idle_list.append(arcade.load_texture_pair(
            f"{self.main_path}_{i}.png"
        ))
        self.texture = self.idle_list[0][0]
        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

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

