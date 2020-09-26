import arcade

from Constants.Physics import PLAYER_MOVEMENT_SPEED
from Core.GameResources import GameResources


def setup_physics_engine(game_resources: GameResources):
    # --- Pymunk Physics Engine Setup ---

    # Make a list for all impassable objects
    solids = game_resources.wall_list
    solids.extend(game_resources.object_list)

    # Create the physics engine
    physics_engine = arcade.PhysicsEngineSimple(game_resources.player_sprite, solids)

    return physics_engine
