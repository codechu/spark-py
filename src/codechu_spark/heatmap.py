"""1D heatmap renderer."""

from __future__ import annotations

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

    lo = min(values)
    hi = max(values)
    span = hi - lo
    if span == 0:
        return chars[0] * len(values)

    n = len(chars)
    out: list[str] = []
    for v in values:
        idx = int(round((v - lo) / span * (n - 1)))
        idx = max(0, min(n - 1, idx))
        out.append(chars[idx])
    return "".join(out)
