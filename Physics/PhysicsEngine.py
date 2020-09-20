import arcade

from Constants.Physics import (
    DEFAULT_DAMPING,
    GRAVITY,
    PLAYER_FRICTION,
    PLAYER_MASS,
    PLAYER_MAX_HORIZONTAL_SPEED,
    PLAYER_MAX_VERTICAL_SPEED,
    WALL_FRICTION,
    DYNAMIC_ITEM_FRICTION,
)
from Core.GameResources import GameResources


def setup_physics_engine(game_resources: GameResources):
    # --- Pymunk Physics Engine Setup ---

    # The default damping for every object controls the percent of velocity
    # the object will keep each second. A value of 1.0 is no speed loss,
    # 0.9 is 10% per second, 0.1 is 90% per second.
    # For top-down games, this is basically the friction for moving objects.
    # For platformers with gravity, this should probably be set to 1.0.
    # Default value is 1.0 if not specified.
    damping = DEFAULT_DAMPING

    # Create the physics engine
    physics_engine = arcade.PymunkPhysicsEngine(damping=damping)

    # Add the player.
    # For the player, we set the damping to a lower value, which increases
    # the damping rate. This prevents the character from traveling too far
    # after the player lets off the movement keys.
    # Setting the moment to PymunkPhysicsEngine.MOMENT_INF prevents it from
    # rotating.
    # Friction normally goes between 0 (no friction) and 1.0 (high friction)
    # Friction is between two objects in contact. It is important to remember
    # in top-down games that friction moving along the 'floor' is controlled
    # by damping.
    physics_engine.add_sprite(
        game_resources.player_sprite,
        friction=PLAYER_FRICTION,
        mass=PLAYER_MASS,
        moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
        collision_type="player",
        max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
        max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED,
    )

    # Create the walls.
    # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
    # move.
    # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
    # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
    # repositioned by code and don't respond to physics forces.
    # Dynamic is default.
    physics_engine.add_sprite_list(
        game_resources.wall_list,
        friction=WALL_FRICTION,
        collision_type="wall",
        body_type=arcade.PymunkPhysicsEngine.STATIC,
    )
    """
	# Create the items
	physics_engine.add_sprite_list(
		game_resources.item_list,
		friction=DYNAMIC_ITEM_FRICTION,
		collision_type="item"
	)
	"""
    return physics_engine
