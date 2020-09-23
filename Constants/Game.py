SCREEN_TITLE = "Castaway Wizard"

# How big are our image tiles?
SPRITE_IMAGE_SIZE = 16

# Scale sprites up or down
SPRITE_SCALING_PLAYER = 2
SPRITE_SCALING_TILES = 2

# Scaled sprite size for tiles
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

# Size of grid to show on screen, in number of tiles
SCREEN_GRID_WIDTH = 35
SCREEN_GRID_HEIGHT = 25

# Size of screen to show, in pixels
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT
