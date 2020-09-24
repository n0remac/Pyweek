SCREEN_TITLE = "Castaway Wizard"

# How big are our image tiles?
SPRITE_IMAGE_SIZE = 16

# Scale sprites up or down
SPRITE_SCALING_PLAYER = 2
SPRITE_SCALING_TILES = 2

# Scaled sprite size for tiles
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

# Size of grid to show on screen, in number of tiles
SCREEN_GRID_WIDTH = 30
SCREEN_GRID_HEIGHT = 15

# Size of screen to show, in pixels
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT

# Angle values for the spell selection rings, in degrees
AIR_ANGLE = 270
FIRE_ANGLE = 37
WATER_ANGLE = 143

CONE_ANGLE = AIR_ANGLE
BEAM_ANGLE = FIRE_ANGLE
BALL_ANGLE = WATER_ANGLE

# Selected spell Constants
CONE = 0
BEAM = 1
BALL = 2

AIR = 0
FIRE = 1
WATER = 2
