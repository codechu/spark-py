```text
   c o d e c h u  ·  s p a r k
   ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▄▆█▆▄▂▁▃▅▇█▇▅▃▁▂▅█▅▂▁▄▇▄▁▂▆█▆▂▁▃▇▇▃▁
   ── one line. one glance. one truth about your data. ──
```

[![PyPI](https://img.shields.io/pypi/v/codechu-spark.svg)](https://pypi.org/project/codechu-spark/)
[![Python](https://img.shields.io/pypi/pyversions/codechu-spark.svg)](https://pypi.org/project/codechu-spark/)
[![CI](https://github.com/codechu/spark-py/actions/workflows/ci.yml/badge.svg)](https://github.com/codechu/spark-py/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

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

## Documentation

- [API reference](docs/API.md) — every public symbol with signatures,
  examples, and edge-case tables.
- [Recipes](docs/RECIPES.md) — sparkline windows, top-N bars, 1-D
  heatmaps, custom ramps, terminal-width downsampling.
- [Migration guide](docs/MIGRATION.md) — 0.1 → 0.2 (internal refactor,
  no API changes).

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

## Codechu family

Companion libraries from the Codechu Python ecosystem:

| Library | Purpose |
|---------|---------|
| [codechu-fmt](https://pypi.org/project/codechu-fmt/) | Human-readable formatting — sizes, durations, rates, percent |
| [codechu-meter](https://pypi.org/project/codechu-meter/) | Timing primitives — Stopwatch, ETA, percentile, histogram |
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, spinners, prompts, table |
| [codechu-events](https://pypi.org/project/codechu-events/) | Thread-safe multi-channel pub/sub bus with replay |
| [codechu-xdg](https://pypi.org/project/codechu-xdg/) | XDG Base Directory helpers, vendor-namespaced |
| [codechu-treeviz](https://pypi.org/project/codechu-treeviz/) | Tree visualization — treemap, sunburst, icicle, flame |
| [codechu-fs](https://pypi.org/project/codechu-fs/) | Filesystem primitives — atomic write, XDG trash, safe walk |
| [codechu-term](https://pypi.org/project/codechu-term/) | Terminal capability detection, alt buffer, raw mode |
| [codechu-color](https://pypi.org/project/codechu-color/) | Color palettes, WCAG contrast, color-blind variants |
| [codechu-treedata](https://pypi.org/project/codechu-treedata/) | N-ary tree data structures and algorithms |
| [codechu-log](https://pypi.org/project/codechu-log/) | Structured logging — context, JSON, rotation, redaction |
| [codechu-i18n](https://pypi.org/project/codechu-i18n/) | Internationalization — locale, plural rules, RTL |
| [codechu-ipc](https://pypi.org/project/codechu-ipc/) | Local IPC — Unix socket, FIFO, JSON-line protocol |
| [codechu-config](https://pypi.org/project/codechu-config/) | Schema-driven config — atomic save, migrations |

## Credits

- Unicode block elements per The Unicode Standard
- Conceptual lineage from Edward Tufte's "sparkline" notion (*Beautiful Evidence*, 2006)

## License

MIT — see [LICENSE](LICENSE).
