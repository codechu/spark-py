"""Labeled horizontal mini bar chart."""

from __future__ import annotations

__all__ = ["bar_chart"]


def bar_chart(
    items: list[tuple[str, float]],
    *,
    width: int = 40,
    char: str = "█",
) -> str:
    """Render labeled bars as multi-line text.

    Each line looks like ``'label  ████████  value'``. Bar widths are
    scaled to the maximum value in ``items``. Returns a newline-joined
    string.

    - Empty input → ``''``.
    - All-zero or single-item input still renders sensibly (the lone
      bar shows full width).
    - Negative values are clipped to 0 for bar width purposes but the
      printed value is unchanged.
    """
    if not items:
        return ""
    if width < 1:
        raise ValueError("width must be ≥ 1")
    if not char:
        raise ValueError("char must be non-empty")

    label_w = max(len(label) for label, _ in items)
    max_v = max((v for _, v in items), default=0.0)
    if max_v <= 0:
        max_v = 1.0  # avoid div-by-zero; bars all render as empty

    lines: list[str] = []
    for label, value in items:
        clipped = max(0.0, value)
        bar_len = int(round(clipped / max_v * width))
        bar = char * bar_len
        value_str = _fmt_value(value)
        lines.append(f"{label:<{label_w}}  {bar:<{width}}  {value_str}")
    return "\n".join(lines)


def _fmt_value(v: float) -> str:
    # Integers render without a decimal point; floats keep one decimal.
    if isinstance(v, int) or v.is_integer():
        return str(int(v))
    return f"{v:.1f}"
