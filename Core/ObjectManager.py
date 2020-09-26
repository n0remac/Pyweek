import arcade
import random

from Constants.Game import SPRITE_SCALING_PLAYER, SPRITE_SCALING_TILES, SPRITE_SIZE


class ObjectManager:
    """ Creates objects in the dungeon. """

    def __init__(self, game_resources):
        self.object_list = arcade.SpriteList()
        self.game_resources = game_resources

        #for floor in

    def flask(self, x, y):
        obj = arcade.Sprite('Graphics/items/flasks/flasks_1_1.png', scale=2, center_x=x, center_y=y)
        self.object_list.append(obj)

    def candle(self, x, y):
        obj = arcade.Sprite('Graphics/items/torch/candlestick_1_1.png', scale=2, center_x=x, center_y=y)
        self.game_resources.light_list.append(obj)

    def coin(self, x, y):
        obj = arcade.Sprite('Graphics/items/coin/coin_1.png', scale=2, center_x=x, center_y=y)
        self.game_resources.light_list.append(obj)