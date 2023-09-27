import concurrent.futures
import random
import copy
import sys
sys.setrecursionlimit(10000)
# 判断是否可以填数

#第一步判断，用于判断行和列重复
#board用于存储九宫格的数字，row为行，col为列，输入一个数字num判断行列中是否有重复
def could_place(board, row, col, num):
    # 判断行中是否出现重复
    for i in range(9):
        if board[row][i] == num:
            return False
    # 判断列中是否出现重复
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # 第二步判断 用于判断 3x3 宫中是否出现重复
    #将9*9九宫格切割为9个3*3九宫格，对数字num所在九宫格中的数字进行重复判断
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

# 判明数独是否有解
def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                #调用函数，从1~9尝试填入数字，判断是否可以填入，如果可以填入，再递归调用solve函数，判明数独是否有解
                for num in range(1, 10):
                    if could_place(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# #判断是否是唯一解,在solve的基础上进行改编，通过count参数的大小来判断是否有唯一解
# def only_solve_sudoku(board, count):
#     for row in range(9):
#         for col in range(9):
#             if board[row][col] == 0:
#                 for num in range(1, 10):
#                     if could_place(board, row, col, num):
#                         board[row][col] = num
#                         if only_solve_sudoku(board, count):
#                             count += 1
#                             if count > 1: # 如果已经找到两个及以上的解，则可以提前结束函数执行
#                                 return True
#                         board[row][col] = 0
#                 return False
#     return True


def only_solve_sudoku(board,count):
    empty_cells = []
    count = 0 # 计数器

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                empty_cells.append((row, col))

    stack = [(board, 0)] # 使用栈保存待处理的空白格子及索引位置
    while stack:
        curr_board, index = stack.pop()
        if index == len(empty_cells):
            count += 1
            if count > 1: # 如果已经找到两个及以上的解，则可以提前结束函数执行
                return True
            continue

        row, col = empty_cells[index]
        for num in range(1, 10):
            if could_place(curr_board, row, col, num):
                new_board = copy.deepcopy(curr_board)
                new_board[row][col] = num
                stack.append((new_board, index + 1))

    if count == 1:
        return True
    else:
        return False


# 生成数独答案
def generate_sudoku():
    #初始化一个空的9*9二维列表
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

# 判明数独是否有唯一解
def is_unique_solution(board):
    # 统计解的数量
    count=0
    only_solve_sudoku(board,count)
    return count == 1

# 获取固定的数独
    #设置一个随机数，在挖空的时候对每个空判断随机数，如果大于所设难度等级，则保留数字，否则挖空为0
    #根据概率学 难度为1挖空10%，难度为2挖空20%，以此类推，最高难度为5，挖空50%
def get_fixed_sudoku(board, level):
    fixed_board = [[val if random.randint(1, 10) > level else 0 for val in row] for row in board]
    temp_fixedboard = copy.deepcopy(fixed_board)

    if is_unique_solution(temp_fixedboard):
        return fixed_board 
    else:
        return get_fixed_sudoku(board, level)  # 传递递归函数的返回值


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
        print(puzzle)
        display_sudoku(puzzle)
        print("答案：")
        display_sudoku(solution)
        print()

if __name__ == "__main__":
    main()