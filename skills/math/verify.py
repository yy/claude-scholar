#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["sympy"]
# ///
"""SymPy verification helper for math derivations."""

import re
import sys

from sympy import (
    Symbol,
    symbols,
    sympify,
    simplify,
    expand,
    expand_log,
    diff,
    integrate,
    solve,
)

# Pre-declare common symbols
x, y, z, t, s, n, k = symbols("x y z t s n k")
a, b, c, C = symbols("a b c C")

# SymPy reserved symbols that conflict with common variable names
# E=Euler's number, I=imaginary unit, S=singleton, N=numeric eval, O=big-O
SYMPY_RESERVED = {"E", "I", "S", "N", "O"}

_WORD_BOUNDARY = re.compile(r"\b[A-Z]\b")


def _make_local_dict(expr_str: str) -> dict:
    """Create a local dict that treats reserved symbols as regular variables if used."""
    local_dict = {}
    for name in SYMPY_RESERVED:
        if re.search(r"\b" + name + r"\b", expr_str):
            # Override reserved symbol with a regular Symbol
            local_dict[name] = Symbol(name)
    return local_dict


def safe_sympify(expr: str):
    """Sympify with handling for reserved symbol names."""
    local_dict = _make_local_dict(expr)
    return sympify(expr, locals=local_dict)


def check_equal(expr1: str, expr2: str) -> None:
    """Check if two expressions are equivalent."""
    # Combine both expressions to detect reserved symbols consistently
    combined = expr1 + " " + expr2
    local_dict = _make_local_dict(combined)
    e1 = sympify(expr1, locals=local_dict)
    e2 = sympify(expr2, locals=local_dict)
    diff_result = simplify(e1 - e2)
    if diff_result == 0:
        print(f"✓ {expr1} = {expr2}")
    else:
        print(f"✗ Not equal. Difference: {diff_result}")


def derive(expr: str, var: str = "x") -> None:
    """Compute derivative."""
    e = safe_sympify(expr)
    v = Symbol(var)
    result = diff(e, v)
    print(f"d/d{var}[{e}] = {simplify(result)}")


def integrate_expr(expr: str, var: str = "x") -> None:
    """Compute integral."""
    e = safe_sympify(expr)
    v = Symbol(var)
    result = integrate(e, v)
    print(f"∫ {e} d{var} = {result}")


def simp(expr: str) -> None:
    """Simplify expression."""
    e = safe_sympify(expr)
    print(f"Original:   {e}")
    print(f"Simplified: {simplify(e)}")
    print(f"Expanded:   {expand(e)}")
    # Try additional simplifications if relevant
    try:
        el = expand_log(e, force=True)
        if el != e:
            print(f"Log expand: {el}")
    except Exception:
        pass


def solve_expr(expr: str, var: str = "x") -> None:
    """Solve equation (expr = 0)."""
    e = safe_sympify(expr)
    v = Symbol(var)
    solutions = solve(e, v)
    print(f"Solutions to {e} = 0: {solutions}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: verify.py <command> <args...>")
        print("Commands: eq, diff, int, simp, solve")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    match cmd:
        case "eq":
            check_equal(args[0], args[1])
        case "diff":
            derive(args[0], args[1] if len(args) > 1 else "x")
        case "int":
            integrate_expr(args[0], args[1] if len(args) > 1 else "x")
        case "simp":
            simp(args[0])
        case "solve":
            solve_expr(args[0], args[1] if len(args) > 1 else "x")
        case _:
            print(f"Unknown command: {cmd}")
