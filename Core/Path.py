
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def route(start, end, matrix):
    print("start",start[0], start[1])
    # print("end", end[0], end[1])
    grid = Grid(matrix=matrix)
    print("grid",grid.nodes[0])
    start = grid.node(start[0], start[1])
    end = grid.node(end[0], end[1])
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path = finder.find_path(start, end, grid)
    # print("path", path)

    return path