import arcade

from Core.GameResources import GameResources

class GameInstance:
    """
    This is an instance of the game and all of the different components needed to render it.
    """
    def __init__(self):

        # Core game resources
        self.game_resources = GameResources()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.LEFT:
                self.left_pressed = True
        elif key == arcade.key.RIGHT:
                self.right_pressed = True
        elif key == arcade.key.UP:
                self.up_pressed = True
        elif key == arcade.key.DOWN:
                self.down_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.LEFT:
                self.left_pressed = False
        elif key == arcade.key.RIGHT:
                self.right_pressed = False
        elif key == arcade.key.UP:
                self.up_pressed = False
        elif key == arcade.key.DOWN:
                self.down_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.game_resources.on_mouse_motion(x, y, dx, dy)

    def on_draw(self):
        self.game_resources.on_draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        pass