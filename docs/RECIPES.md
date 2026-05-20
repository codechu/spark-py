# Recipes

Short, copy-pasteable patterns. Every recipe uses only the public
API and the Python standard library.

---

## 1. CPU history as a one-line sparkline

A common monitoring use case: keep a rolling window of samples and
render it as a single line beside other status text.

```python
from collections import deque
from codechu_spark import sparkline

window = deque(maxlen=60)

def on_sample(cpu_percent: float) -> None:
    window.append(cpu_percent)
    line = sparkline(list(window), width=30)
    print(f"cpu {cpu_percent:5.1f}%  {line}")
```

Example output for a synthetic 60-sample series, downsampled to
width 30:

```
cpu  62.4%  ▇▂▃▄▄▆▄▃█▇▄▇▂▄█▅▄▂▄▆▁▄▅▃▅▅▁▆▂▅
```

The `deque(maxlen=...)` does the windowing; `width=` does the
downsample-to-fit so the output column stays stable.

---

## 2. Labeled mini-bar chart for top-N items

`bar_chart` already does the layout. Sort, slice, hand it the
tuples.

```python
from codechu_spark import bar_chart

sizes = {
    "logs":         4200,
    "build":         980,
    "cache":         510,
    "node_modules":  320,
    "venv":          180,
    "tmp":            40,
}

top5 = sorted(sizes.items(), key=lambda kv: kv[1], reverse=True)[:5]
print(bar_chart(top5, width=25))
```

Output:

```
logs          █████████████████████████  4200
build         ██████                     980
cache         ███                        510
node_modules  ██                         320
venv          █                          180
```

Labels left-pad to the longest entry, bars scale to the max value.

---

## 3. 1-D heatmap for density

A heatmap row is denser than a sparkline — useful when you have a
fixed-length bucketed series (hours, days, percentiles) and want
intensity, not shape.

```python
from codechu_spark import heatmap

# requests per hour, midnight → 11pm
hours = [0,0,1,2,3,5,8,12,15,18,22,30,
         40,45,50,48,42,35,28,20,15,10,6,3]

print(heatmap(hours))
```

Output (24 chars, one per hour):

```
      ░░░░▒▒▓███▓▓▒▒░░
```

Quiet pre-dawn maps to spaces, the noon-to-afternoon peak to full
blocks. Combine with hour ticks above for a one-row "when does
traffic happen?" readout.

---

## 4. Custom glyph ramp

Both `sparkline` and `heatmap` accept `chars=` — any string ordered
low → high. Useful when the default Unicode blocks don't render
well in your terminal font, or when you want an ASCII-safe build.

```python
from codechu_spark import sparkline

# Classic ASCII ramp, low to high
ascii_ramp = ".:-=+*#%@"
print(sparkline([0.1, 0.3, 0.7, 0.9, 1.0], chars=ascii_ramp))
# → .-*%@

# Two-tone "is it busy or not" ramp
print(sparkline([0, 1, 0, 1, 1, 0], chars=" █"))
# →  █ ██
```

Rules:

- `chars` must be non-empty (else `ValueError`).
- One Python character per glyph is assumed; if you pass an emoji
  whose terminal width is 2, your output will visually be twice as
  wide as the glyph count.

---

## 5. Downsample a long series to terminal width

`sparkline(values, width=N)` downsamples by averaging consecutive
buckets. To fit any terminal:

```python
import shutil
from codechu_spark import sparkline

def fit_sparkline(values: list[float], reserve: int = 12) -> str:
    """Render `values` to the current terminal width.

    `reserve` columns are left for a leading label or trailing units.
    """
    cols = shutil.get_terminal_size((80, 24)).columns
    width = max(8, cols - reserve)
    return sparkline(values, width=width)


big = [i % 23 + (i // 17) for i in range(10_000)]
print(f"throughput  {fit_sparkline(big)}")
```

Notes:

- `width >= len(values)` is treated as no-op — no upsampling. If you
  pass an absurdly large `width` for a short series, you'll get
  exactly `len(values)` glyphs back.
- Averaging smooths outliers. If you want peaks preserved, downsample
  yourself (e.g. take `max` per bucket) and pass the result with
  `width=None`.
