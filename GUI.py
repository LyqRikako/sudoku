import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from functools import partial
import sudoku
# 更新数独显示
def update_sudoku_display(idx):
    for i in range(9):
        for j in range(9):
            if puzzles[idx][i][j] == 0:
                entries[idx][i][j].delete(0, tk.END)
            else:
                entries[idx][i][j].delete(0, tk.END)
                entries[idx][i][j].insert(0, str(puzzles[idx][i][j]))
                if entries[idx][i][j]['bg'] != '#fffacd':
                    entries[idx][i][j].config(bg='#fff')
    update_gray_cells(idx)
#切换数独题目
def switch_sudoku(event):
    global notebook
    idx = int(notebook.index(notebook.select()))
    update_sudoku_display(idx)
# 函数：高亮格子并绑定数字选择事件
def highlight_cell(row, col):
    global current_selected_cell
    global current_thread
    current_thread = notebook.index(notebook.select())
    # Reset previous highlight
    if current_selected_cell:
        entries[current_selected_cell[0]][current_selected_cell[1]][current_selected_cell[2]].config(bg='#fff')
    # Set new highlight
    entries[current_thread][row][col].config(bg='#e6e6fa')
    current_selected_cell = (current_thread, row, col)
# 用于更新非空白格子的背景色
def update_gray_cells(thread_idx):
    for row in range(9):
        for col in range(9):
            if puzzles[thread_idx][row][col] != 0:
                entries[thread_idx][row][col].config(bg='#fffacd')
def init_white_cells():
    global entries
    for idx in range(len(entries)):
        for row in range(9):
            for col in range(9):
                entries[idx][row][col].config(bg='#fff')
# 生成界面
def generate_interface(thread_count):
    global notebook
    global entries
    global current_thread
    global current_selected_cell
    root = tk.Tk()
    root.title("数独趣多多")
    # 创建标签页
    notebook = ttk.Notebook(root)
    notebook.pack(side='right', padx=10, pady=10)
    for i in range(thread_count):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=f"{i + 1}")
        # 为存储 Entry 对象的子列表初始化为空列表
        entry_row = []
        for row in range(9):
            entry_row.append([])
            for col in range(9):
                entry = tk.Entry(frame, width=2, font=("Arial", 15))
                entry.grid(row=row, column=col)
                entry.bind('<Button-1>', lambda e, row=row, col=col: (highlight_cell(row, col),on_cell_click(solutions,row, col)))
                entry_row[row].append(entry)
        # 将 Entry 对象列表添加到 entries
        entries.append(entry_row)
    current_selected_cell = None
    current_thread = 0
    # 更新数独显示
    switch_sudoku(None)
    # 绑定事件
    notebook.bind("<<NotebookTabChanged>>", switch_sudoku)
    # 创建难度选择部分
    difficulty_frame = ttk.Frame(root)
    difficulty_frame.pack(side="top", padx=20, pady=20)
    # 难度选择标签
    ttk.Label(difficulty_frame, text="难度选择").grid(row=0, column=0, columnspan=3, pady=(0, 10))
    # 难度选择按钮
    difficulty_buttons = {}
    for idx, difficulty in enumerate(["新手", "简单", "一般", "中等", "困难"]):
        difficulty_buttons[difficulty] = tk.Button(difficulty_frame, text=difficulty, width=8,
                                                   command=partial(change_difficulty, difficulty, thread_number))
        difficulty_buttons[difficulty].grid(row=1 + idx // 3, column=idx % 3, padx=5, pady=5)
    # 数字选择部分
    number_frame = ttk.Frame(root)
    number_frame.pack(side="right", padx=20, pady=20)
    ttk.Label(number_frame, text="数字选择").grid(row=0, column=0, columnspan=3, pady=(0, 10))
    for i in range(3):
        for j in range(3):
            button_number = i * 3 + j + 1
            button = tk.Button(number_frame, text=str(button_number), width=8, command=partial(select_number, button_number))
            button.grid(row=i + 1, column=j, padx=5, pady=5)
    # 添加显示答案按钮
    show_answer_button = tk.Button(number_frame, text="显示答案", width=8, command=partial(show_answer, root))
    show_answer_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
    # 添加显示已完成数独的按钮
    show_completed_button = tk.Button(number_frame, text="提交答案", width=12, command=show_completed_sudoku)
    show_completed_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    # 提示按钮
    # button_get_cell = tk.Button(root, text="获取选中空白单元格", command=get_selected_cell())
    # button_get_cell.pack(side="bottom", padx=20, pady=10)
    init_white_cells()
    update_gray_cells(current_thread)
    root.mainloop()
def on_cell_click(solutions,row, col):
    print(f"选中的空白单元格：行{row + 1}，列{col + 1}")
    print(solutions[0][0])
# def get_selected_cell():
#
#     print(f"当前选中的空白单元格：行{x + 1}，列{y + 1}")
def change_difficulty(difficulty, thread_number):
    global current_difficulty
    global puzzles
    global solutions
    current_difficulty = difficulty
    # 生成新的数独题目
    global current_thread
    current_thread = notebook.index(notebook.select())
    puzzles , solutions = sudoku.generate_sudoku_puzzle(difficulty,thread_number)
    # 更新数独显示
    switch_sudoku(None)
    messagebox.showinfo("提示", f"已切换难度为 {difficulty}")
    # 更新非空白格子的背景色
    init_white_cells()
    update_gray_cells(current_thread)
# 函数：选择数字
def select_number(number):
    global current_thread
    global current_selected_cell
    if current_selected_cell:
        entries[current_selected_cell[0]][current_selected_cell[1]][current_selected_cell[2]].delete(0, tk.END)
        entries[current_selected_cell[0]][current_selected_cell[1]][current_selected_cell[2]].insert(0, str(number))
        current_selected_cell = None
#显示答案
def show_answer_grid(answer, root):
    answer_window = tk.Toplevel()
    answer_window.title("答案")
    for i in range(9):
        for j in range(9):
            entry = tk.Entry(answer_window, width=2, font=("Arial", 18), justify="center", bd=2, relief="solid")
            entry.grid(row=i, column=j)
            entry.insert(0, str(answer[i][j]))
            entry.configure(state='readonly')
    answer_window.geometry(f"+{root.winfo_x() + notebook.winfo_width() + 30}+{root.winfo_y()}")
def show_answer(root):
    global current_thread
    # 获取当前选定的数独索引
    idx = int(notebook.index(notebook.select()))
    show_answer_grid(solutions[idx], root)
def show_completed_sudoku():
    # 获取当前选定的数独索引
    idx = int(notebook.index(notebook.select()))
    # 获取已完成的数独
    completed_sudoku = get_completed_sudoku(idx)
    print(completed_sudoku)
    if sudoku.is_valid_sudoku(completed_sudoku):
        messagebox.showinfo("提示", "恭喜你，答案正确！")
    else:
        messagebox.showinfo("提示", "很遗憾，答案错误！")
def get_completed_sudoku(thread_idx):
    completed_sudoku = []
    for i in range(9):
        row = []
        for j in range(9):
            entry = entries[thread_idx][i][j]
            value = entry.get()
            if value:
                row.append(int(value))
            else:
                row.append(0)
        completed_sudoku.append(row)
    return completed_sudoku
# 例子使用：生成9个数独题目和答案
thread_number = 9
level=4
puzzles , solutions = sudoku.generate_sudoku_puzzle(level,thread_number)
# 存储界面中的所有Entry
entries = []
# 生成界面
generate_interface(thread_number)