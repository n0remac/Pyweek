import arcade
import math

from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Core.GameResources import GameResources
from Core.RendererFactory import RendererFactory
from Core.ObjectManager import ObjectManager
from Physics.EnemyPhysicsEngine import setup_enemy_physics_engine
from Core.HealthRing import Health
from Physics.PhysicsEngine import setup_physics_engine
from Graphics.Particles.Torch.TorchSystem import TorchSystem


class GameInstance:
    """
    This is an instance of the game and all of the different components needed to render it.
    """

    def __init__(self, window):

        # Refernce to main window object
        self.window = window

        # Core game resources
        self.game_resources = GameResources()

        # Physics engine
        self.physics_engine = setup_physics_engine(self.game_resources)
        # Enemy Physics engine
        self.enemy_physics_engine = setup_enemy_physics_engine(self.game_resources)

        self.horizontal_key_list = []
        self.verticle_key_list = []

        # create default scene renderer via factory.
        # This configures the post processing stack and default lighting
        self.scene_renderer = RendererFactory.create_renderer(window)

        # bind rendering callbacks
        self.scene_renderer.draw_primary_callback = self.on_draw_scene
        self.scene_renderer.draw_emissive_callback = self.on_draw_emissive
        self.scene_renderer.draw_after_post_callback = self.on_draw_after_post

        # Set background color
        # Based on old arcade.AMAZON color
        # (59, 122, 87)
        self.scene_renderer.background_color = (
            37.0 / 255.0,
            19.0 / 255.0,
            26.0 / 255.0,
            1.0,
        )

        # dim the ambient lighting to make the player's light more vibrant
        self.scene_renderer.light_renderer.ambient_light = (0.25, 0.25, 0.25)

        # create light sources
        self.light_list = []

        self.player_light = self.scene_renderer.light_renderer.create_point_light(
            (400, 400),  # Position
            (
                1.75,
                1.75,
                1.75,
            ),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB This can go over 1.0 because of HDR
            160.0,
        )  # Radius

        # player heath system
        self.player_health = Health(
            self.player_light, self.scene_renderer.post_processing
        )

        # torch particle system
        self.torch_particle_system = TorchSystem(window.ctx)

        # dict used to determine radius of light based on light_type
        radius_by_type = {"torch": 70.0, "candle": 40.0}

        for light in self.game_resources.light_list:
            radius = radius_by_type.get(light.properties["type"])
            self.light_list.append(
                self.scene_renderer.light_renderer.create_point_light(
                    (light.center_x, light.center_y),  # Position
                    (
                        1.75,
                        2.75,
                        1.75,
                    ),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB This can go over 1.0 because of HDR
                    radius,
                )  # Radius
            )

            if light.properties["type"] == "torch":
                self.torch_particle_system.add_torch((light.center_x, light.center_y))
            else:
                self.torch_particle_system.add_candle((light.center_x, light.center_y))

        # TODO: This code will crash if there are zero lights loaded. Please fix!
        self.torch_particle_system.build_buffer()

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
        elif key == arcade.key.P:
            self.player_health.health += 10.0
        elif key == arcade.key.O:
            self.player_health.health -= 10.0

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
        self.game_resources.projectile_manager.on_mouse_press(x, y, button, modifiers)

    # This method should idealy do nothing but invoke the scene renderer. use the following drawing methods instead
    def on_draw(self):
        self.scene_renderer.draw_scene()

    # This method should be used to draw everything efected by lighting and post-processing
    def on_draw_scene(self):
        self.game_resources.on_draw()

    # Everything drawn in here will be drawn with blend mode:Additive. Use for glowing stuff that ignores lighting
    def on_draw_emissive(self):
        self.torch_particle_system.render(self.window.ctx.projection_2d_matrix)
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

        # Makes enemy collide with walls
        self.enemy_physics_engine.update()

        self.path = arcade.astar_calculate_path(
            self.game_resources.enemy.position,
            self.game_resources.player_sprite.position,
            self.game_resources.barrier_list,
            diagonal_movement=False,
        )
        self.game_resources.enemy.on_update(
            self.path, self.game_resources.player_sprite.position
        )

        # move projectiles
        self.game_resources.projectile_manager.on_update(delta_time)

        # move the player light to the player
        self.player_light.position = (
            self.game_resources.player_sprite.center_x,
            self.game_resources.player_sprite.center_y,
        )
