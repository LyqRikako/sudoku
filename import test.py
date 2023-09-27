from test import could_place
def number_of_solve_sudoku(board):
    global count
    count =0
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                #调用函数，从1~9尝试填入数字，判断是否可以填入，如果可以填入，再递归调用solve函数，判明数独是否有解
                for num in range(1, 10):
                    if could_place(board, row, col, num):
                        board[row][col] = num
                        if number_of_solve_sudoku(board):
                            count+=1
                            if(count>1):
                                print("hello")
                                return "False"
                            return True
                        board[row][col] = 0
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                #调用函数，从1~9尝试填入数字，判断是否可以填入，如果可以填入，再递归调用solve函数，判明数独是否有解
                for num in range(1, 10):
                    if could_place(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            print("hello")
                            return True
                        board[row][col] = 0
                return False
    return True



import numpy as np
board = np.array([[0, 3, 6, 4, 2, 7, 9, 8, 5], [0, 5, 4, 9, 6, 3, 7, 1, 2], [0, 2, 9, 1, 5, 8, 3, 4, 6], [4, 6, 5, 7, 8, 1, 2, 9, 3], [2, 8, 3, 6, 9, 5, 4, 7, 1], [1, 9, 8, 2, 3, 6, 5, 4, 7], [6, 4, 2, 5, 1, 9, 8, 3, 7], [3, 1, 7, 8, 4, 2, 6, 5, 9], [9, 7, 1, 3, 6, 4, 5, 2, 8]])
count=0
bool=solve_sudoku(board,count)
print(bool)
