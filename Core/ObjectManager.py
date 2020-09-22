import arcade
import random

from Constants.Game import SPRITE_SCALING_PLAYER, SPRITE_SCALING_TILES, SPRITE_SIZE


class ObjectManager:
    """ Creates objects in the dungeon. """

    def __init__(self, game_resources):

        self.game_resources = game_resources
        for i in range(0, 10):
            self.create_object(random.randint(0, 10), random.randint(0, 10))

    def create_object(self, x, y):
        x = SPRITE_SIZE * x + SPRITE_SIZE / 2
        y = SPRITE_SIZE * y + SPRITE_SIZE / 2
        box = DestructableObject(
            center_x=x,
            center_y=y,
            filename="Graphics/items and trap_animation/box_2/box_2_3.png",
            scale=SPRITE_SCALING_TILES,
        )
        self.game_resources.object_list.append(box)


class DestructableObject(arcade.Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass
