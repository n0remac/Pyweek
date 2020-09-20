import arcade

from Constants.Physics import PLAYER_MOVE_FORCE_ON_GROUND
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

        # Track the current state of what key is pressed
        # TODO: Figure out where we want to store state variables.
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False

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

        # Update player forces based on keys pressed
        if self.left_pressed and not self.right_pressed:
            # Create a force to the left. Apply it.
            force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.physics_engine.apply_force(self.game_resources.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.game_resources.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            # Create a force to the right. Apply it.
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.physics_engine.apply_force(self.game_resources.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.game_resources.player_sprite, 0)
        elif self.up_pressed and not self.down_pressed:
            # Create a force to the right. Apply it.
            force = (0, PLAYER_MOVE_FORCE_ON_GROUND)
            self.physics_engine.apply_force(self.game_resources.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.game_resources.player_sprite, 0)
        elif self.down_pressed and not self.up_pressed:
            # Create a force to the right. Apply it.
            force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
            self.physics_engine.apply_force(self.game_resources.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.game_resources.player_sprite, 0)
        else:
            # Player's feet are not moving. Therefore up the friction so we stop.
            self.physics_engine.set_friction(self.game_resources.player_sprite, 1.0)

        self.physics_engine.step()
        self.game_resources.on_update(delta_time)
