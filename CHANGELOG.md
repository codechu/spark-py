# Changelog

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/).

## [Unreleased]

## [0.3.0] — 2026-05-20

### Added
- `sparkline(..., thresholds=[low, high], colors=(low, mid, high))` —
  per-glyph ANSI coloring based on value band. Backwards-compatible:
  with `thresholds=None` the function is byte-identical to 0.2.
- `multi_sparkline(series_list, labels=None, *, share_scale=True)` —
  render multiple series on adjacent lines. Shared min/max by default
  so heights compare across rows; opt-in independent scaling.
- `sparkline_with_axis(values, *, width=None)` — one-line layout
  `"min →▁▂▃▄← max"` for dashboards.

## [0.2.0] — 2026-05-20

### Changed
- Internal refactor: extracted shared `_glyph_ramp` helper used by
  `sparkline` and `heatmap` (private API, no behavior change).

## [0.1.0] — 2026-05-20

### Added
- Initial extraction from [codechu/cli-py](https://github.com/codechu/cli-py)
- `sparkline(values, *, width, chars)` — Unicode eighth-block
  sparkline with optional downsampling + custom glyphs
- `bar_chart(items, *, width, char)` — multi-line labeled horizontal
  bar chart, scaled to max value
- `heatmap(values, *, chars)` — 1D heatmap row with intensity glyphs
