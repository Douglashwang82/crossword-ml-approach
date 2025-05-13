from typing import List

Grid = List[List[str]]

class WordPlacement:
    def __init__(self, word: str, row: int, col: int, direction: str):
        self.word = word
        self.row = row
        self.col = col
        self.direction = direction  # 'across' or 'down'
