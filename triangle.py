"""Triangle classifier.

classify_triangle(a, b, c) returns one of:
    "Invalid", "Equilateral", "Isosceles", "Scalene",
    "Right Isosceles", "Right Scalene"
"""

import math
from numbers import Real

# Relative tolerance used for every floating-point equality check.
REL_TOL = 1e-9


def _is_number(x) -> bool:
    """True for finite real numbers (bools are rejected even though they subclass int)."""
    return isinstance(x, Real) and not isinstance(x, bool) and math.isfinite(x)


def _close(x, y) -> bool:
    return math.isclose(x, y, rel_tol=REL_TOL)


def is_valid_triangle(a, b, c) -> bool:
    """Return True if a, b, c can form a non-degenerate triangle."""
    sides = (a, b, c)
    if not all(_is_number(s) for s in sides):
        return False
    if any(s <= 0 for s in sides):
        return False

    small, mid, large = sorted(sides)
    # Strict triangle inequality; the degenerate case (small + mid == large)
    # is invalid, including when floating-point error makes it look slightly larger.
    return small + mid > large and not _close(small + mid, large)


def _is_right(a, b, c) -> bool:
    small, mid, large = sorted((a, b, c))
    return _close(small**2 + mid**2, large**2)


def classify_triangle(a, b, c) -> str:
    """Classify a triangle by its side lengths. Never raises; bad input -> "Invalid"."""
    if not is_valid_triangle(a, b, c):
        return "Invalid"

    ab, bc, ac = _close(a, b), _close(b, c), _close(a, c)
    if ab and bc:
        # An equilateral triangle cannot be right, so no prefix check is needed.
        return "Equilateral"

    kind = "Isosceles" if (ab or bc or ac) else "Scalene"
    return f"Right {kind}" if _is_right(a, b, c) else kind
