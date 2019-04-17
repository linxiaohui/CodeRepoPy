# -*- coding: UTF-8 -*-

import sys
import itertools
import pulp

def SolveSudoku(sudoku):
    '''
    sudoku: (行,列,值) 的list, 表明初始状态. 行、列、值 均为 "1"-"9"的字符
    '''
    ROWS = COLUMNS = VALUES = [str(i) for i in range(1,10)]
    # 构建3*3个Box的(行、列)
    BOXES = []
    landmarker = list(zip(*[iter(range(0,9))]*3))
    for r in landmarker:
        for c in landmarker:
            BOXES.append([(ROWS[i],COLUMNS[j]) for i,j in itertools.product(r,c)])
    prob = pulp.LpProblem("SudokuSolver", pulp.LpMaximize)
    # 生成一个变量的字典，便于使用行、列、值获取变量
    pvardict = pulp.LpVariable.dicts("position", (ROWS,COLUMNS,VALUES), 0, 1, cat=pulp.LpInteger)
    # 设置目标函数, 该问题不需要`优化目标`
    prob += 0, ""
    # 设置限制
    for r in ROWS:
        for c in COLUMNS:
            prob += pulp.lpSum([pvardict[r][c][v] for v in VALUES]) == 1, '每个格子只有一个数'+r+c
    for r in ROWS:
        for v in VALUES:
            prob += pulp.lpSum([pvardict[r][c][v] for c in COLUMNS]) == 1, '每个数字在每一行只有一个'+r+v
    for c in COLUMNS:
        for v in VALUES:
            prob += pulp.lpSum([pvardict[r][c][v] for r in ROWS]) == 1, '每个数字在每一列只有一个'+c+v
    for b in BOXES:
        for v in VALUES:
            prob += pulp.lpSum([pvardict[r][c][v] for r,c in b]) == 1, '每个BOX中每个数字只有一个'+str(b)+v
    # 初始状态
    for r,c,v in sudoku:
        prob += pvardict[r][c][v] == 1,'初始状态'+r+c+v
    
    prob.writeLP("Sudoku.lp")
    prob.solve()

    print(pulp.LpStatus[prob.status])
    return pvardict

#sudokuout = open('sudokuout.txt','w')
sudokuout = sys.stdout

def SudokuPrint(choice):
    ROWS = COLUMNS = VALUES = [str(i) for i in range(1,10)]
    for r in ROWS:
        if r in ["1","4","7"]:
            sudokuout.write("+-------+-------+-------+\n")
        for c in COLUMNS:
            for v in VALUES:
                if pulp.value(choice[r][c][v])==1:
                    if c == "1" or c == "4" or c =="7":
                        sudokuout.write("| ")
                    sudokuout.write(v + " ")
                    if c == "9":
                        sudokuout.write("|\n")
    sudokuout.write("+-------+-------+-------+\n\n")

if __name__ == '__main__':
    # SUDOKU
    SUDOKU=[("1","2","1"),
            ("1","3","6"),
            ("1","4","9"),
            ("1","6","4"),
            ("1","7","5"),
            ("2","2","7"),
            ("2","6","5"),
            ("2","7","1"),
            ("2","8","4"),
            ("3","9","9"),
            ("4","1","3"),
            ("4","3","4"),
            ("4","5","1"),
            ("4","7","7"),
            ("4","8","9"),
            ("5","1","9"),
            ("5","9","3"),
            ("6","2","2"),
            ("6","3","1"),
            ("6","5","3"),
            ("6","7","4"),
            ("6","9","6"),
            ("7","1","1"),
            ("8","2","3"),
            ("8","3","7"),
            ("8","4","6"),
            ("8","8","2"),
            ("9","3","8"),
            ("9","4","2"),
            ("9","6","1"),
            ("9","7","3"),
            ("9","8","5")]
    
    v = SolveSudoku(SUDOKU)
    SudokuPrint(v)
