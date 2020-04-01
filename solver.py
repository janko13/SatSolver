import sys
import random
import numpy as np
import time

from collections import Counter


def read_dimac(file):
    formula = []
    with open(file, 'r') as f:
        for line in f:
            data = line.split()
            if data[0] == 'c':
                continue
            if data[0] == 'p':
                num_var = int(data[2])
                continue
            formula.append(list(map(int, data[:-1])))
    return formula, num_var


def bcp(formula, unit):
    simplified = []
    for clause in formula:
        if unit not in clause:
            if -unit in clause:
                if len(clause) == 1:
                    return False, []
                simplified.append([lit for lit in clause if lit != -unit])
            else:
                simplified.append(clause)

    return True, simplified


def freq(formula):
    return Counter([literal for clause in formula for literal in clause])


def show(formula):
    """ Prints each clause in a new line. """
    for clause in formula:
        print(clause)


def get_first_unit(formula):
    for clause in formula:
        if len(clause) == 1:
            return clause
    return []


def propagate(formula):
    unique = set([literal for clause in formula for literal in clause])
    conditions = [literal for literal in unique if -literal not in unique]
    for pure in conditions:
        _, formula = bcp(formula, pure)

    while True:
        unit = get_first_unit(formula)
        if not unit:
            break
        flag, formula = bcp(formula, *unit)
        conditions.extend(unit)
        if flag == False:
            return False, [], []
        if not formula:
            return True, formula, conditions

    return True, formula, conditions


def dpll(formula, conditions):
    """ Backtracking part """
    flag, formula, conds = propagate(formula)
    conditions.extend(conds)

    if not flag:
        return []
    if not formula:
        return conditions

    var = select_var(formula, heuristic='rnd')
    cond_pos = [c for c in conditions]
    cond_pos.append(var)
    solution = dpll(bcp(formula, var)[1], cond_pos)
    if not solution:
        cond_neg = [c for c in conditions]
        cond_neg.append(-var)
        solution = dpll(bcp(formula, -var)[1], cond_neg)
    return solution


def select_var(formula, heuristic='rnd'):
    f = freq(formula)
    if heuristic == 'most_common':
        return f.most_common(1)[0][0]
    return random.choice(list(f.keys()))


def check_correctness(formula, solution):
    for clause in formula:
        sol = False
        for literal in clause:
            # trenutnemu rezultatu ali ne (negaciaj) xor (vrednost clena)
            sol = sol or not ((literal > 0) ^ (solution[np.absolute(literal) - 1] > 0))
        if not sol:
            break
    return sol


if __name__ == '__main__':
    verbose = True
    output_file = sys.argv[2]
    heuristics = 'rnd'
    if len(sys.argv) == 4:
        heuristics = sys.argv[3]
    formula, num_var = read_dimac(sys.argv[1])
    s = time.time()
    solution = dpll(formula, [])
    # print("ELAPSED TIME", time.time() - s)

    if not solution:
        raise ValueError("Not satisfiable")

    solution.sort(key=lambda x: abs(x))
    # print("Number of true variables", len([x for x in solution if x > 0]))

    str_sol = ' '.join([str(x) for x in solution])
    # if verbose:
    #     print("SOLUTION", check_correctness(formula, solution))
    #     print(str_sol)

    # write solution to file
    with open(output_file, 'w') as out:
        out.write(str_sol)
