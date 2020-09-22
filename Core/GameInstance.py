import arcade
import math

from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Core.GameResources import GameResources
from Core.LightManager import LightManager
from Core.ObjectManager import ObjectManager
from Core.ProjectileManager import ProjectileManager
from Physics.PhysicsEngine import setup_physics_engine


class GameInstance:
    """
    This is an instance of the game and all of the different components needed to render it.
    """

    def __init__(self, window):

        # Refernce to main window object
        self.window = window

        # Core game resources
        self.game_resources = GameResources()

        # Managers
        self.object_manager = ObjectManager(self.game_resources)
        self.projectile_manager = ProjectileManager(self.game_resources)
        self.light_manager = LightManager(self.game_resources, window)

        # Physics engine
        self.physics_engine = setup_physics_engine(self.game_resources)

        self.horizontal_key_list = []
        self.verticle_key_list = []

        

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.verticle_key_list.insert(0, PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.verticle_key_list.insert(0, -PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.horizontal_key_list.insert(0, -PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.horizontal_key_list.insert(0, PLAYER_MOVEMENT_SPEED)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.game_resources.player_sprite.change_y = 0
            if len(self.verticle_key_list) > 0:
                self.verticle_key_list.remove(PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.game_resources.player_sprite.change_y = 0
            if len(self.verticle_key_list) > 0:
                self.verticle_key_list.remove(-PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.game_resources.player_sprite.change_x = 0
            if len(self.horizontal_key_list) > 0:
                self.horizontal_key_list.remove(-PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.game_resources.player_sprite.change_x = 0
            if len(self.horizontal_key_list) > 0:
                self.horizontal_key_list.remove(PLAYER_MOVEMENT_SPEED)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        self.projectile_manager.on_mouse_press(x, y, button, modifiers)

    # This method should idealy do nothing but invoke the scene renderer from light_manager. use the following drawing methods instead
    def on_draw(self):
        self.light_manager.on_draw()

    # This method should be used to draw everything efected by lighting and post-processing
    def on_draw_scene(self):
        self.game_resources.on_draw()

    # Everything drawn in here will be drawn with blend mode:Additive. Use for glowing stuff that ignores lighting
    def on_draw_emissive(self):
        pass

    # Drawn after all post processing, for things like UI
    def on_draw_after_post(self):
        pass

    def on_update(self, delta_time):
        """ Movement and game logic """
        if len(self.horizontal_key_list) > 0:
            self.game_resources.player_sprite.change_x = self.horizontal_key_list[0]
        if len(self.verticle_key_list) > 0:
            self.game_resources.player_sprite.change_y = self.verticle_key_list[0]

        # Move the player with the physics engine
        self.physics_engine.update()

        # move projectiles
        self.projectile_manager.on_update(delta_time)

        # move light sources
        self.light_manager.on_update(delta_time)
