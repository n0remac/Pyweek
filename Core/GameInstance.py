import arcade
import math
import ctypes
import platform
import subprocess

from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Constants.Game import SCREEN_WIDTH, SCREEN_HEIGHT
from Core.GameResources import GameResources
from Core.ObjectManager import ObjectManager
from Core.RendererFactory import RendererFactory
from Core.HealthRing import Health
from Physics.EnemyPhysicsEngine import setup_enemy_physics_engine
from Physics.PhysicsEngine import setup_physics_engine
from Graphics.Particles.Torch.TorchSystem import TorchSystem
from Graphics.Particles.Fireball.Fireball import FireBall


class GameInstance:
    """
    This is an instance of the game and all of the different components needed to render it.
    """

    def __init__(self, window):

        # Reference to main window object
        self.window = window

        # Core game resources
        self.game_resources = GameResources(self)
        self.object_manager = ObjectManager(self.game_resources, self)

        self.screensize = 1920,1080

        # Fullscreen information get based on OS
        if platform.system() == 'Linux':
            print("This game expects linux users to be using a 1080p, 16:9 monitor.  Other aspect ratios or resolutions on linux may cause issues.")
            """
            cmd = ['xrandr']
            cmd2 = ['grep', '*']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
            p.stdout.close()
            resolution_string, junk = p2.communicate()
            resolution = resolution_string.split()[0]
            width, height = resolution.split('x')
            self.screensize[0] = width
            self.screensize[1] = height
            """
        elif platform.system() == 'Windows':
            user32 = ctypes.windll.user32
            self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        # Physics engine
        self.physics_engine = setup_physics_engine(self.game_resources)

        self.horizontal_key_list = []
        self.verticle_key_list = []


        # create default scene renderer via factory.
        # This configures the post processing stack and default lighting
        self.scene_renderer = RendererFactory.create_renderer(window)

        # bind rendering callbacks
        self.scene_renderer.draw_primary_callback = self.on_draw_scene
        self.scene_renderer.draw_emissive_callback = self.on_draw_emissive
        self.scene_renderer.draw_after_post_callback = self.on_draw_after_post
        self.scene_renderer.draw_to_light_bufer_callback = self.on_draw_light_buffer

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
        #self.scene_renderer.light_renderer.ambient_light = (0.01, 0.01, 0.01)

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
        self.game_resources.torch_particle_system = self.torch_particle_system

        # TODO:MOVE THIS STUFF
        self.fireball_system = FireBall(
            window.ctx, self.game_resources.projectile_manager.projectile_physics
        )

        self.game_resources.projectile_manager.on_bullet_death = (
            self.fireball_system.on_particle_death
        )

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

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        self.game_resources.player_sprite.on_key_press(key, modifiers)
        if key == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)
            if self.window.fullscreen:
                if SCREEN_WIDTH > SCREEN_HEIGHT:
                    self.window.screensize_multiplier = self.screensize[0]/SCREEN_WIDTH
                else:
                    self.window.screensize_multiplier = self.screensize[1]/SCREEN_HEIGHT
            else:
                self.window.set_size(self.window.original_size[0],self.window.original_size[1])
                self.window.screensize_multiplier = 1

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        self.game_resources.player_sprite.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.game_resources.player_sprite.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.game_resources.projectile_manager.on_mouse_press(x, y, button, modifiers)

    # This method should idealy do nothing but invoke the scene renderer. use the following drawing methods instead
    def on_draw(self):

        # Update particle lights, needs to happen once per frame
        self.scene_renderer.light_renderer.draw_dynamic_point_lights(
            self.game_resources.bullet_list
        )

        self.scene_renderer.draw_scene()

    # This method should be used to draw everything efected by lighting and post-processing
    def on_draw_scene(self):
        self.game_resources.on_draw()

    # Everything drawn in here will be drawn with blend mode:Additive. Use for glowing stuff that ignores lighting
    def on_draw_emissive(self):
        self.torch_particle_system.render(self.window.ctx.projection_2d_matrix)
        self.fireball_system.render(
            self.window.ctx.projection_2d_matrix, self.game_resources.bullet_list
        )
        pass

    def on_draw_light_buffer(self):
        self.fireball_system.render_lights(
            self.window.ctx.projection_2d_matrix, self.game_resources.bullet_list
        )

    # Drawn after all post processing, for things like UI
    def on_draw_after_post(self):
        pass

    def on_update(self, delta_time):
        """ Movement and game logic """

        x_force = self.game_resources.player_sprite.x_force
        y_force = self.game_resources.player_sprite.y_force
        self.game_resources.player_sprite.on_update(delta_time)
        self.game_resources.projectile_manager.projectile_physics.apply_impulse(self.game_resources.player_sprite, (x_force, y_force))

        # Move the player with the physics engine
        # self.physics_engine.update()

        self.game_resources.enemy_manager.on_update(delta_time)

        # move projectiles
        self.game_resources.projectile_manager.on_update(delta_time)

        # move the player light to the player
        self.player_light.position = (
            self.game_resources.player_sprite.center_x,
            self.game_resources.player_sprite.center_y,
        )
        # update animations
        self.game_resources.player_sprite.update_animation(delta_time)
        self.game_resources.object_manager.on_update(delta_time)
        self.game_resources.on_update(delta_time)
