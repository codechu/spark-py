# codechu-spark — API reference

Reference for every public symbol in `codechu_spark` 0.2.0.

The package re-exports three rendering functions and a version
constant:

```python
from codechu_spark import sparkline, bar_chart, heatmap, __version__
```

| Symbol         | Kind     | Returns | Summary                                  |
| -------------- | -------- | ------- | ---------------------------------------- |
| `sparkline`    | function | `str`   | One-row Unicode sparkline                |
| `bar_chart`    | function | `str`   | Multi-line labeled horizontal bar chart  |
| `heatmap`      | function | `str`   | One-row 1-D intensity heatmap            |
| `__version__`  | constant | `str`   | Package version (`"0.2.0"`)              |

All rendering functions are pure: no I/O, no globals, no terminal
control codes — they return strings you print yourself.

---

## `sparkline`

```python
sparkline(
    values: list[float],
    *,
    width: int | None = None,
    chars: str = "▁▂▃▄▅▆▇█",
) -> str
```

Render `values` as a single-row Unicode sparkline. Values are
min/max linearly scaled across the glyph ramp.

### Parameters

| Name     | Type                | Default       | Description                                                                                          |
| -------- | ------------------- | ------------- | ---------------------------------------------------------------------------------------------------- |
| `values` | `list[float]`       | —             | Series to render. Any iterable of numbers; `int` and `float` both accepted.                          |
| `width`  | `int \| None`       | `None`        | Target output width. `None` → one glyph per value. If `width < len(values)`, the series is downsampled by averaging consecutive buckets. `width >= len(values)` is treated as no-op (no upsampling, no padding). |
| `chars`  | `str`               | `"▁▂▃▄▅▆▇█"`  | Glyph ramp ordered low → high. Any length ≥ 1.                                                       |

### Returns

`str` — exactly `min(len(values), width)` glyphs from `chars`
(or `""` if `values` is empty).

### Raises

- `ValueError` — if `chars` is empty.
- `ValueError` — if `values` contains `NaN` (raised from the
  internal scaling step; not caught explicitly).

### Example

```python
>>> sparkline([1, 3, 7, 2, 5])
'▁▃█▂▆'

>>> sparkline(list(range(20)), width=5)
'▁▃▅▆█'

>>> sparkline([1, 2, 3], chars=".-=#")
'.-#'
```

### Edge cases

| Input                                | Output     | Notes                                              |
| ------------------------------------ | ---------- | -------------------------------------------------- |
| `[]`                                 | `''`       | Empty series short-circuits.                       |
| `[5, 5, 5]`                          | `'▁▁▁'`    | All-equal → first glyph (span == 0).               |
| `[42]`                               | `'▁'`      | Single value → first glyph (span == 0).            |
| `[1.0, float('nan'), 3.0]`           | _raises_   | `ValueError: cannot convert float NaN to integer`. |
| `sparkline([1,2,3], width=10)`       | `'▁▄█'`    | `width > len(values)`: no upsampling.              |
| `sparkline([1,2,3,4], chars="")`     | _raises_   | `ValueError: chars must be non-empty`.             |

---

## `bar_chart`

```python
bar_chart(
    items: list[tuple[str, float]],
    *,
    width: int = 40,
    char: str = "█",
) -> str
```

Render `items` as a multi-line labeled horizontal bar chart. Each
line is `"<label>  <bar>  <value>"`, with labels left-padded to the
longest label and bars padded with spaces to `width`.

### Parameters

| Name    | Type                          | Default | Description                                                                |
| ------- | ----------------------------- | ------- | -------------------------------------------------------------------------- |
| `items` | `list[tuple[str, float]]`     | —       | `(label, value)` pairs, rendered in order.                                 |
| `width` | `int`                         | `40`    | Maximum bar width in glyphs. Must be ≥ 1.                                  |
| `char`  | `str`                         | `"█"`   | Bar glyph. Must be non-empty (may be multi-character).                     |

### Returns

`str` — lines joined by `"\n"`. Returns `""` if `items` is empty.

### Raises

- `ValueError` — if `width < 1`.
- `ValueError` — if `char` is empty.

### Example

```python
>>> print(bar_chart([
...     ("python", 42),
...     ("rust",   17),
...     ("go",     8),
... ], width=20))
python  ████████████████████  42
rust    ████████              17
go      ████                  8
```

### Value formatting

- Integers (or floats that are whole numbers) render without a
  decimal point: `42` → `"42"`, `7.0` → `"7"`.
- Other floats render with one decimal: `3.5` → `"3.5"`.

### Edge cases

| Input                                       | Output                                              | Notes                                                       |
| ------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------- |
| `[]`                                        | `''`                                                | Empty input short-circuits.                                 |
| `[('solo', 5)]`, `width=10`                 | `'solo  ██████████  5'`                             | Single item → full-width bar.                               |
| `[('a', 0), ('b', 0)]`                      | bars all empty (spaces only); values still printed  | `max_v <= 0` falls back to `1.0` divisor.                   |
| `[('a', -3), ('b', 10)]`                    | `a` bar is empty; printed value is `-3`             | Negative values clip to zero-width bar but value is verbatim. |
| `[('a', float('nan'))]`                     | _raises_                                            | `ValueError` from `int(round(...))` on NaN.                 |
| `width=0`                                   | _raises_                                            | `ValueError: width must be ≥ 1`.                            |

---

## `heatmap`

```python
heatmap(
    values: list[float],
    *,
    chars: str = " ░▒▓█",
) -> str
```

Render `values` as a single-row 1-D heatmap, one glyph per value.
Same scaling rule as `sparkline`, but with a denser default ramp
suited to intensity readouts.

### Parameters

| Name     | Type           | Default      | Description                              |
| -------- | -------------- | ------------ | ---------------------------------------- |
| `values` | `list[float]`  | —            | Series to render.                        |
| `chars`  | `str`          | `" ░▒▓█"`    | Glyph ramp ordered low → high.           |

### Returns

`str` — one glyph per input value, or `""` for empty input.

### Raises

- `ValueError` — if `chars` is empty.
- `ValueError` — if `values` contains `NaN`.

### Example

```python
>>> heatmap([0, 1, 2, 3, 4])
' ░▒▓█'

>>> heatmap([0, 5, 10], chars=".oO")
'.oO'
```

### Edge cases

| Input                       | Output    | Notes                              |
| --------------------------- | --------- | ---------------------------------- |
| `[]`                        | `''`      | Empty input short-circuits.        |
| `[7, 7, 7]`                 | `'   '`   | All-equal → first glyph repeated (default ramp's first glyph is space). |
| `[42]`                      | `' '`     | Single value → first glyph.        |
| `[1.0, float('nan'), 3.0]`  | _raises_  | `ValueError`.                      |

---

## `__version__`

```python
>>> from codechu_spark import __version__
>>> __version__
'0.2.0'
```

String constant; tracks the package release.

---

## Internal helpers (not public)

`codechu_spark._helpers._glyph_ramp` and
`codechu_spark.sparkline._downsample` are implementation details.
They are **not** re-exported and may change without a deprecation
cycle. Don't import them.

See [MIGRATION.md](MIGRATION.md) for the 0.1 → 0.2 refactor that
introduced `_glyph_ramp`.
