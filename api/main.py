from crossword.core import generate_crossword
from crossword.grid_utils import print_grid

words = [
    "crossword", "python", "puzzle", "logic", "algorithm", "function",
    "variable", "matrix", "grid", "loop", "conditional", "compile", "debug",
    "execute", "nested", "recursion", "syntax", "statement", "operator",
    "binary", "decimal", "integer", "boolean", "character", "string", "method",
    "class", "object", "inheritance", "interface", "module", "package", "import",
    "array", "list", "tuple", "dictionary", "lambda", "exception", "index",
    "scope", "closure", "thread", "process", "pointer", "heap", "stack",
    "virtual", "instance", "static", "attribute", "reference", "constant",
    "condition", "iteration", "break", "continue", "return", "input", "output",
    "key", "sony", "sir", "cap"
]

if __name__ == '__main__':
    grid = generate_crossword(words, 15)
    print_grid(grid)
