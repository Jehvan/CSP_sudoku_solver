WHITE = "\033[97m"    # Fixed
GREEN = "\033[92m"    # Solved
BLUE = "\033[94m"     # Odd
MAGENTA = "\033[95m"  # Even
CYAN = "\033[96m"     # Diagonal
RESET = "\033[0m"


def pretty_print(board, fixed=set(), parity=None, diagonal=False):
    print("+-------+-------+-------+")
    for r in range(9):
        print("|", end=" ")
        for c in range(9):
            val = board[r][c]

            # Base coloring
            if (r, c) in fixed:
                color = WHITE
            else:
                color = GREEN

            # Odd / Even coloring (overrides base)
            if parity is not None:
                p = parity[r][c]
                if p == "O":
                    color = BLUE
                elif p == "E":
                    color = MAGENTA

            # Diagonal coloring (highest priority)
            if diagonal and (r == c or r + c == 8):
                color = CYAN

            print(f"{color}{val}{RESET}", end=" ")

            if (c + 1) % 3 == 0:
                print("|", end=" ")
        print()
        if (r + 1) % 3 == 0:
            print("+-------+-------+-------+")
