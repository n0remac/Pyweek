SCREEN_TITLE = "Castaway Wizard"

# How big are our image tiles?
SPRITE_IMAGE_SIZE = 16

# Scale sprites up or down
SPRITE_SCALING_PLAYER = 2
SPRITE_SCALING_TILES = 2

# Scaled sprite size for tiles
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

# Size of grid to show on screen, in number of tiles
SCREEN_GRID_WIDTH = 45
SCREEN_GRID_HEIGHT = 28

# Size of screen to show, in pixels
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT


# Constants used to track if the player is facing left or right
DOWN_FACING = 0
UP_FACING = 1
RIGHT_FACING = 0
LEFT_FACING = 1

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 500 
RIGHT_VIEWPORT_MARGIN = 500
BOTTOM_VIEWPORT_MARGIN = 400
TOP_VIEWPORT_MARGIN = 400

# How close the player needs to be for the enemy to track it.
# starts to break above 15
ENEMY_AWARENESS = 40
