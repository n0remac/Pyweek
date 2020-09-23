import arcade

from Constants.Game import SPRITE_SCALING_TILES, SPRITE_SCALING_PLAYER, SPRITE_SIZE
from Core.PlayerCharacter import PlayerCharacter


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
        self.wall_list = arcade.tilemap.process_layer(
            my_map, "Walls", SPRITE_SCALING_TILES
        )
        self.floor_list = arcade.tilemap.process_layer(
            my_map, "Floor", SPRITE_SCALING_TILES
        )
        self.light_list = arcade.tilemap.process_layer(
            my_map, "Lighting", SPRITE_SCALING_TILES
        )

        # Create player sprite
        self.player_sprite = PlayerCharacter()

        # Set player location
        grid_x = 10
        grid_y = 5
        self.player_sprite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2
        # Add to player sprite list
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        self.wall_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.floor_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.light_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.bullet_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.player_list.draw(filter=(arcade.gl.NEAREST, arcade.gl.NEAREST))
        self.object_list.draw()
