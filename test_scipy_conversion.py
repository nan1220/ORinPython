#!/usr/bin/env python3
"""
Test script to verify scipy.optimize conversions from Gurobi

This script runs all the converted optimization examples to ensure they
produce correct results.
"""

import numpy as np
from scipy.optimize import linprog, minimize
import sys

def test_factory_problem():
    """Test the basic factory production problem"""
    print("\n" + "="*60)
    print("TEST 1: Factory Production Problem")
    print("="*60)
    
    c = [-40, -50]  # Maximize 40*x1 + 50*x2
    A_ub = [[1, 2],   # wood constraint
            [4, 3]]   # labor constraint
    b_ub = [40, 120]
    bounds = [(0, None), (0, None)]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    print(f"Chairs: {result.x[0]:.1f}")
    print(f"Tables: {result.x[1]:.1f}")
    print(f"Revenue: ${-result.fun:.1f}")
    
    assert abs(result.x[0] - 24.0) < 0.1, "Chairs should be 24"
    assert abs(result.x[1] - 8.0) < 0.1, "Tables should be 8"
    assert abs(-result.fun - 1360.0) < 0.1, "Revenue should be $1360"
    
    print("✅ PASSED")
    return True

def test_c2q1():
    """Test problem C2Q1"""
    print("\n" + "="*60)
    print("TEST 2: Problem C2Q1 (Maximization)")
    print("="*60)
    
    c = [-10, -6]
    A_ub = [[3, 8], [45, 30]]
    b_ub = [20, 180]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None), (0, None)], method='highs')
    
    print(f"x0 = {result.x[0]:.1f}")
    print(f"x1 = {result.x[1]:.1f}")
    print(f"Objective = {-result.fun:.1f}")
    
    assert abs(-result.fun - 40.0) < 0.1, "Objective should be 40"
    
    print("✅ PASSED")
    return True

def test_c2q2():
    """Test problem C2Q2 (minimization with >= constraints)"""
    print("\n" + "="*60)
    print("TEST 3: Problem C2Q2 (Minimization)")
    print("="*60)
    
    c = [0.5, 0.03]
    A_ub = [[-8, -6],   # Negate for >= constraint
            [-1, -2]]
    b_ub = [-48, -12]   # Negate for >= constraint
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None), (0, None)], method='highs')
    
    print(f"x0 = {result.x[0]:.1f}")
    print(f"x1 = {result.x[1]:.1f}")
    print(f"Objective = {result.fun:.2f}")
    
    assert abs(result.fun - 0.24) < 0.01, "Objective should be 0.24"
    
    print("✅ PASSED")
    return True

def test_c4q8():
    """Test problem C4Q8 (3 variables)"""
    print("\n" + "="*60)
    print("TEST 4: Problem C4Q8 (3 Variables)")
    print("="*60)
    
    c = [4, 3, 2]
    A_ub = [[-2, -4, -1],
            [-3, -2, -1]]
    b_ub = [-16, -12]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)]*3, method='highs')
    
    print(f"x0 = {result.x[0]:.1f}")
    print(f"x1 = {result.x[1]:.1f}")
    print(f"x2 = {result.x[2]:.1f}")
    print(f"Objective = {result.fun:.1f}")
    
    assert abs(result.fun - 17.0) < 0.1, "Objective should be 17"
    
    print("✅ PASSED")
    return True

def test_assignment_problem():
    """Test assignment problem C4Q32"""
    print("\n" + "="*60)
    print("TEST 5: Assignment Problem C4Q32")
    print("="*60)
    
    c = [22, 18, 35, 41, 30, 28, 25, 36, 18]
    A_eq = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 1]]
    b_eq = [1, 1, 1, 1, 1, 1]
    
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)]*9, method='highs')
    
    print(f"Objective = {result.fun:.1f}")
    print(f"Solution vector (non-zero elements):")
    for i, val in enumerate(result.x):
        if val > 0.01:
            print(f"  x{i} = {val:.2f}")
    
    assert abs(result.fun - 70.0) < 0.1, "Objective should be 70"
    
    print("✅ PASSED")
    return True

def test_transportation_problem():
    """Test transportation problem C4Q33"""
    print("\n" + "="*60)
    print("TEST 6: Transportation Problem C4Q33")
    print("="*60)
    
    c = [40, 65, 70, 30]
    A_eq = [[1, 1, 0, 0],
            [0, 0, 1, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1]]
    b_eq = [250, 400, 300, 350]
    
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)]*4, method='highs')
    
    print(f"x0 = {result.x[0]:.1f}")
    print(f"x1 = {result.x[1]:.1f}")
    print(f"x2 = {result.x[2]:.1f}")
    print(f"x3 = {result.x[3]:.1f}")
    print(f"Objective = {result.fun:.1f}")
    
    assert abs(result.fun - 24000.0) < 0.1, "Objective should be 24000"
    
    print("✅ PASSED")
    return True

def test_scalable_formulation():
    """Test scalable formulation with data structures"""
    print("\n" + "="*60)
    print("TEST 7: Scalable Formulation")
    print("="*60)
    
    products = ['chair', 'table']
    price = {'chair': 40, 'table': 50}
    resources = ['wood', 'labor']
    capacity = {'wood': 40, 'labor': 120}
    bom = {
        ('wood', 'chair'): 1,
        ('wood', 'table'): 2,
        ('labor', 'chair'): 4,
        ('labor', 'table'): 3
    }
    
    c = [-price[p] for p in products]
    A_ub = [[bom[(r, p)] for p in products] for r in resources]
    b_ub = [capacity[r] for r in resources]
    bounds = [(0, None) for _ in products]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    print(f"Revenue = ${-result.fun:.1f}")
    for i, p in enumerate(products):
        print(f"  {p} = {result.x[i]:.1f}")
    
    assert abs(-result.fun - 1360.0) < 0.1, "Revenue should be $1360"
    
    print("✅ PASSED")
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("scipy.optimize Conversion Test Suite")
    print("="*60)
    print("\nTesting all converted optimization examples...")
    
    tests = [
        test_factory_problem,
        test_c2q1,
        test_c2q2,
        test_c4q8,
        test_assignment_problem,
        test_transportation_problem,
        test_scalable_formulation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 All tests passed successfully!")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
