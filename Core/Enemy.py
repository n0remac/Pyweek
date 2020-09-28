import arcade
from arcade import SpriteList
from typing import List, Union

from Core.Character import Character
from Constants.Game import SPRITE_SIZE, SPRITE_SCALING_PLAYER, ENEMY_AWARENESS
from Constants.Physics import PLAYER_MOVEMENT_SPEED


class Enemy(Character):
    def __init__(self, barrier_list, game_resources):
        super().__init__(
            "Graphics/Character_animation/monsters_idle/vampire/v2/vampire_v2",
        )
        self.load_textures()
        self.game_resources = game_resources
        self.speed = PLAYER_MOVEMENT_SPEED
        self.path = [
            self.game_resources.player_sprite.center_x,
            self.game_resources.player_sprite.center_y,
        ]
        self.obstacles = self.game_resources.wall_list

        self.barrier_list = barrier_list

        self.light = game_resources.scene_renderer.light_renderer.create_point_light(
            (-1000, -1000), (1.5, 0.5, 0.25), 196
        )
        self.barrier_list = barrier_list

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


class EnemyManager:
    enemy_list: Union[SpriteList, List[Enemy]]

    def __init__(self, game_resources):
        self.game_resources = game_resources
        self.enemy_list = arcade.SpriteList()

    def spawn_enemy(self, barrier_list, position):
        # Enemy
        enemy = Enemy(barrier_list, self.game_resources)
        enemy.position = position

        self.path = enemy.path

        # Add to enemy sprite list
        self.enemy_list.append(enemy)

        return enemy

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

        for enemy in self.enemy_list:
            position = self.game_resources.player_sprite.position
            if arcade.get_distance(position[0], position[1], enemy.position[0], enemy.position[1]) < 500:
                enemy.calculate_astar()
                enemy.update_position()
                enemy.update_animation(delta_time)
