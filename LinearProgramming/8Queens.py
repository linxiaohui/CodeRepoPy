from pulp import *

# 棋盘行、列编号
Rows = [str(i) for i in range(1,9)]
Cols = [str(i) for i in range(1,9)]

# 对角线上的行列编号
Diagonals = []
for r in range(1,8):
    c = 1
    i = 0
    diag = [(str(r),str(c))]
    while r+i<8:
        i+=1
        diag.append((str(r+i),str(c+i)))
    Diagonals.append(diag)

for c in range(2,8):
    r = 1
    i = 0
    diag = [(str(r),str(c))]
    while c+i<8:
        i+=1
        diag.append((str(r+i),str(c+i)))
    Diagonals.append(diag)

for r in range(1,8):
    c = 8
    i = 0
    diag = [(str(r),str(c))]
    while r+i<8:
        i+=1
        diag.append((str(r+i),str(c-i)))
    Diagonals.append(diag)

for c in range(2,8):
    r = 1
    i = 0
    diag = [(str(r),str(c))]
    while c-i>1:
        i+=1
        diag.append((str(r+i),str(c-i)))
    Diagonals.append(diag)

prob = LpProblem("8 Queens", LpMinimize)

chess_board = LpVariable.dicts("chess_board", (Rows,Cols),0,1,LpInteger)

prob += 0, "Arbitrary Objective Function"
# 每行只有一个Queen
for r in Rows:
    prob += lpSum([chess_board[r][c] for c in Cols]) == 1, ""
# 每列只有一个Queen
for c in Cols:
    prob += lpSum([chess_board[r][c] for r in Rows]) == 1, ""
# 每条对角线`最多`只有一个Queen
for diag in Diagonals:
    prob += lpSum([chess_board[r][c] for r,c in diag]) <= 1, ""

prob.writeLP("8Queens.lp")

def print_chess_board(board):
    for i in Rows:
        for j in Cols:
            print(int(value(board[i][j])),end=' ')
        print()

solution_cnt = 0

while True:
    prob.solve()
    #print("Status:", LpStatus[prob.status])
    if LpStatus[prob.status] == "Optimal":
        #print_chess_board(chess_board)
        solution_cnt += 1
        prob += lpSum([chess_board[r][c] for r in Rows
                                         for c in Cols
                                         if value(chess_board[r][c])==1]) <= 7
    else:
        print("ALL",solution_cnt, "Solutions")
        break
