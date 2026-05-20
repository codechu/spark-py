# codechu-spark — API reference

Reference for every public symbol in `codechu_spark` 0.3.0.

The package re-exports five rendering functions and a version
constant:

```python
from codechu_spark import (
    sparkline,
    multi_sparkline,
    sparkline_with_axis,
    bar_chart,
    heatmap,
    __version__,
)
```

| Symbol                 | Kind     | Returns | Summary                                  |
| ---------------------- | -------- | ------- | ---------------------------------------- |
| `sparkline`            | function | `str`   | One-row Unicode sparkline (optional ANSI threshold coloring) |
| `multi_sparkline`      | function | `str`   | Multiple series on adjacent lines        |
| `sparkline_with_axis`  | function | `str`   | Sparkline with min/max axis labels       |
| `bar_chart`            | function | `str`   | Multi-line labeled horizontal bar chart  |
| `heatmap`              | function | `str`   | One-row 1-D intensity heatmap            |
| `__version__`          | constant | `str`   | Package version (`"0.3.0"`)              |

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
    thresholds: list[float] | tuple[float, float] | None = None,
    colors: tuple[str, str, str] | None = None,
) -> str
```

Render `values` as a single-row Unicode sparkline. Values are
min/max linearly scaled across the glyph ramp. With
`thresholds=[low, high]` + `colors=(low_ansi, mid_ansi, high_ansi)`
each glyph is wrapped in the matching ANSI escape based on its
post-downsample value (`v < low`, `low <= v < high`, `v >= high`).
Callers supply the raw ANSI codes — no palette is shipped, and the
caller decides whether the output stream supports color
(explicit-config principle).

### Parameters

| Name     | Type                | Default       | Description                                                                                          |
| -------- | ------------------- | ------------- | ---------------------------------------------------------------------------------------------------- |
| `values` | `list[float]`       | —             | Series to render. Any iterable of numbers; `int` and `float` both accepted.                          |
| `width`  | `int \| None`       | `None`        | Target output width. `None` → one glyph per value. If `width < len(values)`, the series is downsampled by averaging consecutive buckets. `width >= len(values)` is treated as no-op (no upsampling, no padding). |
| `chars`  | `str`               | `"▁▂▃▄▅▆▇█"`  | Glyph ramp ordered low → high. Any length ≥ 1.                                                       |
| `thresholds` | `list[float] \| None` | `None`    | `[low, high]` — value cutoffs between low/mid/high color bands. Must be paired with `colors`.        |
| `colors` | `tuple[str, str, str] \| None` | `None` | ANSI codes for the three bands, e.g. `("\x1b[32m", "\x1b[33m", "\x1b[31m")`. Must be paired with `thresholds`. |

### Returns

`str` — exactly `min(len(values), width)` glyphs from `chars`
(or `""` if `values` is empty). When coloring is enabled the
returned string contains ANSI escape sequences and `\x1b[0m`
resets around each glyph; the *visible* width is unchanged.

### Raises

- `ValueError` — if `chars` is empty.
- `ValueError` — if exactly one of `thresholds`/`colors` is given.
- `ValueError` — if `thresholds` is not length 2 or `colors` not
  length 3.
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

>>> # CPU history with green / yellow / red thresholds
>>> green, yellow, red = "\x1b[32m", "\x1b[33m", "\x1b[31m"
>>> sparkline(
...     [10, 45, 80],
...     thresholds=[30, 70],
...     colors=(green, yellow, red),
... )
'\x1b[32m▁\x1b[0m\x1b[33m▄\x1b[0m\x1b[31m█\x1b[0m'
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

## `multi_sparkline`

```python
multi_sparkline(
    series_list: list[list[float]],
    labels: list[str] | None = None,
    *,
    share_scale: bool = True,
    width: int | None = None,
    chars: str = "▁▂▃▄▅▆▇█",
) -> str
```

Render multiple series as adjacent sparkline rows, joined by `"\n"`.

### Parameters

| Name          | Type                       | Default       | Description                                                                                  |
| ------------- | -------------------------- | ------------- | -------------------------------------------------------------------------------------------- |
| `series_list` | `list[list[float]]`        | —             | One series per row, rendered in order.                                                       |
| `labels`      | `list[str] \| None`        | `None`        | Optional row labels. Must match `series_list` length. Padded to the longest label.           |
| `share_scale` | `bool`                     | `True`        | If `True`, all rows share one min/max (heights comparable). If `False`, each row scales independently. |
| `width`       | `int \| None`              | `None`        | Same semantics as `sparkline.width`; applied per row.                                        |
| `chars`       | `str`                      | `"▁▂▃▄▅▆▇█"`  | Glyph ramp ordered low → high.                                                               |

### Returns

`str` — rows joined by `"\n"`. Empty `series_list` → `""`. Empty
rows become empty lines (or label-only when labels supplied).

### Raises

- `ValueError` — if `labels` length does not match `series_list`.
- `ValueError` — if `chars` is empty.

### Example

```python
>>> print(multi_sparkline(
...     [[0, 1, 2, 3], [0, 5, 10, 15]],
...     labels=["small", "large"],
...     share_scale=True,
... ))
small  ▁▁▂▂
large  ▁▃▆█
```

With `share_scale=False`, both rows would end on `█`.

---

## `sparkline_with_axis`

```python
sparkline_with_axis(
    values: list[float],
    *,
    width: int | None = None,
    chars: str = "▁▂▃▄▅▆▇█",
) -> str
```

Render a sparkline with the min/max of the *original* series as
text labels on either side.

### Parameters

| Name     | Type           | Default       | Description                              |
| -------- | -------------- | ------------- | ---------------------------------------- |
| `values` | `list[float]`  | —             | Series to render.                        |
| `width`  | `int \| None`  | `None`        | Forwarded to the inner `sparkline`.      |
| `chars`  | `str`          | `"▁▂▃▄▅▆▇█"`  | Glyph ramp ordered low → high.           |

### Returns

`str` — `"<min> →<sparkline>← <max>"`. Integer-valued numbers
render without a decimal; other floats render with one decimal.
Empty input → `""`.

### Example

```python
>>> sparkline_with_axis([1, 2, 3, 4, 10])
'1 →▁▂▃▃█← 10'

>>> sparkline_with_axis(list(range(100)), width=10)
'0 →▁▂▃▃▄▅▆▆▇█← 99'
```

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
'0.3.0'
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
