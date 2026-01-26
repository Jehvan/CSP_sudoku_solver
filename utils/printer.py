# Pretty print function for readability

WHITE = "\033[97m"
GREEN = "\033[92m"
RESET = "\033[0m"

def pretty_print(board, fixed):
    print("+-------+-------+-------+")
    for r in range(9):
        print("|", end=" ")
        for c in range(9):
            color = WHITE if (r, c) in fixed else GREEN
            print(color + str(board[r][c]) + RESET, end=" ")
            if (c + 1) % 3 == 0:
                print("|", end=" ")
        print()
        if (r + 1) % 3 == 0:
            print("+-------+-------+-------+")
