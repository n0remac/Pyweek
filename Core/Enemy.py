import arcade
import math
import random

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

    def draw(self):
        if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)

    def on_update(self, path, end):
        self.path = path
        if self.path and len(self.path) > 1:
            if self.path[0][0] < self.path[1][0]:
                self.center_x = self.center_x + self.speed / 5
            elif self.path[0][0] > self.path[1][0]:
                self.center_x = self.center_x - self.speed / 5

            if self.path[0][1] < self.path[1][1]:
                self.center_y = self.center_y + self.speed / 5
            elif self.path[0][1] > self.path[1][1]:
                self.center_y = self.center_y - self.speed / 5


class EnemyManager:
    def __init__(self, game_resources):
        self.game_resources = game_resources
        self.enemy_list = arcade.SpriteList()

        # Enemy
        self.enemy = Enemy(game_resources)
        self.y_spawn_location = []
        self.x_spawn_location = []
        for i in self.game_resources.floor_list:
            if i.position[0] == self.game_resources.player_sprite.position[0]:
                print("i - ps y", i.position[1] - self.game_resources.player_sprite.position[1])
                if i.position[1] - self.game_resources.player_sprite.position[1] < 500:
                    if i.position[1] - self.game_resources.player_sprite.position[1] > -500:
                        self.y_spawn_location.append(i.position[1]) 
        for i in self.game_resources.floor_list:
            if i.position[1] == self.game_resources.player_sprite.position[1]:
                print("i - ps x", i.position[0] - self.game_resources.player_sprite.position[0])
                if i.position[0] - self.game_resources.player_sprite.position[0] < 500:
                    if i.position[0] - self.game_resources.player_sprite.position[0] > -500:
                        self.x_spawn_location.append(i.position[0]) 
        print("player pos", self.game_resources.player_sprite.position)
        random_y = random.randint(0, len(self.y_spawn_location) - 1)
        random_x = random.randint(0, len(self.x_spawn_location) - 1)
        enemy_position = [self.x_spawn_location[random_x], self.y_spawn_location[random_y]]
        print("enemy pos",enemy_position)
        self.enemy.position = enemy_position

        # Add to enemy sprite list
        self.enemy_list.append(self.enemy)

        self.make_barrier_list()

        self.path = self.enemy.path

    def make_barrier_list(self):
        grid_size = SPRITE_SIZE

        playing_field_left_boundary = self.game_resources.player_sprite.center_x - (
            ENEMY_AWARENESS * SPRITE_SIZE
        )
        playing_field_right_boundary = self.game_resources.player_sprite.center_x + (
            ENEMY_AWARENESS * SPRITE_SIZE
        )
        playing_field_top_boundary = self.game_resources.player_sprite.center_y + (
            ENEMY_AWARENESS * SPRITE_SIZE
        )
        playing_field_bottom_boundary = self.game_resources.player_sprite.center_y - (
            ENEMY_AWARENESS * SPRITE_SIZE
        )

        self.barrier_list = arcade.AStarBarrierList(
            self.enemy,
            self.game_resources.wall_list,
            grid_size,
            playing_field_left_boundary,
            playing_field_right_boundary,
            playing_field_bottom_boundary,
            playing_field_top_boundary,
        )

    def setup(self):
        # Enemy Physics engine
        self.enemy_physics_engine = setup_enemy_physics_engine(self.game_resources)

    def on_update(self, delta_time):
        # Makes enemy collide with walls
        self.enemy_physics_engine.update()

        # print("position math x", abs(self.enemy.position[0]) - abs(self.game_resources.player_sprite.position[0]))
        # print("position math y", abs(self.enemy.position[1]) - abs(self.game_resources.player_sprite.position[1]))

        self.path = arcade.astar_calculate_path(
                self.enemy.position,
                self.game_resources.player_sprite.position,
                self.barrier_list,
                diagonal_movement=False,
        )
        # print("path", self.path)
        self.enemy.on_update(self.path, self.game_resources.player_sprite.position)
