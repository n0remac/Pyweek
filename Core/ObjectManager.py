import arcade

from Core.Character import Character

class ObjectManager:
    """ Creates objects in the dungeon. """

    def __init__(self, game_resources):
        self.object_list = arcade.SpriteList()
        self.game_resources = game_resources



        #for floor in

    def flask(self, x, y):
        obj = Item((x, y), 'Graphics/items/flasks/flasks_1')
        self.object_list.append(obj)

    def candle(self, x, y):
        obj = Item((x, y), 'Graphics/items/torch/candlestick_1')
        self.object_list.append(obj)

    def coin(self, x, y):
        obj = Item((x, y), 'Graphics/items/coin/coin')
        self.object_list.append(obj)

    def on_update(self, delta_time):
        for obj in self.object_list:
            obj.update_animation(delta_time)

class Item(Character):
    def __init__(self, position, main_path):
        super().__init__(position)
        self.main_path = main_path
        self.load_textures()