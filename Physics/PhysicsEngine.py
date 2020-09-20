import arcade

from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Core.GameResources import GameResources


def setup_physics_engine(game_resources: GameResources):
    # --- Pymunk Physics Engine Setup ---

    # Create the physics engine
    physics_engine = arcade.PhysicsEngineSimple(
        game_resources.player_sprite, game_resources.wall_list
    )

    return physics_engine
