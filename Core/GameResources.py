import random
import sys

import arcade
from pytiled_parser.objects import TileLayer, Size, ObjectLayer

from Core.Enemy import EnemyManager
from Constants.Game import (
    SPRITE_SCALING_TILES,
    SPRITE_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    LEFT_VIEWPORT_MARGIN,
    RIGHT_VIEWPORT_MARGIN,
    BOTTOM_VIEWPORT_MARGIN,
    TOP_VIEWPORT_MARGIN,
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

    def __init__(self, game_instance):

        self.game_instance = game_instance
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

        self.dead = False

        # Static map for testing
        # generated_map = generate_tiled_compatible_level(70, 70)
        # place_room(Rect(1, 1, 5, 5), generated_map)
        # place_room(Rect(10, 1, 10, 10), generated_map)
        # place_room(Rect(1, 10, 8, 8), generated_map)
        # place_tunnel(Rect(6, 3, 5, 1), generated_map)
        # place_tunnel(Rect(3, 6, 1, 5), generated_map)

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

        # Uncomment if you want to actually load the level from the Tiled map.
        # self.wall_list = arcade.tilemap.process_layer(
        #     my_map, "Walls", SPRITE_SCALING_TILES
        # )
        # self.floor_list = arcade.tilemap.process_layer(
        #     my_map, "Floor", SPRITE_SCALING_TILES
        # )
        # self.light_list = arcade.tilemap.process_layer(
        #     my_map, "Lighting", SPRITE_SCALING_TILES
        # )

        self.start_location = generated_map["start_location"][0].location

        # Create player sprite
        self.player_sprite = PlayerCharacter(convert_from_tiled_coordinates(my_map, generated_map["start_location"][0].location), self, game_instance.scene_renderer)

        # Set player location
        i = random.randint(0, len(self.floor_list))
        start_pos = self.floor_list[i].position

        # Add to player sprite list
        self.player_list.append(self.player_sprite)

        # Game managers
        self.object_manager = ObjectManager(self, game_instance)
        self.enemy_manager = EnemyManager(self)
        self.enemy_manager.setup()
        self.projectile_manager = ProjectileManager(self)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_draw(self):

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(
                self.view_left,
                SCREEN_WIDTH + self.view_left,
                self.view_bottom,
                SCREEN_HEIGHT + self.view_bottom,
            )
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
        if self.dead:
            sys.exit(0)

