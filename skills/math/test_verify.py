#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["sympy", "pytest"]
# ///
"""Tests for the math verification helper."""

import pytest
from sympy import Symbol, symbols, simplify

from verify import (
    safe_sympify,
    check_equal,
    derive,
    integrate_expr,
    simp,
    solve_expr,
    _make_local_dict,
)


class TestSafeSympify:
    """Tests for safe_sympify and reserved symbol handling."""

    def test_basic_expression(self):
        """Basic expressions should parse correctly."""
        result = safe_sympify("x**2 + 2*x + 1")
        x = Symbol("x")
        assert result == x**2 + 2 * x + 1

    def test_reserved_symbol_E(self):
        """E should be treated as a variable, not Euler's number."""
        result = safe_sympify("E*x")
        E, x = Symbol("E"), Symbol("x")
        assert result == E * x
        # Verify it's not Euler's number (e ≈ 2.718)
        assert result.subs([(E, 1), (x, 1)]) == 1

    def test_reserved_symbol_I(self):
        """I should be treated as a variable, not imaginary unit."""
        result = safe_sympify("I*x")
        sym_I, x = Symbol("I"), Symbol("x")
        assert result == sym_I * x
        # Verify it's not imaginary unit
        assert result.subs([(sym_I, 2), (x, 3)]) == 6

    def test_reserved_symbol_S(self):
        """S should be treated as a variable."""
        result = safe_sympify("S + 1")
        S = Symbol("S")
        assert result == S + 1

    def test_reserved_symbol_N(self):
        """N should be treated as a variable."""
        result = safe_sympify("N**2")
        N = Symbol("N")
        assert result == N**2

    def test_reserved_symbol_O(self):
        """O should be treated as a variable."""
        result = safe_sympify("O*x")
        sym_O, x = Symbol("O"), Symbol("x")
        assert result == sym_O * x

    def test_multiple_reserved_symbols(self):
        """Multiple reserved symbols in one expression."""
        result = safe_sympify("E*I + S*N + O")
        sym_E, sym_I, sym_S, sym_N, sym_O = symbols("E I S N O")
        expected = sym_E * sym_I + sym_S * sym_N + sym_O
        assert simplify(result - expected) == 0

    def test_make_local_dict_detects_reserved(self):
        """_make_local_dict should detect reserved symbols in expression."""
        local_dict = _make_local_dict("E*x + I*y")
        assert "E" in local_dict
        assert "I" in local_dict
        assert "S" not in local_dict  # Not in expression

    def test_make_local_dict_empty_when_no_reserved(self):
        """_make_local_dict should return empty dict when no reserved symbols."""
        local_dict = _make_local_dict("x**2 + y")
        assert local_dict == {}


class TestCheckEqual:
    """Tests for check_equal function."""

    def test_equal_expressions(self, capsys):
        """Equal expressions should print success."""
        check_equal("x**2 + 2*x + 1", "(x+1)**2")
        captured = capsys.readouterr()
        assert "✓" in captured.out

    def test_unequal_expressions(self, capsys):
        """Unequal expressions should print failure."""
        check_equal("x**2", "x**3")
        captured = capsys.readouterr()
        assert "✗" in captured.out

    def test_equal_with_reserved_symbols(self, capsys):
        """Equality check should work with reserved symbols."""
        check_equal("2*E", "E + E")
        captured = capsys.readouterr()
        assert "✓" in captured.out

    def test_trig_identity(self, capsys):
        """Trigonometric identities should be recognized."""
        check_equal("sin(x)**2 + cos(x)**2", "1")
        captured = capsys.readouterr()
        assert "✓" in captured.out


class TestDerive:
    """Tests for derive function."""

    def test_basic_derivative(self, capsys):
        """Basic polynomial derivative."""
        derive("x**2", "x")
        captured = capsys.readouterr()
        assert "2*x" in captured.out

    def test_derivative_with_reserved_symbol(self, capsys):
        """Derivative with reserved symbol as variable."""
        derive("E**2", "E")
        captured = capsys.readouterr()
        assert "2*E" in captured.out

    def test_exp_derivative(self, capsys):
        """Derivative of exponential function."""
        derive("exp(x)", "x")
        captured = capsys.readouterr()
        assert "exp(x)" in captured.out

    def test_chain_rule(self, capsys):
        """Chain rule application."""
        derive("sin(x**2)", "x")
        captured = capsys.readouterr()
        assert "cos" in captured.out
        assert "2*x" in captured.out


class TestIntegrate:
    """Tests for integrate_expr function."""

    def test_basic_integral(self, capsys):
        """Basic polynomial integral."""
        integrate_expr("x**2", "x")
        captured = capsys.readouterr()
        assert "x**3/3" in captured.out

    def test_exp_integral(self, capsys):
        """Integral of exponential function."""
        integrate_expr("exp(x)", "x")
        captured = capsys.readouterr()
        assert "exp(x)" in captured.out

    def test_integral_with_reserved_symbol(self, capsys):
        """Integral with reserved symbol as variable."""
        integrate_expr("E", "E")
        captured = capsys.readouterr()
        assert "E**2/2" in captured.out


class TestSimp:
    """Tests for simp function."""

    def test_simplify_polynomial(self, capsys):
        """Simplification of polynomial."""
        simp("(x+1)**2 - x**2 - 2*x - 1")
        captured = capsys.readouterr()
        assert "Simplified: 0" in captured.out

    def test_expand_polynomial(self, capsys):
        """Expansion of polynomial."""
        simp("(x+1)**2")
        captured = capsys.readouterr()
        assert "x**2 + 2*x + 1" in captured.out

    def test_log_expansion(self, capsys):
        """Log expansion when applicable."""
        simp("log(x*y)")
        captured = capsys.readouterr()
        assert "Log expand:" in captured.out


class TestSolve:
    """Tests for solve_expr function."""

    def test_linear_equation(self, capsys):
        """Solve linear equation."""
        solve_expr("x - 5", "x")
        captured = capsys.readouterr()
        assert "5" in captured.out

    def test_quadratic_equation(self, capsys):
        """Solve quadratic equation."""
        solve_expr("x**2 - 4", "x")
        captured = capsys.readouterr()
        assert "-2" in captured.out
        assert "2" in captured.out

    def test_solve_with_reserved_symbol(self, capsys):
        """Solve for reserved symbol."""
        solve_expr("E**2 - 9", "E")
        captured = capsys.readouterr()
        assert "-3" in captured.out
        assert "3" in captured.out


class TestReservedSymbolsComprehensive:
    """Comprehensive tests ensuring reserved symbols work across all operations."""

    def test_E_in_all_operations(self, capsys):
        """E as variable works in all operations."""
        # Equality
        check_equal("E + E", "2*E")
        out1 = capsys.readouterr().out
        assert "✓" in out1

        # Derivative
        derive("E**3", "E")
        out2 = capsys.readouterr().out
        assert "3*E**2" in out2

        # Integral
        integrate_expr("E**2", "E")
        out3 = capsys.readouterr().out
        assert "E**3/3" in out3

        # Solve
        solve_expr("E - 7", "E")
        out4 = capsys.readouterr().out
        assert "7" in out4

    def test_mixed_reserved_and_regular_symbols(self, capsys):
        """Mix of reserved and regular symbols."""
        check_equal("E*x + I*y", "x*E + y*I")
        captured = capsys.readouterr()
        assert "✓" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
