import arcade
import math

from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Constants.Game import (
    SPRITE_SCALING_PLAYER,
    DOWN_FACING,
    UP_FACING,
    RIGHT_FACING,
    LEFT_FACING,
)
from Constants.Animation import WALK_CYCLE_LENGTH, IDLE_CYCLE_LENGTH

# from Core.Projectiles.Projectile_Manager import angle


class PlayerCharacter(arcade.Sprite):
    """ Player Sprite"""

    def __init__(self):

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
        # Track our states (leaving this here in case we need to have like.  casting states and stuff)

        # --- Load Textures ---

        main_path = "Graphics/Character_animation/player_animation/player_animation"

        # Load textures for idle standing
        self.down_idle_texture_pair = arcade.load_texture_pair(
            f"{main_path}_down_idle0.png"
        )
        self.down_walk_texture_pair = arcade.load_texture_pair(
            f"{main_path}_down_walk0.png"
        )
        self.up_idle_texture_pair = arcade.load_texture_pair(
            f"{main_path}_up_idle0.png"
        )
        self.up_walk_texture_pair = arcade.load_texture_pair(
            f"{main_path}_up_walk0.png"
        )

        self.down_walk_textures = []
        for i in range(WALK_CYCLE_LENGTH):
            texture = arcade.load_texture_pair(f"{main_path}_down_walk{i}.png")
            self.down_walk_textures.append(texture)

        self.down_idle_textures = []
        for i in range(IDLE_CYCLE_LENGTH):
            texture = arcade.load_texture_pair(f"{main_path}_down_idle{i}.png")
            self.down_idle_textures.append(texture)

        self.up_walk_textures = []
        for i in range(WALK_CYCLE_LENGTH):
            texture = arcade.load_texture_pair(f"{main_path}_up_walk{i}.png")
            self.up_walk_textures.append(texture)

        self.up_idle_textures = []
        for i in range(IDLE_CYCLE_LENGTH):
            texture = arcade.load_texture_pair(f"{main_path}_up_idle{i}.png")
            self.up_idle_textures.append(texture)

        # Set the initial texture
        self.texture = self.down_idle_texture_pair[0]

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
            if self.change_x == 0 and self.change_y == 0:
                self.frames = IDLE_CYCLE_LENGTH
                if self.cur_texture > (self.frames - 2):
                    self.cur_texture = 0
                # idle animation
                if self.character_face_direction == DOWN_FACING:
                    self.texture = self.down_idle_textures[self.cur_texture][
                        self.character_face_direction_horizontal
                    ]
                    return
                else:
                    self.texture = self.up_idle_textures[self.cur_texture][
                        self.character_face_direction_horizontal
                    ]
                return
            else:
                # Walking animation
                self.frames = WALK_CYCLE_LENGTH
                if self.cur_texture > (self.frames - 2):
                    self.cur_texture = 0
                if self.character_face_direction == DOWN_FACING:
                    self.texture = self.down_walk_textures[self.cur_texture][
                        self.character_face_direction_horizontal
                    ]
                    return
                else:
                    self.texture = self.up_walk_textures[self.cur_texture][
                        self.character_face_direction_horizontal
                    ]

    def on_mouse_motion(self, x, y, dx, dy):
        # Figure out if we need to flip face up or down or left or right
        if self.center_y < y and self.character_face_direction == DOWN_FACING:
            self.character_face_direction = UP_FACING
        elif self.center_y > y and self.character_face_direction == UP_FACING:
            self.character_face_direction = DOWN_FACING
        if (
            self.center_x < x
            and self.character_face_direction_horizontal == LEFT_FACING
        ):
            self.character_face_direction_horizontal = RIGHT_FACING
        elif (
            self.center_x > x
            and self.character_face_direction_horizontal == RIGHT_FACING
        ):
            self.character_face_direction_horizontal = LEFT_FACING
