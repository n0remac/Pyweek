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
from Core.HealthRing import Health


class PlayerCharacter(Character):
    """ Player Sprite"""

    def __init__(self, position, game_resources, scene_renderer):

        # Set up parent class
        super().__init__(position)
        self.game_resources = game_resources
        self.main_path = "Graphics/Character_animation/Acolyte/player_animation_down_idle"
        self.load_textures()

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.x_force = 0
        self.y_force = 0
        self.speed = 40

        self.walk_textures = []
        walk_path = 'Graphics/Character_animation/Acolyte/player_animation_down_walk'
        for i in range(1, 5):
            self.walk_textures.append(arcade.load_texture_pair(
            f"{walk_path}_{i}.png"
        ))

        self.player_light = scene_renderer.light_renderer.create_point_light(
            (400, 400),  # Position
            (
                1.75,
                1.75,
                1.75,
            ),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB This can go over 1.0 because of HDR
            160.0,
        )  # Radius

        # player heath system
        self.player_health = Health(
            self.player_light, scene_renderer.post_processing
        )

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
            if self.x_force != 0 or self.y_force != 0:
                self.texture = self.walk_textures[self.cur_texture][self.character_face_direction_horizontal]
            else:
                self.texture = self.idle_list[self.cur_texture][self.character_face_direction_horizontal]

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.game_resources.object_manager.candle(self.game_resources.player_sprite.position[0] - 5,
                                                      self.game_resources.player_sprite.position[1])

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_update(self, delta_time):
        self.x_force = 0
        self.y_force = 0

        if self.up_pressed:
            self.y_force += self.speed
        if self.down_pressed:
            self.y_force -= self.speed
        if self.left_pressed:
            self.x_force -= self.speed
        if self.right_pressed:
            self.x_force += self.speed

        # move the player light to the player
        self.player_light.position = (
            self.game_resources.player_sprite.center_x,
            self.game_resources.player_sprite.center_y,
        )
