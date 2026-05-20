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

Stdlib-only text visualizations: single-row charts that fit a log
line, a status field, or a dashboard cell. No GUI, no external
deps — just Unicode block elements arranged for one-glance
readability.

```text
load:  ▁▃▄▆█▇▅▃▂▁                            sparkline
disk:  ████▆▆▅▅▄▃▂▁                          (auto-downsamples)
io:    ░░▒▒▓▓██▓▓▒░                          heatmap

python  ████████████████████  42             bar_chart
rust    ████████              17
go      ███                    8
```

## Install

```bash
pip install codechu-spark
```

Python 3.10+. Zero third-party dependencies.

## Quick example

```python
from codechu_spark import sparkline, bar_chart, heatmap

print(sparkline([1, 3, 7, 2, 5]))             # ▁▃█▂▅
print(sparkline(list(range(100)), width=10))  # downsampled by averaging

print(bar_chart([("python", 42), ("rust", 17), ("go", 8)], width=20))

print(heatmap([0, 1, 2, 3, 4]))               # ' ░▒▓█'
```

## What you get

- **`sparkline`** — one-row Unicode chart. Auto-downsamples by
  averaging when the data is wider than the target.
- **`multi_sparkline`** — multiple series stacked on adjacent lines.
- **`sparkline_with_axis`** — sparkline with min/max axis labels.
- **`bar_chart`** — multi-line labeled horizontal bars; scaled to
  the maximum value, labels left-aligned.
- **`heatmap`** — denser-than-sparkline single-row intensity readout.

All functions accept a custom `chars=` ramp (low → high) so you can
swap in ASCII fallbacks, color characters, or your own glyph set.

## Read more

- [API reference](docs/API.md) — every public symbol with signatures
  and edge-case tables.
- [Recipes](docs/RECIPES.md) — sparkline windows, top-N bars, 1-D
  heatmaps, custom ramps, terminal-width downsampling.
- [Migration guide](docs/MIGRATION.md) — 0.1 → 0.2 (internal refactor,
  no API changes).
- [Changelog](CHANGELOG.md)

## Family

| Library | Purpose |
|---------|---------|
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, spinners, prompts |
| [codechu-fmt](https://pypi.org/project/codechu-fmt/) | Human-readable sizes, durations, rates |
| [codechu-meter](https://pypi.org/project/codechu-meter/) | Timing — stopwatch, ETA, rate, histogram |
| [codechu-term](https://pypi.org/project/codechu-term/) | Terminal capabilities, alt buffer, raw mode |
| [codechu-treeviz](https://pypi.org/project/codechu-treeviz/) | Treemap + sunburst layouts |

Full ecosystem: [github.com/codechu](https://github.com/codechu).

## Credits

- Unicode block elements per The Unicode Standard.
- Conceptual lineage from Edward Tufte's "sparkline" notion
  (*Beautiful Evidence*, 2006).

## License

MIT — see [LICENSE](LICENSE).

Part of [Codechu](https://github.com/codechu).
