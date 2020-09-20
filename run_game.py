import arcade

from Constants.Game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from Core.GameInstance import GameInstance

from Graphics.SceneRenderer import SceheRenderer

from Graphics.PostProcessing.Tonemap import Tonemap

class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        super().__init__(width, height, title)
        self.game_instance: Optional[GameInstance] = None

    def setup(self):
        """ Set up everything with the game """

        window_size = self.get_size()
        self.game_instance = GameInstance()

        self.test_sprite = arcade.Sprite('Graphics/test_image.png')
        self.test_sprite.center_x = 100
        self.test_sprite.center_y = 300
        self.test_list = arcade.SpriteList()
        self.test_list.append(self.test_sprite)

        self.scene_renderer = SceheRenderer(self, self.get_size())
        #bind rendering callbacks
        self.scene_renderer.draw_primary_callback = self.on_draw_scene
        self.scene_renderer.draw_emissive_callback = self.on_draw_emissive
        self.scene_renderer.draw_after_post_callback = self.on_draw_after_post

        self.scene_renderer.background_color = (0.5,0.5,0.5,1.0)
        self.scene_renderer.light_renderer.ambient_light = (1.0, 0.6, 0.3)

        self.light = self.scene_renderer.light_renderer.create_point_light(
            (400,400),
            (1.0,1.0,1.0),
            128.0)

        self.tonemap = Tonemap()
        self.scene_renderer.post_processing.add_effect(self.tonemap)

        self.tonemap.white_point = 2.0

    def on_draw(self):
        #draw the game
        self.scene_renderer.draw_scene()

    def on_draw_scene(self):
        self.test_list.draw()
        pass

    def on_draw_emissive(self):
        pass

    def on_draw_after_post(self):
        pass


def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()