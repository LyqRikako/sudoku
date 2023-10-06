import concurrent.futures
import random
import copy
# 判断是否可以填数
# 第一步判断，用于判断行和列重复
# board用于存储九宫格的数字，row为行，col为列，输入一个数字num判断行列中是否有重复
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
    # 将9*9九宫格切割为9个3*3九宫格，对数字num所在九宫格中的数字进行重复判断
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True
# 判明数独是否有解
def solve_sudoku(board):
    if not is_valid_sudoku(board):  # 如果当前数独不合法，直接返回 False
        return False
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                # 调用函数，从1~9尝试填入数字，判断是否可以填入，如果可以填入，再递归调用solve函数，判明数独是否有解
                for num in range(1, 10):
                    if could_place(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True
# 生成数独答案
def generate_sudoku():
    # 初始化一个空的9*9二维列表
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

difficulty_mapping = {
    "新手": 8,
    "简单": 7,
    "一般": 6,
    "中等": 5,
    "困难": 4,
    "专家": 3
}
# 获取固定的数独
# 通过对答案挖空生成数独题目
# 设置一个随机数，在挖空的时候对每个空判断随机数，如果小于等于所设难度等级，则保留数字，否则挖空为0
# 根据概率学 难度为9挖空10%，难度为8挖空20%，以此类推,
def get_fixed_sudoku(board, level):
    fixed_board = [[val if random.randint(1, 10) <= level else 0 for val in row] for row in board]
    return fixed_board

# 多线程生成数独谜题和答案的主要函数
def generate_sudoku_puzzle(level,thread_number):
    puzzles = []
    solutions = []
    solvetest=[]
    diff= difficulty_mapping.get(level,4)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(thread_number):
            future = executor.submit(generate_sudoku)
            puzzle=get_fixed_sudoku(future.result(), diff)
            puzzles.append(copy.deepcopy(puzzle))
            # print("puzzle1",puzzle)
            solutions.append(future.result())
            solve_sudoku(puzzle)
            # print("puzzle2",puzzle)
            solvetest.append(puzzle)
            # print("puzzle3",puzzles)
            
    return puzzles, solutions ,solvetest

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
#检查答案
def check_answer(board):
    # 将答案的一行取出来 检查行是否符合要求
    for row in board:
        if not is_valid_row(row):
            return False
    # 检查列是否符合要求
    for col in range(9):
        # 将答案的一列取出来 检查是否符合要求
        column = [board[row][col] for row in range(9)]
        if not is_valid_row(column):
            return False
    # 检查每个3x3的子区域是否符合要求
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if not is_valid_row(subgrid):
                return False
    return True

#检查数独一行或者一列的合法性
def is_valid_row(row):
    # 创建一个空集合
    seen = set()
    for num in row:
        if num == 0:
            return False  # 存在数字为0，返回False
        if num in seen:
            return False
        seen.add(num)
    return True

#检查整个数独棋盘的合法性
def is_valid_sudoku(board):
    # 检查行
    for row in range(9):
        nums = [0] * 10
        for col in range(9):
            num = board[row][col]
            if num != 0:
                if nums[num]:
                    return False
                nums[num] = 1
    # 检查列
    for col in range(9):
        nums = [0] * 10
        for row in range(9):
            num = board[row][col]
            if num != 0:
                if nums[num]:
                    return False
                nums[num] = 1
    # 检查九宫格
    for i in range(3):
        for j in range(3):
            nums = [0] * 10
            for row in range(i * 3, (i + 1) * 3):
                for col in range(j * 3, (j + 1) * 3):
                    num = board[row][col]
                    if num != 0:
                        if nums[num]:
                            return False
                        nums[num] = 1
    return True

def check_and_tip(puzzle,user_answer):
    blank = []
    false_map=[]
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:  # 判断是否为空格
                blank.append([i, j])  # 将空格的横纵坐标添加到blank列表中
    for coord in blank:
        x = coord[0]
        y = coord[1]
        flag = 0
        # 检查空格处所填数字的合法性
        # 检查行合法性
        for col in range(9):
            if user_answer[x][col] == user_answer[x][y] and col != y:
                false_map.append([x, y])
                flag = 1
                break
        if flag == 1:
            continue
        
        # 检查列合法性
        for row in range(9):
            if user_answer[row][y] == user_answer[x][y] and row != x:
                false_map.append([x, y])
                flag = 1
                break
        if flag == 1:
            continue

        # 检查九宫格合法性
        row_start = (x // 3) * 3
        col_start = (y // 3) * 3
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if user_answer[row][col] == user_answer[x][y] and row != x and col != y:
                    false_map.append([x, y])
                    flag = 1
                    break
            if flag == 1:
                break
    return false_map





def main():
    # 生成数独谜题和答案，并显示
    sudoku_puzzles, sudoku_solutions ,solvetest= generate_sudoku_puzzle(4,9)
    for puzzle, solution ,solve in zip(sudoku_puzzles, sudoku_solutions ,solvetest):
        print("数独谜题：")
        print(puzzle)
        display_sudoku(puzzle)
        print("答案：")
        display_sudoku(solution)
        print("jieda:")
        display_sudoku(solve)
        print()
if __name__ == "__main__":
    main()