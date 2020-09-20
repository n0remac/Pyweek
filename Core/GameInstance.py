import arcade

from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Core.GameResources import GameResources
from Physics.PhysicsEngine import setup_physics_engine


class GameInstance:
    """
    This is an instance of the game and all of the different components needed to render it.
    """

    def __init__(self):

        # Core game resources
        self.game_resources = GameResources()

        # Physics engine
        self.physics_engine = setup_physics_engine(self.game_resources)

        # Set background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.game_resources.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.game_resources.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.game_resources.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.game_resources.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.game_resources.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.game_resources.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.game_resources.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.game_resources.player_sprite.change_x = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self.game_resources.on_mouse_motion(x, y, dx, dy)

    def on_draw(self):
        self.game_resources.on_draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        # self.physics_engine.step()
        # self.game_resources.on_update(delta_time)
