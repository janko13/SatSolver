### SATSolver

#### Run
Move to directory with solver.py and run
```bash
python3 solver.py data/nqueens55.txt data/nqueens55_solution.txt <heuristics: rnd (default) or most_common>
```

Example:

```bash
python3 solver.py data/nqueens55.txt data/nqueens55_solution.txt rnd
```

Random heuristics works faster than picking most common variable.