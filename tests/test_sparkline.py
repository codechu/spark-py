"""Tests for codechu_spark.sparkline."""

from __future__ import annotations

import pytest

from codechu_spark import multi_sparkline, sparkline, sparkline_with_axis


def test_empty():
    assert sparkline([]) == ""


def test_single_value():
    s = sparkline([5])
    # Single value → span=0 → first char
    assert s == "▁"


def test_all_equal():
    s = sparkline([5, 5, 5, 5])
    assert len(s) == 4
    assert len(set(s)) == 1
    assert s[0] == "▁"


def test_gradient():
    s = sparkline([0, 1, 2, 3, 4, 5, 6, 7])
    bars = "▁▂▃▄▅▆▇█"
    assert s[0] == bars[0]
    assert s[-1] == bars[-1]
    assert len(s) == 8


def test_downsample():
    s = sparkline(list(range(100)), width=10)
    assert len(s) == 10


def test_width_larger_than_input():
    # Width > len → no padding; render at input length.
    s = sparkline([1, 2, 3], width=10)
    assert len(s) == 3


def test_custom_chars():
    s = sparkline([0, 1, 2, 3], chars=".-=#")
    assert s[0] == "."
    assert s[-1] == "#"


def test_empty_chars_raises():
    with pytest.raises(ValueError):
        sparkline([1, 2, 3], chars="")


def test_negative_values():
    # Negative + positive mix still renders monotonically.
    s = sparkline([-5, 0, 5])
    bars = "▁▂▃▄▅▆▇█"
    assert s[0] == bars[0]
    assert s[-1] == bars[-1]


# --- v0.3.0: threshold coloring ---------------------------------------------

RED = "\x1b[31m"
YELLOW = "\x1b[33m"
GREEN = "\x1b[32m"
RESET = "\x1b[0m"


def test_threshold_coloring_bands():
    # values explicitly span all three bands.
    s = sparkline(
        [10, 50, 90],
        thresholds=[30, 70],
        colors=(GREEN, YELLOW, RED),
    )
    # 10 → green, 50 → yellow, 90 → red. Each glyph wrapped + reset.
    assert s.startswith(GREEN)
    assert YELLOW in s
    assert s.count(RESET) == 3
    # Order: green block before yellow before red.
    assert s.index(GREEN) < s.index(YELLOW) < s.index(RED)


def test_threshold_no_color_when_thresholds_none():
    # Backwards-compat: thresholds=None → identical to bare sparkline.
    assert sparkline([1, 2, 3]) == sparkline([1, 2, 3], thresholds=None, colors=None)


def test_threshold_requires_both_args():
    with pytest.raises(ValueError):
        sparkline([1, 2, 3], thresholds=[1, 2])
    with pytest.raises(ValueError):
        sparkline([1, 2, 3], colors=(RED, YELLOW, GREEN))


def test_threshold_coloring_all_below():
    s = sparkline([1, 2, 3], thresholds=[100, 200], colors=(GREEN, YELLOW, RED))
    # Every glyph wrapped in low color.
    assert s.count(GREEN) == 3
    assert YELLOW not in s
    assert RED not in s


# --- v0.3.0: multi_sparkline ------------------------------------------------


def test_multi_sparkline_shared_scale():
    # When sharing scale, the smaller series should not max out.
    out = multi_sparkline([[0, 1, 2], [0, 5, 10]], share_scale=True)
    lines = out.split("\n")
    assert len(lines) == 2
    # Second series spans the global range → ends on full block.
    assert lines[1][-1] == "█"
    # First series only reaches 2 out of 10 → does NOT end on full block.
    assert lines[0][-1] != "█"


def test_multi_sparkline_independent_scale():
    out = multi_sparkline([[0, 1, 2], [0, 5, 10]], share_scale=False)
    lines = out.split("\n")
    # Independent scaling → each series uses its full ramp.
    assert lines[0][-1] == "█"
    assert lines[1][-1] == "█"


def test_multi_sparkline_labels():
    out = multi_sparkline(
        [[1, 2, 3], [4, 5, 6]],
        labels=["cpu", "memory"],
    )
    lines = out.split("\n")
    assert lines[0].startswith("cpu   ")  # padded to "memory" width
    assert lines[1].startswith("memory")


def test_multi_sparkline_empty():
    assert multi_sparkline([]) == ""


def test_multi_sparkline_label_length_mismatch():
    with pytest.raises(ValueError):
        multi_sparkline([[1, 2], [3, 4]], labels=["only-one"])


# --- v0.3.0: sparkline_with_axis --------------------------------------------


def test_axis_labels_present():
    out = sparkline_with_axis([1, 2, 3, 4, 10])
    assert out.startswith("1 →")
    assert out.endswith("← 10")
    assert "▁" in out  # at least one glyph in between


def test_axis_empty():
    assert sparkline_with_axis([]) == ""


def test_axis_with_width():
    out = sparkline_with_axis(list(range(100)), width=10)
    # min=0, max=99
    assert out.startswith("0 →")
    assert out.endswith("← 99")
    # exactly 10 glyphs between arrows
    body = out.split("→", 1)[1].split("←", 1)[0]
    assert len(body) == 10


def test_axis_float_format():
    out = sparkline_with_axis([0.5, 1.0, 2.5])
    # 0.5 → "0.5", 2.5 → "2.5"
    assert out.startswith("0.5 →")
    assert out.endswith("← 2.5")
