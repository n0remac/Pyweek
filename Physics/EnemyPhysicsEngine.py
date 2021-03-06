import arcade

from Constants.Physics import PLAYER_MOVEMENT_SPEED

# from Core.GameResources import GameResources


def setup_enemy_physics_engine(game_resources):
    # --- Pymunk Physics Engine Setup ---

    # Create the physics engine
    enemy_physics_engine = arcade.PhysicsEngineSimple(
        game_resources.enemy_manager.enemy, game_resources.wall_list
    )

    return enemy_physics_engine
