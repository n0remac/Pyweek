import arcade

from Constants.Game import SPRITE_SCALING_TILES, SPRITE_SCALING_PLAYER, SPRITE_SIZE
from Core.EnemyManager import EnemyManager


class GameResources:
    """
    Load arcade resources
    """

    def __init__(self):

        # Create the sprite lists
        self.sprite_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.object_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Read in the tiled map
        map_name = "Graphics/test_map.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)
        self.map = my_map
        self.wall_list = arcade.tilemap.process_layer(
            my_map, "Walls", SPRITE_SCALING_TILES
        )
        self.floor_list = arcade.tilemap.process_layer(
            my_map, "Floor", SPRITE_SCALING_TILES
        )
        self.light_list = arcade.tilemap.process_layer(
            my_map, "Lighting", SPRITE_SCALING_TILES
        )

        # Create player sprite
        self.player_sprite = arcade.Sprite(
            "Graphics/player.png", SPRITE_SCALING_PLAYER,
        )

        # Set player location
        grid_x = 10
        grid_y = 5
        self.player_sprite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2
        # Add to player sprite list
        self.player_list.append(self.player_sprite)

        # Enemy Manager
        self.enemy_manager = EnemyManager(self)
        # Enemy
        self.enemy_manager.create_enemy(1, 1, [self.player_sprite.center_x, self.player_sprite.center_y], my_map)
        self.enemy_manager.create_enemy(2, 2, [self.player_sprite.center_x, self.player_sprite.center_y], my_map)

        grid_size = SPRITE_SIZE

        playing_field_left_boundary = -SPRITE_SIZE * 2
        playing_field_right_boundary = SPRITE_SIZE * 35
        playing_field_top_boundary = SPRITE_SIZE * 17
        playing_field_bottom_boundary = -SPRITE_SIZE * 2

        self.barrier_list = arcade.AStarBarrierList(self.enemy_list[0],
                                                    self.wall_list,
                                                    grid_size,
                                                    playing_field_left_boundary,
                                                    playing_field_right_boundary,
                                                    playing_field_bottom_boundary,
                                                    playing_field_top_boundary)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_draw(self):
        self.wall_list.draw()
        self.floor_list.draw()
        self.light_list.draw()
        self.object_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()

    def on_update(self, delta_time):
        pass

        
