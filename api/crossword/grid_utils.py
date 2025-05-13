from .model import Grid

def create_empty_grid(size: int) -> Grid:
    return [[' ' for _ in range(size)] for _ in range(size)]

def print_grid(grid: Grid):
    for row in grid:
        print(' '.join(row))
