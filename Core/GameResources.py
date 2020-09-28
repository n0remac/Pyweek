import random
import sys

import arcade
import math
from Core.lerp import lerp
from pytiled_parser.objects import TileLayer, Size, ObjectLayer

from Core.Enemy import EnemyManager
from Constants.Game import (
    SPRITE_SCALING_TILES,
    SPRITE_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    LERP_MARGIN,
    CAMERA_SPEED
)
from Core.ArcadeUtils import convert_from_tiled_coordinates
from Core.LevelGenerator.generate_game_level import generate_game_level
from Core.PlayerCharacter import PlayerCharacter
from Core.ObjectManager import ObjectManager
from Core.Projectile_Manager import ProjectileManager


class GameResources:
    """
    Load arcade resources
    """

    def __init__(self, scene_renderer):

        self.scene_renderer = scene_renderer
        # Create the sprite lists
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.object_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_list = arcade.SpriteList()

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Read in the tiled map
        map_name = "Graphics/test_map.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)

        # Cache a copy of this to use for the location conversion function
        self.my_map = my_map

        # Procedurally generated map
        generated_map = generate_game_level(60, 60)

        # Screenshake
        self.shake_remain = 0
        self.shake_strength = 1
        self.shake_x = 0
        self.shake_y = 0

        self.dead = False

        fake_walls_layer = TileLayer(
            id_=1,
            name="Walls",
            size=Size(width=100, height=100),
            layer_data=generated_map["Walls"],
            offset=None,
            opacity=None,
            properties=None,
        )

        fake_floor_layer = TileLayer(
            id_=2,
            name="Floor",
            size=Size(width=100, height=100),
            layer_data=generated_map["Floor"],
            offset=None,
            opacity=None,
            properties=None,
        )

        fake_lighting_layer = TileLayer(
            id_=3,
            name="Lighting",
            size=Size(width=100, height=100),
            layer_data=generated_map["Lighting"],
            offset=None,
            opacity=None,
            properties=None,
        )

        if "Warps" in generated_map:
            fake_warps_layer = ObjectLayer(
                id_=4,
                name="Warps",
                tiled_objects=generated_map["Warps"],
                offset=None,
                opacity=None,
                properties=None,
            )
            self.warps_list = arcade.tilemap._process_object_layer(
                my_map, fake_warps_layer, scaling=SPRITE_SCALING_TILES, use_spatial_hash=True
            )

        self.doors_enabled = False

        if "Doors" in generated_map:
            fake_doors_layer = ObjectLayer(
                id_=5,
                name="Doors",
                tiled_objects=generated_map["Doors"],
                offset=None,
                opacity=None,
                properties=None,
            )
            self.doors_list = arcade.tilemap._process_object_layer(
                my_map, fake_doors_layer, scaling=SPRITE_SCALING_TILES, use_spatial_hash=True
            )

        self.wall_list = arcade.tilemap._process_tile_layer(
            my_map, fake_walls_layer, scaling=SPRITE_SCALING_TILES, use_spatial_hash=True
        )
        self.light_list = arcade.tilemap._process_tile_layer(
            my_map, fake_lighting_layer, scaling=SPRITE_SCALING_TILES, use_spatial_hash=True
        )
        self.floor_list = arcade.tilemap._process_tile_layer(
            my_map, fake_floor_layer, scaling=SPRITE_SCALING_TILES, use_spatial_hash=True
        )

        self.start_location = generated_map["start_location"][0].location

        # Create player sprite
        self.player_sprite = PlayerCharacter(convert_from_tiled_coordinates(my_map, generated_map["start_location"][0].location), self, self.scene_renderer)

        # Set player location
        i = random.randint(0, len(self.floor_list))
        start_pos = self.floor_list[i].position

        # Add to player sprite list
        self.player_list.append(self.player_sprite)

        # Game managers
        self.object_manager = ObjectManager(self, scene_renderer)
        self.enemy_manager = EnemyManager(self)
        self.enemy_manager.setup()
        self.projectile_manager = ProjectileManager(self)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_draw(self):
        # --- Manage Scrolling ---
        if math.fabs(self.player_sprite.center_x-self.view_left+(SCREEN_WIDTH/2)) > LERP_MARGIN*SCREEN_HEIGHT or math.fabs(self.player_sprite.center_y-self.view_bottom+(SCREEN_HEIGHT/2)) > LERP_MARGIN*SCREEN_HEIGHT:
            self.view_left = int(lerp(self.view_left,self.player_sprite.center_x-(SCREEN_WIDTH/2),CAMERA_SPEED))
            self.view_bottom = int(lerp(self.view_bottom,self.player_sprite.center_y-(SCREEN_HEIGHT/2),CAMERA_SPEED))

        self.wall_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.floor_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.light_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.warps_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        if self.doors_enabled:
            self.doors_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.bullet_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.player_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.object_manager.object_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.enemy_manager.enemy_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))

    def on_update(self, delta_time):

        x_force = self.player_sprite.x_force
        y_force = self.player_sprite.y_force
        self.player_sprite.on_update(delta_time)
        self.projectile_manager.projectile_physics.apply_impulse(self.player_sprite,
                                                                (x_force, y_force))
        self.enemy_manager.on_update(delta_time)

        # move projectiles
        self.projectile_manager.on_update(delta_time)

        # update animations
        self.player_sprite.update_animation(delta_time)
        self.object_manager.on_update(delta_time)

        if self.shake_remain > 0:
            self.shake_x = random.randrange(-self.shake_strength,self.shake_strength)
            self.shake_y = random.randrange(-self.shake_strength,self.shake_strength)
            self.shake_remain -= 1
        else:
            self.shake_x = 0
            self.shake_y = 0

        if self.dead:
            sys.exit(0)

        arcade.set_viewport(
            self.view_left+self.shake_x,
            (SCREEN_WIDTH) + self.view_left+self.shake_x,
            self.view_bottom+self.shake_y,
            (SCREEN_HEIGHT) + self.view_bottom+self.shake_y,
        )
