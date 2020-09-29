import random

import arcade
from arcade import SpriteList
from typing import List, Union

from Constants.Game import ENEMY_AWARENESS, PATHING_RATE, SPRITE_SIZE
from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Core.Character import Character

class Enemy(Character):
    def __init__(self, barrier_list, game_resources):
        super().__init__()
        self.randomize_enemy_sprite()
        self.load_textures()
        self.game_resources = game_resources
        self.speed = PLAYER_MOVEMENT_SPEED
        self.path = []
        self.obstacles = self.game_resources.wall_list

        self.barrier_list = barrier_list

        self.light = game_resources.scene_renderer.light_renderer.create_point_light(
            (-1000, -1000), (1.5, 0.5, 0.25), 196
        )

    def randomize_enemy_sprite(self):
        sprites = [
            "Graphics/Character_animation/monsters_idle/vampire/v2/vampire_v2",
            "Graphics/Character_animation/monsters_idle/skull/v2/skull_v2",
            "Graphics/Character_animation/monsters_idle/skeleton2/v2/skeleton2_v2",
            "Graphics/Character_animation/monsters_idle/skeleton1/v2/skeleton_v2",
                   ]
        choice = random.choice(sprites)
        self.main_path = choice

    def draw(self):
        if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)      

    def on_death(self):
        self.game_resources.scene_renderer.light_renderer.destroy_light(self.light)


    def calculate_astar(self):
        # self.barrier_list = self.make_barrier_list()
        self.path = arcade.astar_calculate_path(
            self.position,
            self.game_resources.player_sprite.position,
            self.barrier_list,
            diagonal_movement=True,
        )

    def update_position(self):
        if self.path and len(self.path) > 1:
            first_leg = self.path[0]
            second_leg = self.path[1]

            position_difference_x = first_leg[0] - second_leg[0]
            position_difference_y = first_leg[1] - second_leg[1]

            physics_engine = self.game_resources.projectile_manager.projectile_physics

            impulse_force = (0, 0)

            move_force = 20

            if position_difference_x > 0:
                impulse_force = (-move_force, impulse_force[1])
            elif position_difference_x < 0:
                impulse_force = (move_force, impulse_force[1])

            if position_difference_y > 0:
                impulse_force = (impulse_force[0], -move_force)
            elif position_difference_y < 0:
                impulse_force = (impulse_force[0], move_force)

            physics_engine.apply_impulse(self, impulse_force)
            self.light.position = (self.center_x, self.center_y)

    def on_update(self, delta_time):
        self.update_position()
        self.update_animation(delta_time)


class EnemyManager:
    enemy_list: Union[SpriteList, List[Enemy]]

    def __init__(self, game_resources):
        self.game_resources = game_resources
        self.enemy_list = arcade.SpriteList()
        self.next_to_path = 0
        self.time_elapsed = 0
        self.barrier_list = self.make_barrier_list()

    def spawn_enemy(self, position=(0,0)):
        # Enemy
        enemy = Enemy(self.barrier_list, self.game_resources)
        enemy.position = position

        self.path = enemy.path

        # Add to enemy sprite list
        self.enemy_list.append(enemy)

        self.game_resources.projectile_manager.add_enemy(enemy)

        return enemy

    def spawn_random_enemy(self):
        radius = self.game_resources.player_sprite.player_health.max_light_radius
        player_pos = self.game_resources.player_sprite.position

        rand_x = random.randint(int(player_pos[0]-radius), int(player_pos[0]+radius))
        rand_y = random.randint(int(player_pos[1] - radius), int(player_pos[1] + radius))
        enemy = self.spawn_enemy(self.make_barrier_list(), (player_pos[0]+100, player_pos[1]+100))
        self.game_resources.projectile_manager.add_enemy(enemy)
        #for floor in self.game_resources.floor_list:
        #    if floor.position[0] < rand_x + 100 and floor.position[0] > rand_x - 100 and floor.position[1] < rand_x + 100 and floor.position[1] > rand_x - 100:
        #        self.spawn_enemy(self.make_barrier_list(), floor.position)

    def spawn_continual_enemies(self):
        if len(self.enemy_list) < 5:
            self.spawn_random_enemy()

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

    def kill_enemy(self, enemy):
        if enemy in self.enemy_list:
            self.enemy_list.remove(enemy)

    def setup(self):
        pass

    def on_update(self, delta_time):

        # move enemies
        for enemy in self.enemy_list:
            position = self.game_resources.player_sprite.position
            if arcade.get_distance(position[0], position[1], enemy.position[0], enemy.position[1]) < 500:
                enemy.on_update(delta_time)

        # path the next enemy in line
        if self.time_elapsed >= PATHING_RATE:
            if self.next_to_path < len(self.enemy_list):
                self.enemy_list[self.next_to_path].calculate_astar()
                self.next_to_path += 1
            else:
                self.next_to_path = 0

        self.time_elapsed += delta_time