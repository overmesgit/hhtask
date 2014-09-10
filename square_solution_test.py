from square_solution import Square, NotIntersectSquares

tests = [
    ([], 0),
    ([[1, 1, 2, 2]], 1),
    ([[1, 1, 2, 2], [1, 1, 2, 2]], 1),
    ([[1, 1, 2, 2], [1, 1, 2, 5]], 4),
    ([[1, 1, 2, 2], [1, 1, 2, 5], [0, 0, 5, 5]], 25),
    ([[0, 1, 3, 3], [2, 2, 6, 4], [1, 0, 3, 5]], 18),
    ([[0, 1, 3, 3], [2, 2, 6, 4], [1, 0, 3, 5], [-1, -1, 0, 0], [0, 0, 1, 1], [1, -1, 2, 6]], 22),
    ([[0, 1, 3, 3], [2, 2, 6, 4], [1, 0, 3, 5], [-1, -1, 0, 0], [0, 0, 1, 1], [1, -1, 2, 6], [-1, 2, 7, 3]], 24),
    ([[-1, -1, 0, 0], [0, 0, 1, 1]], 2),
]

for test in tests:
    squares = [Square(*s) for s in test[0]]

    not_inserted_squares = NotIntersectSquares()
    not_inserted_squares.insert_squares(squares)
    res = not_inserted_squares.get_square_sum()
    # print(res)
    if res != test[1]:
        print(res)