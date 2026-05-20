"""Unicode sparkline renderer."""

from __future__ import annotations

from ._helpers import _glyph_ramp

__all__ = ["multi_sparkline", "sparkline", "sparkline_with_axis"]

_DEFAULT_CHARS = "▁▂▃▄▅▆▇█"
_ANSI_RESET = "\x1b[0m"


def sparkline(
    values: list[float],
    *,
    width: int | None = None,
    chars: str = _DEFAULT_CHARS,
    thresholds: list[float] | tuple[float, float] | None = None,
    colors: tuple[str, str, str] | None = None,
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

    Optional threshold coloring:

    - ``thresholds=[low, high]`` + ``colors=(low_ansi, mid_ansi,
      high_ansi)``: wrap each glyph in the matching ANSI escape based
      on the *post-downsample* value. ``v < low`` uses ``low_ansi``,
      ``low <= v < high`` uses ``mid_ansi``, ``v >= high`` uses
      ``high_ansi``. Callers supply the raw ANSI codes (e.g.
      ``"\\x1b[31m"``); no palette is shipped.
    - Both ``thresholds`` and ``colors`` must be provided together or
      both ``None``. ``thresholds=None`` preserves the pre-0.3
      uncolored output exactly.
    """
    if not values:
        return ""
    if not chars:
        raise ValueError("chars must be non-empty")

    color_on = thresholds is not None or colors is not None
    if color_on and (thresholds is None or colors is None):
        raise ValueError("thresholds and colors must be provided together")
    if color_on:
        if len(thresholds) != 2:
            raise ValueError("thresholds must be a 2-tuple [low, high]")
        if len(colors) != 3:
            raise ValueError("colors must be a 3-tuple (low, mid, high)")

    data = list(values)
    if width is not None and width > 0 and len(data) > width:
        data = _downsample(data, width)

    glyphs = _glyph_ramp(data, chars)
    if not color_on:
        return glyphs

    low, high = thresholds
    low_c, mid_c, high_c = colors
    out: list[str] = []
    for v, g in zip(data, glyphs):
        if v < low:
            c = low_c
        elif v < high:
            c = mid_c
        else:
            c = high_c
        out.append(f"{c}{g}{_ANSI_RESET}")
    return "".join(out)


def multi_sparkline(
    series_list: list[list[float]],
    labels: list[str] | None = None,
    *,
    share_scale: bool = True,
    width: int | None = None,
    chars: str = _DEFAULT_CHARS,
) -> str:
    """Render multiple series on adjacent lines.

    - ``share_scale=True`` (default): all series share one min/max
      derived from the union of values, so heights are comparable
      across rows.
    - ``share_scale=False``: each series is scaled independently
      (same as calling :func:`sparkline` per series).
    - ``labels``: optional list of label strings, one per series.
      Labels are right-padded to the longest label and separated from
      the sparkline by two spaces. ``None`` → no label column.
    - ``width`` / ``chars``: forwarded to the per-row render.

    Empty ``series_list`` → ``""``. Empty rows render as empty lines
    (label-only when labels supplied).
    """
    if not series_list:
        return ""
    if labels is not None and len(labels) != len(series_list):
        raise ValueError("labels length must match series_list length")
    if not chars:
        raise ValueError("chars must be non-empty")

    if share_scale:
        flat = [v for s in series_list for v in s]
        if flat:
            lo = min(flat)
            hi = max(flat)
        else:
            lo = hi = 0.0
    else:
        lo = hi = None  # unused

    rendered: list[str] = []
    for series in series_list:
        if not series:
            rendered.append("")
            continue
        data = list(series)
        if width is not None and width > 0 and len(data) > width:
            data = _downsample(data, width)
        if share_scale:
            rendered.append(_glyph_ramp_fixed(data, chars, lo, hi))
        else:
            rendered.append(_glyph_ramp(data, chars))

    if labels is None:
        return "\n".join(rendered)

    pad = max(len(label) for label in labels)
    return "\n".join(
        f"{label.ljust(pad)}  {row}" for label, row in zip(labels, rendered)
    )


def sparkline_with_axis(
    values: list[float],
    *,
    width: int | None = None,
    chars: str = _DEFAULT_CHARS,
) -> str:
    """Render a sparkline with min/max axis labels on either side.

    Returns ``"<min> →<sparkline>← <max>"``. The numeric labels show
    the original data extremes (before any downsampling). Empty input
    → ``""``.
    """
    if not values:
        return ""
    lo = min(values)
    hi = max(values)
    spark = sparkline(values, width=width, chars=chars)
    return f"{_fmt_num(lo)} →{spark}← {_fmt_num(hi)}"


def _fmt_num(v: float) -> str:
    if isinstance(v, int) or (isinstance(v, float) and v.is_integer()):
        return f"{int(v)}"
    return f"{v:.1f}"


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


def _glyph_ramp_fixed(values: list[float], chars: str, lo: float, hi: float) -> str:
    """Like ``_glyph_ramp`` but uses a caller-supplied lo/hi span."""
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
