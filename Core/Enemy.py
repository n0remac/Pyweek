from typing import List, Union

import arcade
import random

from arcade import SpriteList

from Constants.Game import SPRITE_SIZE, SPRITE_SCALING_PLAYER, ENEMY_AWARENESS
from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Physics.EnemyPhysicsEngine import setup_enemy_physics_engine


class Enemy(arcade.Sprite):
    def __init__(self, game_resources):
        super().__init__(
            "Graphics/Character_animation/monsters_idle/skeleton1/v1/skeleton_v1_1.png",
            SPRITE_SCALING_PLAYER,
        )
        self.game_resources = game_resources
        self.speed = PLAYER_MOVEMENT_SPEED
        self.path = [
            self.game_resources.player_sprite.center_x,
            self.game_resources.player_sprite.center_y,
        ]
        self.obstacles = self.game_resources.wall_list
        self.barrier_list = self.make_barrier_list()

    def draw(self):
        if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)

    def calculate_astar(self):
        # self.barrier_list = self.make_barrier_list()
        self.path = arcade.astar_calculate_path(
            self.position,
            self.game_resources.player_sprite.position,
            self.barrier_list,
            diagonal_movement=True,
        )

    def make_barrier_list(self):
        grid_size = SPRITE_SIZE

        playing_field_left_boundary = self.game_resources.player_sprite.position[0] - (
                ENEMY_AWARENESS * SPRITE_SIZE
        )
        playing_field_right_boundary = self.game_resources.player_sprite.position[0] + (
                ENEMY_AWARENESS * SPRITE_SIZE
        )
        playing_field_top_boundary = self.game_resources.player_sprite.position[1] + (
                ENEMY_AWARENESS * SPRITE_SIZE
        )
        playing_field_bottom_boundary = self.game_resources.player_sprite.position[1] - (
                ENEMY_AWARENESS * SPRITE_SIZE
        )

        return arcade.AStarBarrierList(
            self.game_resources.player_sprite,
            self.game_resources.wall_list,
            grid_size,
            playing_field_left_boundary,
            playing_field_right_boundary,
            playing_field_bottom_boundary,
            playing_field_top_boundary,
        )

    def update_position(self):
        if self.path and len(self.path) > 1:
            first_leg = self.path[0]
            second_leg = self.path[1]

            position_difference_x = first_leg[0] - second_leg[0]
            position_difference_y = first_leg[1] - second_leg[1]

            physics_engine = self.game_resources.projectile_manager.projectile_physics

            impulse_force = (0, 0)

            if position_difference_x > 0:
                impulse_force = (-100, impulse_force[1])
            elif position_difference_x < 0:
                impulse_force = (100, impulse_force[1])

            if position_difference_y > 0:
                impulse_force = (impulse_force[0], -100)
            elif position_difference_y < 0:
                impulse_force = (impulse_force[0], 100)

            physics_engine.apply_impulse(self, impulse_force)

            # if self.path[0][0] < self.path[1][0]:
            #     self.position = (self.position[0])
            #     self.position[0] = self.position[0] + self.speed / 5
            # elif self.path[0][0] > self.path[1][0]:
            #     self.center_x = self.center_x - self.speed / 5
            #
            # if self.path[0][1] < self.path[1][1]:
            #     self.center_y = self.center_y + self.speed / 5
            # elif self.path[0][1] > self.path[1][1]:
            #     self.center_y = self.center_y - self.speed / 5


class EnemyManager:
    enemy_list: Union[SpriteList, List[Enemy]]

    def __init__(self, game_resources):
        self.game_resources = game_resources
        self.enemy_list = arcade.SpriteList()

    def spawn_enemy(self, position):
        # Enemy
        enemy = Enemy(self.game_resources)
        #
        # y_spawn_location = []
        # x_spawn_location = []
        #
        # for i in self.game_resources.floor_list:
        #     if i.position[0] == self.game_resources.player_sprite.position[0]:
        #         print("i - ps y", i.position[1] - self.game_resources.player_sprite.position[1])
        #         if i.position[1] - self.game_resources.player_sprite.position[1] < 500:
        #             if i.position[1] - self.game_resources.player_sprite.position[1] > -500:
        #                 y_spawn_location.append(i.position[1])
        #
        # for i in self.game_resources.floor_list:
        #     if i.position[1] == self.game_resources.player_sprite.position[1]:
        #         print("i - ps x", i.position[0] - self.game_resources.player_sprite.position[0])
        #         if i.position[0] - self.game_resources.player_sprite.position[0] < 500:
        #             if i.position[0] - self.game_resources.player_sprite.position[0] > -500:
        #                 x_spawn_location.append(i.position[0])
        #
        # random_y = random.randint(0, len(y_spawn_location))
        # random_x = random.randint(0, len(x_spawn_location))
        # enemy_position = [x_spawn_location[random_x], y_spawn_location[random_y]]
        enemy.position = position

        self.path = enemy.path

        # Add to enemy sprite list
        self.enemy_list.append(enemy)

        return enemy

    def kill_enemy(self, enemy):
        if enemy in self.enemy_list:
            self.enemy_list.remove(enemy)

    def setup(self):
        pass

    def on_update(self, delta_time):

        # print("position math x", abs(self.enemy.position[0]) - abs(self.game_resources.player_sprite.position[0]))
        # print("position math y", abs(self.enemy.position[1]) - abs(self.game_resources.player_sprite.position[1]))

        for enemy in self.enemy_list:
            position = self.game_resources.player_sprite.position
            if arcade.get_distance(position[0], position[1], enemy.position[0], enemy.position[1]) < 500:
                enemy.calculate_astar()
                enemy.update_position()
