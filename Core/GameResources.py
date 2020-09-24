import math
import random

import arcade
from pytiled_parser.objects import TileLayer, Size

from Core.Enemy import Enemy, EnemyManager
from Constants.Game import (
    SPRITE_SCALING_TILES,
    SPRITE_SCALING_PLAYER,
    SPRITE_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    LEFT_VIEWPORT_MARGIN,
    RIGHT_VIEWPORT_MARGIN,
    BOTTOM_VIEWPORT_MARGIN,
    TOP_VIEWPORT_MARGIN,
)
from Core.LevelGenerator.generate_game_level import (
    generate_game_level,
    place_room,
    place_tunnel,
)
from Core.LevelGenerator.shapes import Rect
from Core.LevelGenerator.tiled_mapper.tiled_compatible_level import (
    generate_tiled_compatible_level,
)
from Core.PlayerCharacter import PlayerCharacter
from Core.Projectile_Manager import ProjectileManager


class GameResources:
    """
    Load arcade resources
    """

    def __init__(self):

        # Create the sprite lists
        self.sprite_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.object_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Read in the tiled map
        map_name = "Graphics/test_map.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)

        # Procedurally generated map
        generated_map = generate_game_level(100, 100)

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

        self.wall_list = arcade.tilemap._process_tile_layer(
            my_map, fake_walls_layer, scaling=SPRITE_SCALING_TILES
        )
        self.light_list = arcade.tilemap._process_tile_layer(
            my_map, fake_lighting_layer, scaling=SPRITE_SCALING_TILES
        )
        self.floor_list = arcade.tilemap._process_tile_layer(
            my_map, fake_floor_layer, scaling=SPRITE_SCALING_TILES
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

        # Create player sprite
        self.player_sprite = PlayerCharacter()

        # Set player location
        i = random.randint(0, len(self.floor_list))
        start_pos = self.floor_list[i].position
        grid_x = 20
        grid_y = 25
        self.player_sprite.position = start_pos
        # Add to player sprite list
        self.player_list.append(self.player_sprite)

        # Game managers
        self.projectile_manager = ProjectileManager(self)
        self.enemy_manager = EnemyManager(self)
        self.enemy_manager.setup()

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_draw(self):
        self.wall_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.floor_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.light_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.bullet_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.player_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.object_list.draw()
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

        self.wall_list.draw()
        self.floor_list.draw()
        self.light_list.draw()
        self.object_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        self.enemy_manager.enemy_list.draw()
        self.enemy_manager.enemy.draw()

    def on_update(self, delta_time):
        pass
