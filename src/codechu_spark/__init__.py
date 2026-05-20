"""codechu-spark — stdlib-only text visualizations.

Re-exports:

- :func:`sparkline` — one-row Unicode sparkline
- :func:`bar_chart` — labeled horizontal mini bar chart
- :func:`heatmap`   — 1D heatmap with intensity glyphs
"""

from __future__ import annotations

from .bars import bar_chart
from .heatmap import heatmap
from .sparkline import sparkline

__version__ = "0.2.0"

__all__ = [
    "__version__",
    "bar_chart",
    "heatmap",
    "sparkline",
]
