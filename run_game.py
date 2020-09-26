#!/bin/python3

import sys

# The major, minor version numbers your require
MIN_VER = (3, 7)

if sys.version_info[:2] < MIN_VER:
    sys.exit(
        "This game requires Python {}.{}.".format(*MIN_VER)
    )

import arcade

from Constants.Game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from Core.GameInstance import GameInstance

class TitleScreen(arcade.View):
    # Title Screen view
    def __init__(self):
        """ Create the variables """
        super().__init__()
        self.background = None
        self.selected = 0

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        if self.selected == 0:
            self.background = arcade.load_texture("Graphics/title-screen-play.png")
        else:
            self.background = arcade.load_texture("Graphics/title-screen-quit.png")
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            if self.selected == 0:
                self.selected = 1
            else:
                self.selected = 0


class GameView(arcade.View):
    """ Main Window """

    def __init__(self):
        """ Create the variables """
        super().__init__()
        self.game_instance: Optional[GameInstance] = None

    def setup(self):
        """ Set up everything with the game """
        self.game_instance = GameInstance(self.window)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        self.game_instance.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        self.game_instance.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.game_instance.on_mouse_motion(x, y, dx, dy)
        self.game_instance.game_resources.player_sprite.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.game_instance.on_mouse_press(x, y, button, modifiers)

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.game_instance.on_update(delta_time)

    def on_draw(self):
        """ Draw everything """
        self.game_instance.on_draw()


def main():
    """ Main method """
    #window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    #window.setup()
    game_window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    title_screen = TitleScreen()
    game_window.show_view(title_screen)
    arcade.run()


if __name__ == "__main__":
    main()
