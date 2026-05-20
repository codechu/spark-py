"""Internal helpers shared across renderers."""

from __future__ import annotations

__all__ = ["_glyph_ramp"]


def _glyph_ramp(values: list[float], chars: str) -> str:
    """Map ``values`` onto ``chars`` by min/max linear scaling.

    Preconditions (callers enforce): ``values`` non-empty, ``chars``
    non-empty. Returns ``chars[0]`` repeated when every value is
    equal (span == 0).
    """
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
