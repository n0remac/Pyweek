import arcade

from Constants.Game import SPRITE_SCALING_PLAYER, SPRITE_SCALING_TILES, SPRITE_SIZE
from Constants.Physics import PLAYER_MOVEMENT_SPEED

class EnemyManager:
  # Creates enemies in the dungeon
  def __init__(self, game_resources):

    self.game_resources = game_resources

  def create_enemy(self, x, y, path):
    self.x = x
    self.y = y
    self.speed = PLAYER_MOVEMENT_SPEED
    self.path = path
    self.obstacles = None

    # Create enemy sprite
    self.enemy_sprite = arcade.Sprite(
        "Graphics/Character_animation/monsters_idle/skeleton1/v1/skeleton_v1_1.png", SPRITE_SCALING_PLAYER,
    )
    # Set enemy location
    enemy_grid_x = self.x
    enemy_grid_y = self.y
    self.enemy_sprite.center_x = SPRITE_SIZE * enemy_grid_x + SPRITE_SIZE / 2
    self.enemy_sprite.center_y = SPRITE_SIZE * enemy_grid_y + SPRITE_SIZE / 2

    self.game_resources.enemy_list.append(self.enemy_sprite)

    self.on_update(self.path)
  def on_update(self, path):
    self.path = path
    if len(self.path) > 1:
        if self.path[0][0] < self.path[1][0]:
            self.enemy_sprite.center_x = self.enemy_sprite.center_x + 1
        elif self.path[0][0] > self.path[1][0]:
            self.enemy_sprite.center_x = self.enemy_sprite.center_x - 1

        if self.path[0][1] < self.path[1][1]:
            self.enemy_sprite.center_y = self.enemy_sprite.center_y + 1
        elif self.path[0][1] > self.path[1][1]:
            self.enemy_sprite.center_y = self.enemy_sprite.center_y - 1
