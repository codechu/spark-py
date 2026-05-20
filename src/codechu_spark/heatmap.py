"""1D heatmap renderer."""

from __future__ import annotations

from ._helpers import _glyph_ramp

__all__ = ["heatmap"]

_DEFAULT_CHARS = " ░▒▓█"


def heatmap(values: list[float], *, chars: str = _DEFAULT_CHARS) -> str:
    """Render a 1D heatmap row.

    Each value is mapped to one glyph from ``chars`` based on its
    position within the observed range. Useful for per-bucket load,
    cell utilization, or anything where you want a denser-than-
    sparkline visualization in a single row.

    - Empty input → ``''``.
    - All-equal input → ``chars[0]`` repeated.
    """
    if not values:
        return ""
    if not chars:
        raise ValueError("chars must be non-empty")

    return _glyph_ramp(list(values), chars)
