from typing import List
from .model import Grid, WordPlacement
from .grid_utils import create_empty_grid

def load_dictionary(words: List[str]) -> set:
    return set(words)

def intersects_existing_word(grid: Grid, word: str, row: int, col: int, direction: str) -> int:
    count = 0
    if direction == 'across':
        for i, char in enumerate(word):
            if grid[row][col + i] == char:
                count += 1
    elif direction == 'down':
        for i, char in enumerate(word):
            if grid[row + i][col] == char:
                count += 1
    return count

def get_perpendicular_word(grid: Grid, row: int, col: int, direction: str) -> str:
    word = ''
    if direction == 'across':
        r = row
        while r > 0 and grid[r - 1][col] != ' ':
            r -= 1
        while r < len(grid) and grid[r][col] != ' ':
            word += grid[r][col]
            r += 1
    else:
        c = col
        while c > 0 and grid[row][c - 1] != ' ':
            c -= 1
        while c < len(grid[0]) and grid[row][c] != ' ':
            word += grid[row][c]
            c += 1
    return word

def get_all_words_in_grid(grid: Grid) -> List[str]:
    size = len(grid)
    words_found = set()
    for row in grid:
        row_str = ''.join(row)
        for part in row_str.split(' '):
            if len(part) > 1:
                words_found.add(part)
    for col in range(size):
        col_str = ''.join(grid[row][col] for row in range(size))
        for part in col_str.split(' '):
            if len(part) > 1:
                words_found.add(part)
    return list(words_found)

def can_place_word(grid: Grid, word: str, row: int, col: int, direction: str, dictionary: set, require_intersection=True) -> bool:
    size = len(grid)
    temp_grid = [row.copy() for row in grid]

    if direction == 'across':
        if col + len(word) > size:
            return False
        for i, char in enumerate(word):
            r, c = row, col + i
            cell = grid[r][c]
            if cell != ' ' and cell != char:
                return False
        if require_intersection and intersects_existing_word(grid, word, row, col, direction) == 0:
            return False
        for i, char in enumerate(word):
            if temp_grid[row][col + i] == ' ':
                temp_grid[row][col + i] = char
                perp = get_perpendicular_word(temp_grid, row, col + i, direction)
                if len(perp) > 1 and perp not in dictionary:
                    return False
    elif direction == 'down':
        if row + len(word) > size:
            return False
        for i, char in enumerate(word):
            r, c = row + i, col
            cell = grid[r][c]
            if cell != ' ' and cell != char:
                return False
        if require_intersection and intersects_existing_word(grid, word, row, col, direction) == 0:
            return False
        for i, char in enumerate(word):
            if temp_grid[row + i][col] == ' ':
                temp_grid[row + i][col] = char
                perp = get_perpendicular_word(temp_grid, row + i, col, direction)
                if len(perp) > 1 and perp not in dictionary:
                    return False
    else:
        return False

    for i, char in enumerate(word):
        r, c = (row + i, col) if direction == 'down' else (row, col + i)
        temp_grid[r][c] = char

    all_words = get_all_words_in_grid(temp_grid)
    return all(w in dictionary for w in all_words)

def place_word(grid: Grid, word: str, row: int, col: int, direction: str):
    print(f"Placing word '{word}' at ({row}, {col}) {direction}")
    for i, char in enumerate(word):
        r, c = (row + i, col) if direction == 'down' else (row, col + i)
        grid[r][c] = char

def is_word_in_grid(grid: Grid, word: str) -> bool:
    for row in grid:
        if word in ''.join(row):
            return True
    for col in zip(*grid):
        if word in ''.join(col):
            return True
    return False

def generate_crossword(words: List[str], grid_size: int = 15) -> Grid:
    grid = create_empty_grid(grid_size)
    dictionary = load_dictionary(words)
    words.sort(key=len, reverse=True)

    place_word(grid, words[0], grid_size // 2, (grid_size - len(words[0])) // 2, 'across')

    for word in words[1:]:
        print(f"Trying to place word: {word}")
        if is_word_in_grid(grid, word):
            print(f"Skipped '{word}' (already on grid)")
            continue

        best_score = -1
        best_placement = None

        for row in range(grid_size):
            for col in range(grid_size):
                for direction in ['across', 'down']:
                    if can_place_word(grid, word, row, col, direction, dictionary, require_intersection=True):
                        score = intersects_existing_word(grid, word, row, col, direction)
                        if score > best_score:
                            best_score = score
                            best_placement = (row, col, direction)

        if best_placement:
            row, col, direction = best_placement
            place_word(grid, word, row, col, direction)
        else:
            print(f"Trying fallback placement for: {word}")
            placed = False
            for row in range(grid_size):
                for col in range(grid_size):
                    for direction in ['across', 'down']:
                        if can_place_word(grid, word, row, col, direction, dictionary, require_intersection=False):
                            place_word(grid, word, row, col, direction)
                            placed = True
                            break
                    if placed: break
                if placed: break

    return grid
