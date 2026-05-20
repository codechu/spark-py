```text
   c o d e c h u  ·  s p a r k
   ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▄▆█▆▄▂▁▃▅▇█▇▅▃▁▂▅█▅▂▁▄▇▄▁▂▆█▆▂▁▃▇▇▃▁
   ── one line. one glance. one truth about your data. ──
```

> *Unicode sparklines, mini bar charts, and 1-D heatmaps — pure text.*

# codechu-spark

Stdlib-only text visualizations — Unicode sparklines, labeled mini
bar charts, 1D heatmaps — extracted from the [Disk Cleaner](https://github.com/codechu/disk-cleaner)
toolchain. No external dependencies. Python 3.10+.

## Install

```bash
pip install codechu-spark
```

## API

### `sparkline(values, *, width=None, chars="▁▂▃▄▅▆▇█")`

```python
from codechu_spark import sparkline

sparkline([1, 3, 7, 2, 5])                # → '▁▃█▂▅'
sparkline(list(range(100)), width=10)     # downsampled by averaging
sparkline([1, 2, 3], chars=".-=#")        # custom glyphs
```

- `width=None` → one glyph per value
- `width<len(values)` → downsample by averaging consecutive buckets
- `width>len(values)` → render at `len(values)` (no upsampling)
- Empty list → `''`; all-equal → first glyph repeated

### `bar_chart(items, *, width=40, char="█")`

```python
from codechu_spark import bar_chart

print(bar_chart([
    ("python", 42),
    ("rust",   17),
    ("go",     8),
], width=20))
# python  ████████████████████  42
# rust    ████████              17
# go      ███                    8
```

Bars are scaled to the maximum value. Labels are left-aligned to the
longest label. Negative values clip to a zero-width bar.

### `heatmap(values, *, chars=" ░▒▓█")`

```python
from codechu_spark import heatmap

heatmap([0, 1, 2, 3, 4])     # → ' ░▒▓█'
heatmap([0, 5, 10], chars=".oO")
```

A denser-than-sparkline row. Useful for per-bucket load,
hour-of-day utilization, or any single-row intensity readout.

## Design

- **Pure stdlib.** Zero third-party dependencies.
- **Single-row primitives.** Each function returns a string (with
  embedded newlines for `bar_chart`); no terminal control codes, no
  cursor movement — that's a separate concern.
- **Custom glyphs welcome.** Pass any `chars` string ordered low → high.

## Tests

```bash
pip install -e ".[dev]"
pytest -q
```

Coverage gate: ≥90 %.

## License

MIT — see [LICENSE](LICENSE).
