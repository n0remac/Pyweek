import arcade

from Constants.Game import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from Core.GameInstance import GameInstance


class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        super().__init__(width, height, title)

        self.game_instance: Optional[GameInstance] = None

        # Tracking key presses
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False

    def setup(self):
        """ Set up everything with the game """

        window_size = self.get_size()
        self.game_instance = GameInstance(self)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        self.game_instance.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        self.game_instance.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.game_instance.on_mouse_motion(x, y, dx, dy)

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.game_instance.on_update(delta_time)

    def on_draw(self):
        """ Draw everything """
        self.game_instance.on_draw()


def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
