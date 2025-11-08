# scipy.optimize Conversion - Quick Start Guide

This guide helps you get started with the scipy.optimize versions of the optimization notebooks.

## What Changed?

The main optimization notebooks have been converted from using **Gurobi** (commercial solver) to **scipy.optimize** (open-source). This makes the code:
- Free and open-source
- Easy to install and use
- Great for learning and education
- Compatible with standard Python scientific stack

## Installation

Install the required packages:

```bash
pip install scipy numpy pandas matplotlib
```

For the Index_Tracking notebook, also install:

```bash
pip install yfinance scikit-learn sktime fastparquet pyarrow
```

Or install everything from requirements.txt:

```bash
pip install -r requirements.txt
```

## Testing the Conversion

Run the test suite to verify everything works:

```bash
python3 test_scipy_conversion.py
```

Expected output:
```
🎉 All tests passed successfully!
Test Results: 7 passed, 0 failed
```

## Converted Notebooks

### 1. Solving_problems_using_Python.ipynb

**What it covers:**
- Linear programming with scipy.optimize.linprog
- Factory production problems
- Assignment and transportation problems
- Scalable formulations

**Quick example:**
```python
import numpy as np
from scipy.optimize import linprog

# Maximize 40*chairs + 50*tables
c = [-40, -50]  # Negate for maximization

# Constraints: wood and labor
A_ub = [[1, 2],   # wood
        [4, 3]]   # labor
b_ub = [40, 120]

# Solve
result = linprog(c, A_ub=A_ub, b_ub=b_ub, 
                 bounds=[(0, None), (0, None)], 
                 method='highs')

print(f"Chairs: {result.x[0]:.1f}")
print(f"Tables: {result.x[1]:.1f}")
print(f"Revenue: ${-result.fun:.1f}")
```

### 2. Index_Tracking.ipynb

**What it covers:**
- Portfolio optimization using scipy.optimize.minimize
- Tracking error minimization
- Data fetching from Yahoo Finance
- Visualization of results

**Quick example:**
```python
from scipy.optimize import minimize

def tracking_error(weights, returns, market_returns):
    portfolio_returns = returns @ weights
    errors = portfolio_returns - market_returns
    return np.sum(errors ** 2)

# Optimize
result = minimize(
    tracking_error,
    initial_weights,
    args=(stock_returns, market_returns),
    method='SLSQP',
    bounds=[(0, 1)]*n_assets,
    constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
)
```

## Key Differences from Gurobi

### Maximization vs Minimization

**Gurobi:**
```python
m.setObjective(40*x1 + 50*x2, GRB.MAXIMIZE)
```

**scipy:**
```python
c = [-40, -50]  # Negate coefficients
result = linprog(c, ...)  # Always minimizes
revenue = -result.fun  # Negate result
```

### Constraints

**Gurobi:**
```python
m.addConstr(8*x1 + 6*x2 >= 48)  # >= directly supported
m.addConstr(x1 + x2 == 10)      # == directly supported
```

**scipy:**
```python
# >= constraint: negate both sides for <=
A_ub = [[-8, -6]]
b_ub = [-48]

# == constraint: use A_eq and b_eq
A_eq = [[1, 1]]
b_eq = [10]
```

### Accessing Results

**Gurobi:**
```python
for v in m.getVars():
    print(v.varName, v.x)
print('Objective:', m.objVal)
```

**scipy:**
```python
print('Variables:', result.x)
print('Objective:', result.fun)
print('Success:', result.success)
```

## Limitations

1. **No Integer Programming**: scipy doesn't support integer or binary variables. For integer programming, consider using:
   - PuLP (free, open-source)
   - python-mip (free, open-source)
   - CVXPY (free, supports multiple solvers)

2. **Limited Sensitivity Analysis**: scipy provides basic dual values but not the detailed sensitivity ranges that Gurobi provides.

3. **Large-Scale Problems**: For very large problems (thousands of variables), commercial solvers may be faster.

## Documentation

See `CONVERSION_SUMMARY.md` for detailed technical documentation including:
- Complete conversion patterns
- All test results
- Detailed API comparisons
- References to scipy documentation

## Getting Help

If you encounter issues:

1. Check that scipy is installed: `python -c "import scipy; print(scipy.__version__)"`
2. Run the test suite: `python test_scipy_conversion.py`
3. Review the CONVERSION_SUMMARY.md for detailed examples
4. Check scipy documentation: https://docs.scipy.org/doc/scipy/reference/optimize.html

## License

This code is open-source and free to use for educational purposes.
