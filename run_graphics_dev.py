import arcade
import time
from Constants.Game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from Core.GameInstance import GameInstance
from Core.RendererFactory import RendererFactory

from Graphics.SceneRenderer import SceneRenderer

from Graphics.PostProcessing.Tonemap import Tonemap
from Graphics.Particles.TestParticleSystem import TestParticleSystem
from Core.Async import Async

class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        super().__init__(width, height, title)
        self.game_instance: Optional[GameInstance] = None

    def setup(self):
        """ Set up everything with the game """

        window_size = self.get_size()

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

        self.scene_renderer.light_renderer.ambient_light = (0.1, 0.1, 0.1)
        '''
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
        '''
        self.stoplight = self.scene_renderer.light_renderer.create_point_light(
            (300, 500),  # Position
            (1.0, 1.0, 1.0),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB
            256.0 )  # Radius        

        self.animated_light = self.scene_renderer.light_renderer.create_point_light(
            (800, 500),  # Position
            (1.0, 1.0, 1.0),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB
            256.0 )  # Radius        

        def stoplight(light):
            while True:
                light.color = (0.0, 2.0, 0.0)#Greater than 1 because HDR
                yield 3.0 #run again in 3 seconds
                
                light.color = (1.5, 1.5, 0.0)
                yield 0.75

                light.color = (2.0, 0.0, 0.0)
                yield 3.0

        def animated_light(light):
            while True:
                value = 0.0
                while value < 2.0:
                    light.color = (value ,value, value)
                    value += 0.05
                    yield 0.0 #run next possible frame

                while value > 0.0:
                    light.color = (value , value, value)
                    value -= 0.05                    
                    yield 0.0
          
        Async.run(stoplight(self.stoplight))
        Async.run(animated_light(self.animated_light))


        self.particles = TestParticleSystem(self.ctx)

        # self.light.destroy()

        self.start_time = time.time()
        self.current_time = 0.0

    def on_draw(self):
        self.current_time = time.time() - self.start_time

        # draw the game
        self.scene_renderer.draw_scene()

    # This method should be used to draw everything efected by lighting and post-processing
    def on_draw_scene(self):
        #self.test_list.draw()
        Async.update()

        pass

    # Everything drawn in here will be drawn with blend mode:Additive. Use for glowing stuff that ignores lighting
    def on_draw_emissive(self):
        self.particles.render(self.ctx.projection_2d_matrix)
        pass

    # Drawn after all post processing, for things like UI
    def on_draw_after_post(self):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        self.particles.do_burst((x, y))


def main():
    """ Main method """
    window = GameWindow(1280, 1024, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
