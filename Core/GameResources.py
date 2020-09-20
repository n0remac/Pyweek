import arcade

from Constants.Game import SPRITE_SCALING_TILES, SPRITE_SCALING_PLAYER, SPRITE_SIZE

class GameResources:
    """
    Load arcade resources
    """

    def __init__(self):

        # Read in the tiled map
        map_name = "Graphics/test_map.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)
        self.wall_list = arcade.tilemap.process_layer(
            my_map, "Walls", SPRITE_SCALING_TILES
        )

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_draw(self):
        self.wall_list.draw()
