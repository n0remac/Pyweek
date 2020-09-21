import arcade
import math

from Constants.Physics import PLAYER_MOVEMENT_SPEED, BULLET_MOVE_FORCE
from Core.GameResources import GameResources
from Core.RendererFactory import RendererFactory
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

        # Physics engines
        self.physics_engine = setup_physics_engine(self.game_resources)
        self.projectile_physics = arcade.PymunkPhysicsEngine()

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
            59.0 / 255.0,
            122.0 / 255.0,
            87.0 / 255.0,
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

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        bullet = arcade.SpriteSolidColor(20, 5, arcade.color.DARK_YELLOW)
        self.game_resources.bullet_list.append(bullet)

        # Position the bullet at the player's current location
        start_x = self.game_resources.player_sprite.center_x
        start_y = self.game_resources.player_sprite.center_y
        bullet.position = self.game_resources.player_sprite.position

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # What is the 1/2 size of this sprite, so we can figure out how far
        # away to spawn the bullet
        size = (
            max(
                self.game_resources.player_sprite.width,
                self.game_resources.player_sprite.height,
            )
            / 2
        )

        # Use angle to to spawn bullet away from player in proper direction
        bullet.center_x += size * math.cos(angle)
        bullet.center_y += size * math.sin(angle)

        # Set angle of bullet
        bullet.angle = math.degrees(angle)

        # Add the sprite. This needs to be done AFTER setting the fields above.
        self.projectile_physics.add_sprite(bullet, collision_type="bullet")

        # Add force to bullet
        force = (BULLET_MOVE_FORCE, 0)
        self.projectile_physics.apply_force(bullet, force)

    # This method should idealy do nothing but invoke the scene renderer. use the following drawing methods instead
    def on_draw(self):
        self.scene_renderer.draw_scene()

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

        # Move the player with the physics engine
        self.physics_engine.update()
        self.projectile_physics.step()

        # move the player light to the player
        self.player_light.position = (
            self.game_resources.player_sprite.center_x,
            self.game_resources.player_sprite.center_y,
        )

        # self.physics_engine.step()
        # self.game_resources.on_update(delta_time)
