"""Unicode sparkline renderer."""

from __future__ import annotations

__all__ = ["sparkline"]

_DEFAULT_CHARS = "▁▂▃▄▅▆▇█"


def sparkline(
    values: list[float],
    *,
    width: int | None = None,
    chars: str = _DEFAULT_CHARS,
) -> str:
    """Render ``values`` as a Unicode sparkline.

    - ``width=None`` (default): one glyph per value.
    - ``width<len(values)``: downsample by averaging consecutive
      buckets to fit.
    - ``width>len(values)``: render at ``len(values)`` width — no
      upsampling, no padding.
    - ``chars``: any string of N glyphs ordered low → high.
    - Empty input → ``''``.
    - All-equal input → ``chars[0]`` repeated (every value scales
      to 0).
    """
    if not values:
        return ""
    if not chars:
        raise ValueError("chars must be non-empty")

    data = list(values)
    if width is not None and width > 0 and len(data) > width:
        data = _downsample(data, width)

    lo = min(data)
    hi = max(data)
    span = hi - lo
    if span == 0:
        return chars[0] * len(data)

    n_bars = len(chars)
    out: list[str] = []
    for v in data:
        idx = int(round((v - lo) / span * (n_bars - 1)))
        idx = max(0, min(n_bars - 1, idx))
        out.append(chars[idx])
    return "".join(out)


def _downsample(data: list[float], width: int) -> list[float]:
    n = len(data)
    bucket_size = n / width
    buckets: list[float] = []
    for i in range(width):
        lo = int(i * bucket_size)
        hi = int((i + 1) * bucket_size)
        if hi <= lo:
            hi = lo + 1
        chunk = data[lo:hi]
        if chunk:
            buckets.append(sum(chunk) / len(chunk))
    return buckets
