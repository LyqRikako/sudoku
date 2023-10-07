import sudoku

puzzle = [
            [5, 0, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 0, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 0, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 0, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 0, 6, 3, 5],
            [3, 0, 5, 2, 8, 6, 1, 7, 9]
        ]

user_answer=[
            [5, 5, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 2, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 9, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]

false_map=sudoku.check_and_tip(puzzle,user_answer)

print(false_map)