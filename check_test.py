#检查答案
def is_valid_sudoku(board):
    # 将答案的一行取出来 检查行是否符合要求
    for row in board:
        if not is_valid_row(row):
            return False

    # 检查列是否符合要求
    for col in range(9):
        #将答案的一列取出来 检查是否符合要求
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

def is_valid_row(row):
    #创建一个空集合
    seen = set()
    for num in row:
        if num != 0:
            if num in seen:
                return False
            seen.add(num)
    return True

board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]
print(is_valid_sudoku(board))