import arcade
import random

from Constants.Game import SPRITE_SCALING_PLAYER, SPRITE_SCALING_TILES, SPRITE_SIZE


class ObjectManager:
    """ Creates objects in the dungeon. """

    def __init__(self, game_resources):
        self.object_list = arcade.SpriteList()
        self.game_resources = game_resources


    def create_object(self):

        pos = random.choice( self.game_resources.floor_list).position


        player_x = round(self.game_resources.player_sprite.center_x)
        player_y = round(self.game_resources.player_sprite.center_y)

        x = random.randint(player_x - 500, player_x + 500)
        y = random.randint(player_y - 500, player_y + 500)

        grid_x = math.floor(x / SPRITE_IMAGE_SIZE)
        grid_y = math.floor(y / SPRITE_IMAGE_SIZE)

        floor_tiles = []

        for floor in self.game_resources.floor_list:
            if (
                floor.position[1] > grid_y - 500 or floor.position[1] < grid_y + 500
            ) and (
                floor.position[0] > grid_x - 500 or floor.position[0] < grid_x + 500
            ):
                floor_tiles.append(floor)
        if len(floor_tiles) == 0:
            return

        spawn_tile = random.choice(floor_tiles)

        self.enemy.position = spawn_tile.position

        # Add to enemy sprite list
        self.enemy_list.append(self.enemy)

    def flask(self, x, y):
        obj = arcade.Sprite('Graphics/items/flasks/flasks_1_1.png', scale=2, center_x=x, center_y=y)
        self.object_list.append(obj)
        return obj

    def candle(self, x, y):
        obj = arcade.Sprite('Graphics/items/torch/candlestick_1_1.png', scale=2, center_x=x, center_y=y)
        self.game_resources.light_list.append(obj)
        return obj