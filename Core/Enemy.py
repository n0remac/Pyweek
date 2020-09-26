import arcade
import math
import random

from Constants.Game import (
    SPRITE_SIZE,
    SPRITE_SCALING_PLAYER,
    ENEMY_AWARENESS,
    SPRITE_SCALING_TILES,
    SPRITE_IMAGE_SIZE,
)
from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Physics.EnemyPhysicsEngine import setup_enemy_physics_engine


class Enemy(arcade.Sprite):
    def __init__(self, game_resources, obstacles):
        super().__init__(
            "Graphics/Character_animation/monsters_idle/skeleton1/v1/skeleton_v1_1.png",
            scale=SPRITE_SCALING_TILES,
        )
        self.game_resources = game_resources
        self.enemy_physics_engine = arcade.PhysicsEngineSimple(self, obstacles)

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
        self.make_barrier_list(self.game_resources.player_sprite)
        self.prev_time = 0

    def create_enemy(self):
        # Enemy
        self.enemy = Enemy(self.game_resources, self.enemy_list)

        player_x = round(self.game_resources.player_sprite.center_x)
        player_y = round(self.game_resources.player_sprite.center_y)

        x = random.randint(player_x - 500, player_x + 500)
        y = random.randint(player_y - 500, player_y + 500)

        grid_x = math.floor(x / SPRITE_IMAGE_SIZE)
        grid_y = math.floor(y / SPRITE_IMAGE_SIZE)
        

        floor_tiles = []

        for floor in self.game_resources.floor_list:
            if (
                floor.position[1] > grid_y - 500 or floor.position[1] < grid_y + 500
            ) and (
                floor.position[0] > grid_x - 500 or floor.position[0] < grid_x + 500
            ):
                floor_tiles.append(floor)
        if len(floor_tiles) == 0:
            return

        spawn_tile = random.choice(floor_tiles)

        self.enemy.position = spawn_tile.position

        # Add to enemy sprite list
        self.enemy_list.append(self.enemy)
        

    def make_barrier_list(self, player):
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
            player,
            self.game_resources.wall_list,
            grid_size,
            playing_field_left_boundary,
            playing_field_right_boundary,
            playing_field_bottom_boundary,
            playing_field_top_boundary,
        )

    def on_update(self, delta_time):
        # update physics, path, and position for all the enemies.
        #if delta_time > prev_time
        for enemy in self.enemy_list:
            # Makes enemy collide with walls
            enemy.enemy_physics_engine.update()
            path = arcade.astar_calculate_path(
                enemy.position,
                self.game_resources.player_sprite.position,
                self.barrier_list,
                diagonal_movement=False,
            )
            # print("path", self.path)
            enemy.on_update(path, self.game_resources.player_sprite.position)


"""
# Enemy
        enemy = Enemy(self.game_resources, obstacles)
        y_spawn_location = []
        x_spawn_location = []

        for i in self.game_resources.floor_list:
            if i.position[0] == self.game_resources.player_sprite.position[0]:
                # print("i - ps y", i.position[1] - self.game_resources.player_sprite.position[1])
                if i.position[1] - self.game_resources.player_sprite.position[1] < 500:
                    if (
                        i.position[1] - self.game_resources.player_sprite.position[1]
                        > -500
                    ):
                        y_spawn_location.append(i.position[1])

        for i in self.game_resources.floor_list:
            if i.position[1] == self.game_resources.player_sprite.position[1]:
                # print("i - ps x", i.position[0] - self.game_resources.player_sprite.position[0])
                if i.position[0] - self.game_resources.player_sprite.position[0] < 500:
                    if (
                        i.position[0] - self.game_resources.player_sprite.position[0]
                        > -500
                    ):
                        x_spawn_location.append(i.position[0])

        # print("player pos", self.game_resources.player_sprite.position)
        random_y = random.randint(0, len(y_spawn_location) - 1)
        random_x = random.randint(0, len(x_spawn_location) - 1)
"""
