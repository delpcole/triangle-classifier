import math

import pytest

from triangle import classify_triangle, is_valid_triangle


# --- Invalid: non-positive sides ---------------------------------------------

@pytest.mark.parametrize("sides", [(0, 4, 5), (3, 0, 5), (3, 4, 0), (-3, 4, 5), (-1, -1, -1)])
def test_non_positive_side_is_invalid(sides):
    assert classify_triangle(*sides) == "Invalid"
    assert is_valid_triangle(*sides) is False


# --- Invalid: triangle inequality fails ---------------------------------------

@pytest.mark.parametrize("sides", [(1, 2, 10), (10, 1, 2), (2, 10, 1)])
def test_triangle_inequality_fails_is_invalid(sides):
    assert classify_triangle(*sides) == "Invalid"


# --- Boundary: degenerate (two sides sum exactly to the third) ----------------

@pytest.mark.parametrize("sides", [(1, 2, 3), (3, 1, 2), (2, 3, 1), (0.1, 0.2, 0.3)])
def test_degenerate_triangle_is_invalid(sides):
    # (0.1, 0.2, 0.3): 0.1 + 0.2 is 0.30000000000000004 in floating point,
    # which a plain `>` check would wrongly accept.
    assert classify_triangle(*sides) == "Invalid"


def test_just_past_degenerate_is_valid():
    assert is_valid_triangle(1, 2, 2.999) is True


# --- Equilateral --------------------------------------------------------------

@pytest.mark.parametrize("sides", [(1, 1, 1), (7.5, 7.5, 7.5)])
def test_equilateral(sides):
    assert classify_triangle(*sides) == "Equilateral"


# --- Isosceles (exactly two equal, any position) ------------------------------

@pytest.mark.parametrize("sides", [(5, 5, 3), (5, 3, 5), (3, 5, 5)])
def test_isosceles(sides):
    assert classify_triangle(*sides) == "Isosceles"


# --- Scalene ------------------------------------------------------------------

@pytest.mark.parametrize("sides", [(4, 5, 6), (6, 4, 5)])
def test_scalene(sides):
    assert classify_triangle(*sides) == "Scalene"


# --- Right triangles ----------------------------------------------------------

@pytest.mark.parametrize("sides", [(3, 4, 5), (5, 3, 4), (5, 12, 13)])
def test_right_scalene_integer_sides(sides):
    assert classify_triangle(*sides) == "Right Scalene"


def test_right_isosceles_non_integer_hypotenuse():
    # 5 * sqrt(2) is irrational, so 5**2 + 5**2 == (5*sqrt(2))**2 is False
    # with plain ==. This test fails if the implementation skips the tolerance.
    hyp = 5 * math.sqrt(2)
    assert 5**2 + 5**2 != hyp**2  # documents why a tolerance is required
    assert classify_triangle(5, 5, hyp) == "Right Isosceles"


def test_right_scalene_non_integer_sides():
    assert classify_triangle(1, math.sqrt(3), 2) == "Right Scalene"


def test_near_right_is_not_right():
    assert classify_triangle(3, 4, 5.01) == "Scalene"


# --- Bad input must not crash -------------------------------------------------

@pytest.mark.parametrize("sides", [("3", 4, 5), (None, 4, 5), (math.nan, 4, 5), (math.inf, 4, 5), (True, True, True)])
def test_non_numeric_input_is_invalid(sides):
    assert classify_triangle(*sides) == "Invalid"
