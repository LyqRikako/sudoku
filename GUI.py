import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from functools import partial
import sudoku
# 生成界面
def generate_GUI(thread_number):
    global notebook
    global entries
    global current_thread
    global selected_block
    root = tk.Tk()
    root.title("数独趣多多")
    # 创建标签页部分
    notebook = ttk.Notebook(root)
    notebook.pack(side='right', padx=10, pady=10)
    for i in range(thread_number):
        sudoku_frame = ttk.Frame(notebook)
        notebook.add(sudoku_frame, text=f"{i + 1}")
        entry_row = []
        for row in range(9):
            entry_row.append([])
            for col in range(9):
                entry = tk.Entry(sudoku_frame, width=2, font=("Arial", 15))
                entry.grid(row=row, column=col)
                entry.bind('<Button-1>', lambda e, row=row, col=col: (set_insert_color(row, col),on_cell_click(solutions,row, col)))
                entry_row[row].append(entry)
        entries.append(entry_row)
    selected_block = None
    current_thread = 0
    # 创建主界面部分
    main_frame = ttk.Frame(root)
    main_frame.pack(pady=20)
    sudoku_frame = ttk.Frame(main_frame)
    sudoku_frame.pack(side="top")
    # 创建难度选择和数字选择的父容器
    choices_frame = ttk.Frame(main_frame)
    choices_frame.pack(side="top", padx=20)
    # 创建难度选择部分
    difficulty_frame = ttk.Frame(choices_frame)
    difficulty_frame.pack()
    # 创建数字选择部分
    number_frame = ttk.Frame(choices_frame)
    number_frame.pack(pady=20)
    # 创建答案按钮部分
    solution_frame = ttk.Frame(choices_frame)
    solution_frame.pack(side="top", padx=20, pady=20)
    style = ttk.Style()
    style.map("TButton",
              foreground=[('pressed', 'white'), ('active', 'white')],
              background=[('pressed', '!disabled', 'blue'), ('active', 'green')])
    # 更新数独显示
    switch_puzzle(None)
    # 切换9道数独题目
    notebook.bind("<<NotebookTabChanged>>", switch_puzzle)
    # 添加难度选择按钮
    colors = ["#C5E1A5", "#E6EE9C", "#FBC02D", "#FF6F00", "#E64A19", "#DD2C00", "#FF1744"]
    ttk.Label(difficulty_frame, text="难度选择",font=("",15,"bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))
    button_difficulty = {}
    for idx, difficulty in enumerate(["新手", "简单", "一般", "中等", "困难","专家","自定义"]):
        button_difficulty[difficulty] = tk.Button(difficulty_frame, text=difficulty, width=8,
                                                   command=partial(selected_difficulty, difficulty, thread_number))
        button_difficulty[difficulty].configure(bg=colors[idx],fg="#000")
        button_difficulty[difficulty].grid(row=1 + idx // 3, column=idx % 3, padx=5, pady=5)
    # 添加数字选择按钮
    ttk.Label(number_frame, text="数字选择",font=("",15,"bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20))
    for i in range(3):
        for j in range(3):
            button_number = i * 3 + j + 1
            button = tk.Button(number_frame, text=str(button_number),width=8,command=partial(selected_number, button_number))
            button.configure(bg="#01579B",fg="#FFF")
            button.grid(row=i + 1, column=j, padx=5, pady=5)
    # 添加显示答案按钮
    buttonshow_answer = tk.Button(solution_frame, text="显示答案", width=12, command=partial(show_answer, root))
    buttonshow_answer.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
    buttonshow_answer.configure(bg="#80D8FF", fg="#000")
    # 添加提交答案按钮
    show_completed_button = tk.Button(solution_frame, text="提交答案", width=12, command=show_completed_sudoku)
    show_completed_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    show_completed_button.configure(bg="#80D8FF", fg="#000")
    # 添加提示答案按钮
    button_get_cell = tk.Button(solution_frame, text="提示答案", width=12,command=get_selected_cell)
    button_get_cell.configure(bg="#80D8FF", fg="#000")
    button_get_cell.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
    set_paper_color()
    set_ques_color(current_thread)
    root.mainloop()
# 更新数独显示
def update_display(idx):
    for i in range(9):
        for j in range(9):
            if puzzles[idx][i][j] == 0:
                entries[idx][i][j].delete(0, tk.END)
            else:
                entries[idx][i][j].delete(0, tk.END)
                entries[idx][i][j].insert(0, str(puzzles[idx][i][j]))
                if entries[idx][i][j]['bg'] != '#fffacd':
                    entries[idx][i][j].config(bg='#fff')
    set_ques_color(idx)
# 切换数独题目
def switch_puzzle(event):
    global notebook
    idx = int(notebook.index(notebook.select()))
    if idx < thread_number:
        update_display(idx)
# 设置输入框颜色
def set_insert_color(row, col):
    global selected_block
    global current_thread
    current_thread = notebook.index(notebook.select())
    # 重置背景白色
    if selected_block:
        entries[selected_block[0]][selected_block[1]][selected_block[2]].config(bg='#fff')
    # 输入框颜色
    entries[current_thread][row][col].config(bg='#e6e6fa')
    selected_block = (current_thread, row, col)
# 设置题目数字和背景色
def set_ques_color(thread_idx):
    for row in range(9):
        for col in range(9):
            if puzzles[thread_idx][row][col] != 0:
                entries[thread_idx][row][col].config(bg='#fffacd')
def set_paper_color():
    global entries
    for idx in range(len(entries)):
        for row in range(9):
            for col in range(9):
                entries[idx][row][col].config(bg='#fff')
# 提示按钮功能部分
selected_row = -1
selected_col = -1
def on_cell_click(solutions,row, col):
    global selected_row, selected_col
    selected_row = row
    selected_col = col
    print(f"选中的空白单元格：行{row + 1}，列{col + 1}")
    print(solutions[0][0])
def get_selected_cell():
    global selected_row, selected_col
    global selected_row, selected_col
    idx = int(notebook.index(notebook.select()))
    if selected_row >= 0 and selected_col >= 0:
        messagebox.showinfo("提示", f"该空答案为 {solutions[idx][selected_row][selected_col]}")
        print(f"当前选中的空白单元格：行{selected_row + 1}，列{selected_col + 1}")
    else:
        print("未选中任何空白单元格")
def selected_difficulty(difficulty, thread_number):
    global diff_chosen
    global puzzles
    global solutions
    global current_thread
    diff_chosen = difficulty
    # 生成新的数独题目
    current_thread = notebook.index(notebook.select())
    puzzles , solutions = sudoku.generate_sudoku_puzzle(difficulty,thread_number)
    # 更新数独并提示
    switch_puzzle(None)
    messagebox.showinfo("提示", f"已切换难度为 {difficulty}")
    # 更新颜色
    set_paper_color()
    set_ques_color(current_thread)
# 数字选择部分
def selected_number(number):
    global current_thread
    global selected_block
    if selected_block:
        entries[selected_block[0]][selected_block[1]][selected_block[2]].delete(0, tk.END)
        entries[selected_block[0]][selected_block[1]][selected_block[2]].insert(0, str(number))
        selected_block = None
# 显示答案部分
def show_answer_frame(answer, root):
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
    show_answer_frame(solutions[idx], root)
# 提示答案部分
def show_completed_sudoku():
    # 获取当前选定的数独索引
    idx = int(notebook.index(notebook.select()))
    # 获取已完成的数独
    completed_sudoku = get_completed_sudoku(idx)
    print(completed_sudoku)
    if sudoku.check_answer(completed_sudoku):
        messagebox.showinfo("提示", "恭喜你，答案正确！")
    else:
        messagebox.showinfo("提示", "很遗憾，答案错误！")
def get_completed_sudoku(idx):
    completed_sudoku = []
    for i in range(9):
        row = []
        for j in range(9):
            entry = entries[idx][i][j]
            value = entry.get()
            if value:
                row.append(int(value))
            else:
                row.append(0)
        completed_sudoku.append(row)
    return completed_sudoku
# 界面入口设置参数用以启动
thread_number = 9
level=4
puzzles , solutions = sudoku.generate_sudoku_puzzle(level,thread_number)
entries = []
generate_GUI(thread_number)