"""Tests for codechu_spark.bars."""

from __future__ import annotations

import pytest

from codechu_spark import bar_chart


def test_empty():
    assert bar_chart([]) == ""


def test_single_item():
    s = bar_chart([("a", 10.0)], width=10)
    assert "a" in s
    # max == value → full bar
    assert s.count("█") == 10


def test_multi_line():
    s = bar_chart([("alpha", 10.0), ("beta", 5.0)], width=10)
    lines = s.split("\n")
    assert len(lines) == 2
    # Bars proportional: 10 vs 5
    assert lines[0].count("█") == 10
    assert lines[1].count("█") == 5


def test_label_alignment():
    s = bar_chart([("a", 1.0), ("bbb", 2.0)], width=4)
    lines = s.split("\n")
    # Labels should be left-padded to max width (3)
    assert lines[0].startswith("a  ")
    assert lines[1].startswith("bbb")


def test_int_value_no_decimal():
    s = bar_chart([("a", 10)], width=4)
    assert s.endswith(" 10")


def test_float_value_one_decimal():
    s = bar_chart([("a", 10.5)], width=4)
    assert s.endswith("10.5")


def test_all_zero():
    s = bar_chart([("a", 0.0), ("b", 0.0)], width=10)
    # No bar characters
    assert "█" not in s


def test_negative_clipped_to_zero():
    s = bar_chart([("a", -5.0), ("b", 10.0)], width=10)
    lines = s.split("\n")
    assert lines[0].count("█") == 0
    assert lines[1].count("█") == 10


def test_custom_char():
    s = bar_chart([("a", 5.0)], width=5, char="#")
    assert s.count("#") == 5


def test_invalid_width():
    with pytest.raises(ValueError):
        bar_chart([("a", 1.0)], width=0)


def test_invalid_char():
    with pytest.raises(ValueError):
        bar_chart([("a", 1.0)], char="")
