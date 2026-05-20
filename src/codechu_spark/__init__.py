"""codechu-spark — stdlib-only text visualizations.

Re-exports:

- :func:`sparkline` — one-row Unicode sparkline (optional threshold
  coloring via ANSI escapes)
- :func:`multi_sparkline` — multiple series on adjacent lines, shared
  or independent scale
- :func:`sparkline_with_axis` — sparkline with min/max axis labels
- :func:`bar_chart` — labeled horizontal mini bar chart
- :func:`heatmap`   — 1D heatmap with intensity glyphs
"""

from __future__ import annotations

from .bars import bar_chart
from .heatmap import heatmap
from .sparkline import multi_sparkline, sparkline, sparkline_with_axis

__version__ = "0.3.0"

__all__ = [
    "__version__",
    "bar_chart",
    "heatmap",
    "multi_sparkline",
    "sparkline",
    "sparkline_with_axis",
]
