SCREEN_TITLE = "The Acolyte"

# How big are our image tiles?
SPRITE_IMAGE_SIZE = 16

# Scale sprites up or down
SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_TILES = 1

# Scaled sprite size for tiles
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

# Camera lerp amount
CAMERA_SPEED = .95
# distance before camera moves towards the player, as a proportion of the height of the screen
LERP_MARGIN = 0

# Size of grid to show on screen, in number of tiles
SCREEN_GRID_WIDTH = 32
SCREEN_GRID_HEIGHT = 18

# Size of screen to show, in pixels
"""
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT
"""
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 270


# Constants used to track if the player is facing left or right
DOWN_FACING = 0
UP_FACING = 1
RIGHT_FACING = 0
LEFT_FACING = 1

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 200
TOP_VIEWPORT_MARGIN = 200

# How close the player needs to be for the enemy to track it.
# starts to break above 15
ENEMY_AWARENESS = 64
