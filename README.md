# Triangle Classifier

`triangle.py` provides two functions:

- `is_valid_triangle(a, b, c) -> bool`
- `classify_triangle(a, b, c) -> str`: returns `"Invalid"`, `"Equilateral"`, `"Isosceles"`, `"Scalene"`, `"Right Isosceles"`, or `"Right Scalene"`

## How to run the tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Run one file only: `pytest test_triangle.py` or `pytest test_acceptance.py`.

## Why an equilateral triangle can never be right

A right triangle needs a² + b² = c² where c is its longest side. If all three sides equal *s*, that becomes 2s² = s², which only holds for s = 0, and a side of 0 is not a valid triangle.

## Equivalence classes and boundaries

| # | Class | Example input | Expected |
|---|-------|---------------|----------|
| 1 | A side is zero | `(0, 4, 5)` | Invalid |
| 2 | A side is negative | `(-3, 4, 5)` | Invalid |
| 3 | Triangle inequality fails (any side order) | `(1, 2, 10)` | Invalid |
| 4 | Non-numeric / NaN / infinity / bool | `("3", 4, 5)`, `(nan, 4, 5)` | Invalid |
| 5 | All sides equal | `(1, 1, 1)` | Equilateral |
| 6 | Exactly two equal (each position) | `(5, 5, 3)`, `(5, 3, 5)`, `(3, 5, 5)` | Isosceles |
| 7 | All different | `(4, 5, 6)` | Scalene |
| 8 | Right, all different | `(3, 4, 5)` | Right Scalene |
| 9 | Right, two equal (irrational hypotenuse) | `(5, 5, 5*sqrt(2))` | Right Isosceles |

**Boundaries:**

- **Side = 0**: the edge between invalid and valid side lengths. 0 is invalid.
- **Degenerate**: two sides sum exactly to the third, e.g. `(1, 2, 3)`. This is invalid (the "triangle" is flat). Floating-point inputs like `(0.1, 0.2, 0.3)` are also tested, because `0.1 + 0.2` evaluates to `0.30000000000000004` and a plain `>` check would accept it. Just past the boundary, `(1, 2, 2.999)` is valid.
- **Right angle**: `(3, 4, 5)` is right, while `(3, 4, 5.01)` is not. Right-angle checks use `math.isclose` (relative tolerance 1e-9), never `==`.

## Copilot Review Log

Every suggestion was judged against the spec table, not against what `triangle.py` currently returns.

| Test | Copilot-suggested? | Kept / edited / rejected | Why |
|------|--------------------|--------------------------|-----|
| `test_right_isosceles_non_integer_hypotenuse` | Yes | Edited | Copilot asserted the Pythagorean check with `==`. For legs 5, 5 and hypotenuse `5*sqrt(2)`, `5**2 + 5**2 == hyp**2` is `False` because of floating-point rounding, so an `==`-based check would label this "Isosceles" instead of "Right Isosceles". Changed to rely on `math.isclose` (via `classify_triangle`), and added `assert 5**2 + 5**2 != hyp**2` so the test shows why a tolerance is needed. |
| `test_non_positive_side_is_invalid` | No | — | Written without Copilot. Covers zero and negative sides in each position. |
| `test_triangle_inequality_fails_is_invalid` | No | — | Written without Copilot. Covers the long side in each position. |
| `test_degenerate_triangle_is_invalid` | No | — | Written without Copilot. Includes `(0.1, 0.2, 0.3)`, which a plain `>` check gets wrong. |
| `test_equilateral` | No | — | Written without Copilot. |
| `test_isosceles` | No | — | Written without Copilot. Covers the equal pair in all three positions. |
| `test_scalene` | No | — | Written without Copilot. |
| `test_right_scalene_integer_sides` | No | — | Written without Copilot. |
| `test_non_numeric_input_is_invalid` | No | — | Written without Copilot. |

## Acceptance Criteria (stained-glass studio)

Customer request: show the shape, say whether it is buildable, don't crash on invalid input, flag right-angle pieces, and be correct every time.

- **AC1: Correct classification.** For every input in the reference set in `test_acceptance.py`, `classify_triangle` returns exactly the expected label, with 0 mismatches.
- **AC2: Invalid input is reported, not crashed on.** For every non-buildable input (a side ≤ 0, degenerate, triangle inequality fails, non-numeric or empty), `classify_triangle` returns `"Invalid"` and raises no exception.
- **AC3: Right-angle pieces are flagged.** The result starts with `"Right "` if and only if the sides satisfy a² + b² = c² within a relative tolerance of 1e-9. This holds for integer sides and for irrational ones like `8, 8, 8√2`.

`test_acceptance.py` runs every reference case through `classify_triangle()` and checks all three criteria.
