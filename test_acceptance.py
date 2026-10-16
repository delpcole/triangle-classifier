"""Acceptance test for the stained-glass studio.

Acceptance criteria (see README for the full wording):

AC1  Correct shape: for every row in the reference table below, classify_triangle
     returns exactly the expected label (100% match, 0 mismatches).
AC2  Invalid input never crashes: for every non-buildable input (non-positive,
     degenerate, impossible, non-numeric), classify_triangle returns "Invalid"
     and raises no exception.
AC3  Right-angle pieces flagged: every input whose sides satisfy a^2 + b^2 = c^2
     (within a relative tolerance of 1e-9) returns a label starting with "Right ",
     and no non-right input does.
"""

import math

from triangle import classify_triangle

# (a, b, c, expected) -- what a customer would type, and what we must show them.
REFERENCE_CASES = [
    # buildable shapes
    (6, 6, 6, "Equilateral"),
    (10, 10, 4, "Isosceles"),
    (4, 7, 9, "Scalene"),
    # right-angle pieces (need reinforced corners)
    (3, 4, 5, "Right Scalene"),
    (30, 40, 50, "Right Scalene"),
    (8, 8, 8 * math.sqrt(2), "Right Isosceles"),
    (1.5, 2.0, 2.5, "Right Scalene"),
    # not buildable
    (0, 5, 5, "Invalid"),
    (-2, 3, 4, "Invalid"),
    (2, 3, 5, "Invalid"),        # degenerate: flat, zero area
    (1, 1, 50, "Invalid"),
    ("abc", 3, 4, "Invalid"),    # typo in the form
    (None, 3, 4, "Invalid"),     # empty field
]


def test_stained_glass_studio_acceptance():
    mismatches = []
    for a, b, c, expected in REFERENCE_CASES:
        # AC2: no exception may escape, whatever the customer typed.
        try:
            actual = classify_triangle(a, b, c)
        except Exception as exc:  # noqa: BLE001 - catching everything is the point
            mismatches.append(f"{(a, b, c)} raised {exc!r}")
            continue

        # AC1: exact label match.
        if actual != expected:
            mismatches.append(f"{(a, b, c)}: expected {expected!r}, got {actual!r}")

        # AC3: "Right " prefix appears if and only if the piece is a right triangle.
        if actual.startswith("Right ") != expected.startswith("Right "):
            mismatches.append(f"{(a, b, c)}: right-angle flag wrong ({actual!r})")

    assert mismatches == [], "Acceptance failures:\n" + "\n".join(mismatches)
