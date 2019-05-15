from pulp import *

prob = LpProblem("Bai Ji Bai Qian", LpMinimize)
prob += 0

GongJi = LpVariable("GongJi", 0, None, LpInteger)
MuJi = LpVariable("MuJi", 0, None, LpInteger)
XiaoJi = LpVariable("XiaoJi", 0, None, LpInteger)

prob += lpSum([GongJi, MuJi, XiaoJi])==100, "A"
prob += lpSum([15*GongJi, 9*MuJi, XiaoJi])==300, "B"

prob.writeLP("problem.lp")

prob.solve()
print("Status:", LpStatus[prob.status])
print(value(GongJi))
print(value(MuJi))
print(value(XiaoJi))


# https://www.aiexp.info/calculating-all-feasible-solutions-of-ilp.html
'''
With SCIP, all feasible solutions of "problem.lp" can be calculated easily in the following steps:
SCIP> read problem.lp
SCIP> set emphasis counter
SCIP> set constraints countsols collect TRUE
SCIP> count
SCIP> write allsolutions chicken_sol.txt
'''