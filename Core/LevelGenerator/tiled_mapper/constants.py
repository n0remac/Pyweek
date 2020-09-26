open_floor_tile_ids = [
    6,
    7,
    8,
    9,
    16,
    17,
    18,
    19,
    22,
    23,
    26,
    27,
    28,
    29,
    70,
    71,
    72,
    73,
    79,
]

# Used for the "infinite" void of wall space
closed_wall_tile_ids = [78]

# inner corner tiles
top_left_inner_floor_tile_ids = [11]
top_right_inner_floor_tile_ids = [14]
bottom_left_inner_floor_tile_ids = [31]
bottom_right_inner_floor_tile_ids = [34]

# inner side tiles
top_inner_floor_tile_ids = [12, 13]
right_inner_floor_tile_ids = [24]
bottom_inner_floor_tile_ids = [32, 33]
left_inner_floor_tile_ids = [21]

# outer corner tiles
top_left_outer_wall_tile_ids = [0]
top_right_outer_wall_tile_ids = [5]
bottom_left_outer_wall_tile_ids = [40]
bottom_right_outer_wall_tile_ids = [45]

# outer wall tiles
top_outer_wall_tile_ids = [1, 2, 3, 4]
right_outer_wall_tile_ids = [15, 25, 35]
bottom_outer_wall_tile_ids = [41, 42, 43, 44]
left_outer_wall_tile_ids = [10, 20, 30]

# vertical tunnel corner pieces
top_left_outer_vertical_tunnel_wall_ids = [53]
top_right_outer_vertical_tunnel_wall_ids = [50]
bottom_right_outer_vertical_tunnel_wall_ids = top_outer_wall_tile_ids
bottom_left_outer_vertical_tunnel_wall_ids = top_outer_wall_tile_ids

# horizontal tunnel corner pieces
top_left_outer_horizontal_tunnel_wall_ids = top_outer_wall_tile_ids
top_right_outer_horizontal_tunnel_wall_ids = top_outer_wall_tile_ids
bottom_right_outer_horizontal_tunnel_wall_ids = [50]
bottom_left_outer_horizontal_tunnel_wall_ids = [53]

# all floor tiles
all_open_floor_tiles = (
    open_floor_tile_ids
    + top_left_inner_floor_tile_ids
    + top_right_inner_floor_tile_ids
    + bottom_left_inner_floor_tile_ids
    + bottom_right_inner_floor_tile_ids
)

# lights
light_fixtures = [90, 93, 95]

# warp
warps = [38, 39]

# doors
vertical_door_top = [46]
vertical_door_bottom = [56]
horizontal_door_left = [36]
horizontal_door_right = [37]


