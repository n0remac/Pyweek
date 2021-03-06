import random
import sys
from typing import TYPE_CHECKING

import arcade
import math
import random

from arcade import Sprite

from Constants.Game import SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_IMAGE_SIZE
from Constants.Physics import BULLET_MOVE_FORCE
from Core.ArcadeUtils import convert_from_tiled_coordinates
from Graphics.Lights.PointLight import DynamicPointLight
from Sounds.SoundPool import SoundPool

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
            friction=1.0,
            body_type=arcade.PymunkPhysicsEngine.STATIC,
        )

        self.projectile_physics.add_sprite_list(
            self.game_resources.object_manager.object_list,
            collision_type="object",
            body_type=arcade.PymunkPhysicsEngine.STATIC,
        )

        self.projectile_physics.add_sprite(
            self.game_resources.player_sprite,
            damping=0.0001,
            friction=10.0,
            mass=2.0,
            moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=1200,
            max_vertical_velocity=1200,
            body_type=arcade.PymunkPhysicsEngine.DYNAMIC
        )

        self.projectile_physics.add_sprite_list(
            self.game_resources.warps_list,
            collision_type="warp",
            body_type=arcade.PymunkPhysicsEngine.STATIC,
        )

        self.explosion_sounds = [
            SoundPool("Sounds/explosion.wav", 5, 0.2),
            SoundPool("Sounds/ice-hit.wav", 5, 0.1),
            SoundPool("Sounds/explosion-ele.wav", 5, 0.2)
        ]

        self.shoot_sounds = [
            SoundPool("Sounds/fire-cast.wav", 5, 0.2),
            SoundPool("Sounds/ice-cast.wav", 5, 0.2),
            SoundPool("Sounds/ele-cast.wav", 5, 0.2)
        ]

        def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            bullet_sprite.remove_from_sprite_lists()
            self.on_projectile_death(bullet_sprite)

            if self.on_bullet_death is not None:
                self.on_bullet_death(bullet_sprite)
                

        self.projectile_physics.add_collision_handler(
            "bullet", "wall", post_handler=wall_hit_handler
        )

        def object_hit_handler(bullet_sprite, _object_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """

            if self.on_bullet_death is not None:
                self.on_bullet_death(bullet_sprite)

            self.on_projectile_death(bullet_sprite)

            bullet_sprite.remove_from_sprite_lists()
            _object_sprite.remove_from_sprite_lists()

        self.projectile_physics.add_collision_handler(
            "bullet", "object", post_handler=object_hit_handler
        )

        def player_object_hit_handler(bullet_sprite, _object_sprite, _arbiter, _space, _data):
            """ Called for player/object collision """

            _object_sprite.remove_from_sprite_lists()

            if _object_sprite.kind == 'flask':
                self.game_resources.player_sprite.player_health.health += 10

            if _object_sprite.kind == 'candle_drop':
                self.game_resources.player_sprite.candles += 1

        self.projectile_physics.add_collision_handler(
            "player", "object", post_handler=player_object_hit_handler
        )

        def player_enemy_hit_handler(bullet_sprite, _object_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            self.game_resources.player_sprite.player_health.health -= 1

            if self.game_resources.player_sprite.player_health.health == 0:
                game_resources.dead = True

        self.projectile_physics.add_collision_handler(
            "player", "enemy", post_handler=player_enemy_hit_handler
        )

        def warp_hit_handler(_arbiter, _space, _data):
            warp_sprite, player_sprite = self.projectile_physics.get_sprites_from_arbiter(_arbiter)

            self.projectile_physics.remove_sprite(game_resources.player_sprite)

            new_position = convert_from_tiled_coordinates(
                game_resources.my_map,
                warp_sprite.properties["warp_to_location"]
            )

            self.game_resources.player_sprite.set_position(new_position[0], new_position[1])

            self.game_resources.view_left = new_position[0]
            self.game_resources.view_bottom = new_position[1]

            self.projectile_physics.add_sprite(game_resources.player_sprite,
                                               damping=0.0001,
                                               friction=10.0,
                                               mass=2.0,
                                               moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                               collision_type="player",
                                               max_horizontal_velocity=1200,
                                               max_vertical_velocity=1200,
                                               body_type=arcade.PymunkPhysicsEngine.DYNAMIC)

            game_resources.doors_enabled = True

            barrier_list = game_resources.enemy_manager.make_barrier_list()

            barrier_list = game_resources.enemy_manager.make_barrier_list()

            def spawn_enemy_in_room():
                room_raw = warp_sprite.properties["warp_room_size"]

                x_range = room_raw.x2 - room_raw.x1
                y_range = room_raw.y2 - room_raw.y1

                rand_x = random.randint(room_raw.x1 + 1, room_raw.x1 + x_range - 1)
                rand_y = random.randint(room_raw.y1 + 1, room_raw.y1 + y_range - 1)

                enemy_location = convert_from_tiled_coordinates(
                    game_resources.my_map,
                    (
                        round(round(rand_x * 3) * SPRITE_IMAGE_SIZE),
                        round(round(rand_y * 3) * SPRITE_IMAGE_SIZE)
                    )
                )

                enemy = game_resources.enemy_manager.spawn_enemy(barrier_list, enemy_location)
                self.add_enemy(enemy)

            num_enemies = random.randint(2, 6)

            for i in range(0, num_enemies):
                spawn_enemy_in_room()

            return False

        self.projectile_physics.collision_types.append("warp")
        self.projectile_physics.collision_types.append("player")
        warp_physics_id = self.projectile_physics.collision_types.index("warp")
        player_physics_id = self.projectile_physics.collision_types.index("player")

        handler = self.projectile_physics.space.add_collision_handler(warp_physics_id, player_physics_id)
        handler.begin = warp_hit_handler

        def enemy_bullet_handler(_arbiter, _space, _data):
            bullet_sprite, enemy_sprite = self.projectile_physics.get_sprites_from_arbiter(_arbiter)

            if enemy_sprite:
                enemy_sprite.remove_from_sprite_lists()

                will_drop = random.randint(0, 10)
                if will_drop > 6:
                    self.game_resources.object_manager.flask(enemy_sprite.center_x, enemy_sprite.center_y)

                elif will_drop > 3:
                    self.game_resources.object_manager.candle_drop(enemy_sprite.center_x, enemy_sprite.center_y)
                    self.game_resources.object_manager.object_list
                self.projectile_physics.add_sprite_list(
                self.game_resources.object_manager.object_list,
                        collision_type="object",
                        body_type=arcade.PymunkPhysicsEngine.STATIC,
                    )
                enemy_sprite.on_death()

            if bullet_sprite:
                bullet_sprite.remove_from_sprite_lists()

                if self.on_bullet_death is not None:
                    self.on_bullet_death(bullet_sprite)

                self.on_projectile_death(bullet_sprite)

            if len(game_resources.enemy_manager.enemy_list) == 0:
                game_resources.doors_enabled = False

            return False

        self.projectile_physics.collision_types.append("bullet")
        self.projectile_physics.collision_types.append("enemy")
        bullet_physics_id = self.projectile_physics.collision_types.index("bullet")
        enemy_physics_id = self.projectile_physics.collision_types.index("enemy")

        handler = self.projectile_physics.space.add_collision_handler(bullet_physics_id, enemy_physics_id)
        handler.begin = enemy_bullet_handler

        self.projectile_physics.add_sprite_list(
            self.game_resources.doors_list,
            collision_type="door",
            friction=1.0,
            body_type=arcade.PymunkPhysicsEngine.STATIC,
        )

        def door_player_handler(_arbiter, _space, _data):
            door_sprite, player_sprite = self.projectile_physics.get_sprites_from_arbiter(_arbiter)

            return game_resources.doors_enabled

        self.projectile_physics.collision_types.append("door")
        door_physics_id = self.projectile_physics.collision_types.index("door")

        handler = self.projectile_physics.space.add_collision_handler(door_physics_id, player_physics_id)
        handler.begin = door_player_handler

        def enemy_object_handler(_arbiter, _space, _data):
            door_sprite, player_sprite = self.projectile_physics.get_sprites_from_arbiter(_arbiter)

            return False

        object_physics_id = self.projectile_physics.collision_types.index("object")

        handler = self.projectile_physics.space.add_collision_handler(enemy_physics_id, object_physics_id)
        handler.begin = enemy_object_handler


    light_colors = [
        (1.5, 1.0, 0.2),
        (0.2, 1.0, 1.5),
        (1.0, 0.8, 1.5)
    ]

    def add_enemy(self, enemy_sprite: arcade.Sprite):
        self.projectile_physics.add_sprite(
            enemy_sprite,
            damping=0.0001,
            friction=10.0,
            mass=2.0,
            moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="enemy",
            max_horizontal_velocity=1200,
            max_vertical_velocity=1200,
            body_type=arcade.PymunkPhysicsEngine.DYNAMIC
        )

    def remove_enemy(self, enemy_sprite: arcade.Sprite):
        self.projectile_physics.remove_sprite(enemy_sprite)

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

        self.shoot_sounds[bullet.art_type].play(0.2)

        #TODO:Color based on light
        # add light to sprite
        bullet.point_light = DynamicPointLight(ProjectileManager.light_colors[bullet.art_type], 128.0)

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
        self.projectile_physics.step(delta_time=delta_time)

    def on_projectile_death(self, bullet_sprite):
        #arcade.Sound.play(self.explosion_sound)
        self.explosion_sounds[bullet_sprite.art_type].play(0.2)

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
