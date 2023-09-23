import concurrent.futures
import random

# 判断是否可以填数
def could_place(board, row, col, num):
    # 判断行中是否出现重复
    for i in range(9):
        if board[row][i] == num:
            return False
    # 判断列中是否出现重复
    for i in range(9):
        if board[i][col] == num:
            return False
    # 判断 3x3 宫中是否出现重复
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

# 解数独
def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if could_place(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# 生成数独
def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    for row in range(9):
        for col in range(9):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for num in nums:
                if could_place(board, row, col, num):
                    board[row][col] = num
                    if solve_sudoku(board):
                        return board
                    board[row][col] = 0

# 获取固定的数独
def get_fixed_sudoku(board, level):
    fixed_board = [[val if random.randint(1, 10) <= level else 0 for val in row] for row in board]
    return fixed_board

# 生成数独谜题和答案
def generate_sudoku_puzzle(level=5):
    puzzles = []
    solutions = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(9):
            future = executor.submit(generate_sudoku)
            puzzles.append(get_fixed_sudoku(future.result(), level))
            solutions.append(future.result())

    return puzzles, solutions

# 格式化并打印数独板
def format_sudoku(board):
    formatted_board = ""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                formatted_board += " -"
            else:
                formatted_board += " " + str(board[i][j])
            if (j + 1) % 3 == 0 and j < 8:
                formatted_board += " |"
        formatted_board += "\n"
        if (i + 1) % 3 == 0 and i < 8:
            formatted_board += "-" * 21 + "\n"
    return formatted_board

# 显示数独板
def display_sudoku(board):
    formatted_board = format_sudoku(board)
    print(formatted_board)

def main():
    # 生成数独谜题和答案，并显示
    sudoku_puzzles, sudoku_solutions = generate_sudoku_puzzle()
    for puzzle, solution in zip(sudoku_puzzles, sudoku_solutions):
        print("数独谜题：")
        display_sudoku(puzzle)
        print("答案：")
        display_sudoku(solution)
        print()

if __name__ == "__main__":
    main()