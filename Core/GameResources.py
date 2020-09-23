from random import random

import arcade
from pytiled_parser.objects import TileLayer, Size

from Constants.Game import SPRITE_SCALING_TILES, SPRITE_SCALING_PLAYER, SPRITE_SIZE, SCREEN_WIDTH
from Core.LevelGenerator.generate_game_level import generate_game_level


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

        # Read in the tiled map
        map_name = "Graphics/test_map.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)

        generated_map = generate_game_level(100, 100)

        fake_walls_layer = TileLayer(
            id_=1,
            name="Walls",
            size=Size(width=100, height=100),
            layer_data=generated_map["Walls"],
            offset=None,
            opacity=None,
            properties=None
        )

        fake_floor_layer = TileLayer(
            id_=2,
            name="Floor",
            size=Size(width=100, height=100),
            layer_data=generated_map["Floor"],
            offset=None,
            opacity=None,
            properties=None
        )

        fake_lighting_layer = TileLayer(
            id_=3,
            name="Lighting",
            size=Size(width=100, height=100),
            layer_data=generated_map["Lighting"],
            offset=None,
            opacity=None,
            properties=None
        )

        self.wall_list = arcade.tilemap._process_tile_layer(
            my_map,
            fake_walls_layer,
            scaling=SPRITE_SCALING_TILES
        )
        self.light_list = arcade.tilemap._process_tile_layer(
            my_map,
            fake_lighting_layer,
            scaling=SPRITE_SCALING_TILES
        )
        self.floor_list = arcade.tilemap._process_tile_layer(
            my_map,
            fake_floor_layer,
            scaling=SPRITE_SCALING_TILES
        )
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
        self.player_sprite = arcade.Sprite(
            "Graphics/player.png", SPRITE_SCALING_PLAYER,
        )

        # Set player location
        grid_x = 20
        grid_y = 25
        self.player_sprite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2
        # Add to player sprite list
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        # arcade.set_viewport(self.player_sprite.center_x - (SPRITE_SIZE * (SCREEN_WIDTH / 16)))
        self.wall_list.draw()
        self.floor_list.draw()
        self.light_list.draw()
        self.object_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
