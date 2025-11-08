# Conversion Summary: Gurobi to scipy.optimize

This document summarizes the conversion of optimization code from Gurobi to scipy.optimize and numpy.

## Files Converted

### 1. Solving_problems_using_Python.ipynb
**Original:** Used Gurobi for linear programming examples  
**Converted to:** scipy.optimize.linprog

#### Examples Converted:
- **Factory Production Problem**: Maximize revenue subject to resource constraints
  - Decision variables: chairs and tables
  - Constraints: wood and labor
  - Result: 24 chairs, 8 tables, revenue $1360

- **Scalable Formulations**: Using dictionaries and list comprehensions
  - Demonstrates how to build constraint matrices programmatically
  - Added packaging constraint example
  - Added new product (bench) example

- **Problem C2Q1**: Maximization with inequality constraints
  - Result: x0=4.0, x1=0.0, objective=40.0

- **Problem C2Q2**: Minimization with >= constraints  
  - Result: x0=0.0, x1=8.0, objective=0.24

- **Problem C4Q8**: 3-variable minimization
  - Result: x0=2.0, x1=3.0, x2=0.0, objective=17.0

- **Problem C4Q32**: Assignment problem (9 variables, equality constraints)
  - Result: objective=70.0

- **Problem C4Q33**: Transportation problem (4 variables, equality constraints)
  - Result: objective=24000.0

### 2. Index_Tracking.ipynb
**Original:** Used Gurobi for portfolio optimization  
**Converted to:** scipy.optimize.minimize with SLSQP method

#### Models Implemented:
- **Unconstrained Model**: Minimize tracking error with all available assets
  - Downloads S&P 100 stock data from Yahoo Finance
  - Calculates optimal weights to track index
  - Constraints: weights sum to 1, all weights >= 0

- **Asset-Constrained Model**: Limit portfolio to K assets
  - Uses greedy selection: picks top K assets from unconstrained solution
  - Re-optimizes with only selected assets
  - Default K=10 assets

### 3. requirements.txt
**Removed:** gurobipy  
**Added:** scipy, pandas, yfinance, scikit-learn, sktime, fastparquet, pyarrow

## Conversion Approach

### Linear Programming (scipy.optimize.linprog)

**Gurobi Format:**
```python
from gurobipy import *
m = Model()
x1 = m.addVar(lb=0, vtype=GRB.CONTINUOUS)
x2 = m.addVar(lb=0, vtype=GRB.CONTINUOUS)
m.setObjective(40*x1 + 50*x2, GRB.MAXIMIZE)
m.addConstr(x1 + 2*x2 <= 40)
m.addConstr(4*x1 + 3*x2 <= 120)
m.optimize()
```

**scipy Format:**
```python
import numpy as np
from scipy.optimize import linprog

# Negate coefficients for maximization (linprog minimizes)
c = [-40, -50]

# Inequality constraints: A_ub @ x <= b_ub
A_ub = [[1, 2], [4, 3]]
b_ub = [40, 120]

# Variable bounds
bounds = [(0, None), (0, None)]

# Solve
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
print(f"Optimal value: {-result.fun}")  # Negate back for maximization
```

### Key Differences:

1. **Objective Direction**:
   - Gurobi: Can minimize or maximize (specify with GRB.MINIMIZE or GRB.MAXIMIZE)
   - scipy: Always minimizes (negate coefficients for maximization)

2. **Constraints**:
   - Gurobi: Supports <=, >=, == directly
   - scipy: 
     - <= constraints: use A_ub and b_ub
     - >= constraints: negate both sides to convert to <=
     - == constraints: use A_eq and b_eq

3. **Results Access**:
   - Gurobi: `var.x` for variable value, `model.objVal` for objective
   - scipy: `result.x` for variables, `result.fun` for objective

4. **Sensitivity Analysis**:
   - Gurobi: Provides detailed sensitivity ranges, shadow prices, reduced costs
   - scipy: Limited sensitivity information (duals may be available depending on method)

### Quadratic Programming (scipy.optimize.minimize)

**For tracking error minimization:**
```python
def tracking_error(weights, returns, market_returns):
    portfolio_returns = returns @ weights
    errors = portfolio_returns - market_returns
    return np.sum(errors ** 2)

# Constraints
constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}

# Bounds
bounds = [(0, 1) for _ in range(n_assets)]

# Solve
result = minimize(
    tracking_error,
    w0,
    args=(returns, market_returns),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)
```

## Testing

All converted examples have been tested and produce correct results:

```
✅ Factory Problem: Revenue $1360 (24 chairs, 8 tables)
✅ Scalable Formulation: Revenue $1360
✅ Bench Addition: Revenue $1360 (bench production = 0)
✅ C2Q1: Objective 40.0
✅ C2Q2: Objective 0.24
✅ C4Q8: Objective 17.0
✅ C4Q32: Objective 70.0
✅ C4Q33: Objective 24000.0
```

## Limitations

1. **Integer Programming**: scipy.optimize does not support integer or binary variables. The Integer_Programming.ipynb notebook was not converted as it requires MILP capabilities.

2. **Sensitivity Analysis**: scipy provides limited sensitivity information compared to commercial solvers like Gurobi. For production use requiring detailed sensitivity analysis, consider using CVXPY or PuLP which provide more complete interfaces.

3. **Performance**: For very large-scale problems, commercial solvers may be significantly faster. scipy is excellent for small to medium-sized problems.

4. **Solver Options**: scipy.optimize.linprog uses HiGHS by default, which is an open-source solver. Other methods available: 'highs-ds', 'highs-ipm', 'interior-point', 'revised simplex', 'simplex'.

## Benefits of Conversion

1. **Open Source**: No licensing costs or restrictions
2. **Widely Available**: scipy is a standard scientific Python library
3. **Integration**: Works seamlessly with numpy, pandas, and other scientific Python tools
4. **Educational**: Good for learning and teaching optimization concepts

## Notes

- The output values may differ slightly from Gurobi due to different numerical algorithms and tolerances
- This is expected and acceptable for educational purposes
- For production applications requiring exact reproducibility, additional testing and validation is recommended

## References

- scipy.optimize documentation: https://docs.scipy.org/doc/scipy/reference/optimize.html
- scipy.optimize.linprog: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
- scipy.optimize.minimize: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
