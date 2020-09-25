import arcade
import math

from Constants.Game import SCREEN_HEIGHT, SCREEN_WIDTH
from Constants.Physics import BULLET_MOVE_FORCE
from Graphics.Lights.PointLight import DynamicPointLight


class ProjectileManager:
    """ Handles mouse press presses to fire bullets and creates bullet objects. """

    def __init__(self, game_resources):

        self.game_resources = game_resources

        #used for test stuff
        self.last_type = 0

        self.projectile_physics = arcade.PymunkPhysicsEngine()
        self.projectile_physics.add_sprite_list(
            self.game_resources.wall_list,
            collision_type="wall",
            body_type=arcade.PymunkPhysicsEngine.STATIC,
        )

        self.projectile_physics.add_sprite_list(
            self.game_resources.object_list,
            collision_type="object",
            body_type=arcade.PymunkPhysicsEngine.STATIC,
        )

        def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            bullet_sprite.remove_from_sprite_lists()

            if self.on_bullet_death is not None:
                self.on_bullet_death(bullet_sprite)

        self.projectile_physics.add_collision_handler(
            "bullet", "wall", post_handler=wall_hit_handler
        )

        def object_hit_handler(bullet_sprite, _object_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """

            if self.on_bullet_death is not None:
                self.on_bullet_death(bullet_sprite)

            bullet_sprite.remove_from_sprite_lists()
            _object_sprite.remove_from_sprite_lists()

        self.projectile_physics.add_collision_handler(
            "bullet", "object", post_handler=object_hit_handler
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        bullet = BulletSprite(self.game_resources, 20, 5, arcade.color.DARK_YELLOW)
        self.game_resources.bullet_list.append(bullet)

        # Position the bullet at the player's current location
        start_x = self.game_resources.player_sprite.center_x
        start_y = self.game_resources.player_sprite.center_y
        bullet.position = self.game_resources.player_sprite.position
        bullet.art_type = self.last_type
        self.last_type += 1
        if(self.last_type >= 3):
            self.last_type = 0

        #TODO:Color based on light
        # add light to sprite
        bullet.point_light = DynamicPointLight((1.5, 1.0, 0.2), 128.0)

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x + self.game_resources.view_left
        dest_y = y + self.game_resources.view_bottom

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

    def on_update(self, delta_time):
        self.projectile_physics.step()


class BulletSprite(arcade.SpriteSolidColor):
    """ Bullet Sprite """

    def __init__(self, game_resources, *args):
        super().__init__(*args)
        self.game_resources = game_resources

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        if (
            self.bottom < self.game_resources.view_bottom
            or self.top > self.game_resources.view_bottom + SCREEN_HEIGHT
            or self.right > self.game_resources.view_left + SCREEN_WIDTH
            or self.left < self.game_resources.view_left
        ):
            self.remove_from_sprite_lists()
