import unittest
import sudoku


class Test(unittest.TestCase):
    def test_check_answer(self):
        # 预期的结果
        ## 用于测试检查答案是否正确的功能，经过测试，功能正确
        board1 = [
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
        bool1 = sudoku.check_answer(board1)
        expected_bool1 = True # 预期的结果
        self.assertEqual(bool1, expected_bool1)  # 验证返回的内容是否与预期一致
    
    def test_solve_sudoku(self):
        ##测试检查数独是否有解的功能，经过测试，功能正确
        board2= [
            [5, 5, 0, 6, 0, 8, 9, 1, 2],
            [5, 7, 2, 0, 9, 5, 3, 4, 8],
            [0, 9, 0, 3, 0, 2, 5, 6, 7],
            [8, 5, 9, 7, 0, 1, 4, 2, 3],
            [0, 2, 6, 8, 0, 3, 7, 9, 0],
            [7, 1, 3, 9, 0, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 0, 8, 4],
            [2, 0, 7, 4, 1, 9, 6, 0, 5],
            [0, 4, 5, 2, 8, 6, 1, 7, 0]
        ]
        bool2 = sudoku.solve_sudoku(board2)
        expected_bool2 = False # 预期的结果
        self.assertEqual(bool2, expected_bool2)  # 验证返回的内容是否与预期一致

    def test_check_couldplace(self):
        # 预期的结果
        ## 用于测试检查答案是否正确的功能，经过测试，功能正确
        board3= [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [0, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        bool1 = sudoku.could_place(board3,1,0,4)
        expected_bool3 = False # 预期的结果
        self.assertEqual(bool1, expected_bool3)  # 验证返回的内容是否与预期一致

if __name__ == '__main__':
    unittest.main()