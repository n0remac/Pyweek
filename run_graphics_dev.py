import arcade

from Constants.Game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from Core.GameInstance import GameInstance
from Core.RendererFactory import RendererFactory

from Graphics.SceneRenderer import SceneRenderer

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

        self.test_sprite = arcade.Sprite("Graphics/test_image.png")
        self.test_sprite.center_x = 100
        self.test_sprite.center_y = 300
        self.test_list = arcade.SpriteList()
        self.test_list.append(self.test_sprite)

        self.scene_renderer = RendererFactory.create_renderer(self)

        # bind rendering callbacks
        self.scene_renderer.draw_primary_callback = self.on_draw_scene
        self.scene_renderer.draw_emissive_callback = self.on_draw_emissive
        self.scene_renderer.draw_after_post_callback = self.on_draw_after_post

        self.light = self.scene_renderer.light_renderer.create_point_light(
            (400, 400),  # Position
            (1.0, 1.0, 1.0),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB
            128.0,
        )  # Radius

        self.lightb = self.scene_renderer.light_renderer.create_point_light(
            (300, 300),  # Position
            (0.0, 1.0, 1.0),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB
            96.0,
        )  # Radius

        # self.light.destroy()

    def on_draw(self):
        # draw the game
        self.scene_renderer.draw_scene()

    # This method should be used to draw everything efected by lighting and post-processing
    def on_draw_scene(self):
        self.test_list.draw()
        pass

    # Everything drawn in here will be drawn with blend mode:Additive. Use for glowing stuff that ignores lighting
    def on_draw_emissive(self):
        pass

    # Drawn after all post processing, for things like UI
    def on_draw_after_post(self):
        pass


def main():
    """ Main method """
    window = GameWindow(1280, 1024, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
