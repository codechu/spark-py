"""Tests for codechu_spark.sparkline."""

from __future__ import annotations

import pytest

from codechu_spark import sparkline


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
