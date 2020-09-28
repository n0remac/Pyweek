import arcade

from Core.Character import Character

class ObjectManager:
    """ Creates objects in the dungeon. """

    def __init__(self, game_resources, scene_renderer):
        self.object_list = arcade.SpriteList()
        self.game_resources = game_resources
        self.scene_renderer = scene_renderer

    def flask(self, x, y):
        obj = Item((x, y), 'Graphics/items/flasks/flasks_1', 'flask')
        self.object_list.append(obj)

    def candle_drop(self, x, y):
        obj = Item((x, y), 'Graphics/items/torch/candle_drop','candle_drop')
        self.object_list.append(obj)

    def candle(self, x, y):
        obj = Item((x, y), 'Graphics/items/torch/candlestick_1', 'candle')
        self.object_list.append(obj)
        self.game_resources.torch_particle_system.add_candle((x,y))
        self.scene_renderer.scene_renderer.light_renderer.create_point_light(
                    (x,y),  # Position
                    (
                        2.5,
                        1.25,
                        0.5,
                    ),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB This can go over 1.0 because of HDR
                    250.0,
                )  # Radius

    def coin(self, x, y):
        obj = Item((x, y), 'Graphics/items/coin/coin', 'coin')
        self.object_list.append(obj)

    def on_update(self, delta_time):
        for obj in self.object_list:
            obj.update_animation(delta_time)

class Item(Character):
    def __init__(self, position, main_path, kind):
        super().__init__(position)
        self.main_path = main_path
        self.load_textures()
        self.kind = kind