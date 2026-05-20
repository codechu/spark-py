"""Tests for codechu_spark.heatmap."""

from __future__ import annotations

import pytest

from codechu_spark import heatmap


def test_empty():
    assert heatmap([]) == ""


def test_all_equal():
    s = heatmap([5, 5, 5, 5])
    assert len(s) == 4
    assert len(set(s)) == 1
    assert s[0] == " "  # first glyph of default chars


def test_gradient_default():
    s = heatmap([0, 1, 2, 3, 4])
    chars = " ░▒▓█"
    assert s[0] == chars[0]
    assert s[-1] == chars[-1]
    assert len(s) == 5


def test_custom_chars():
    s = heatmap([0, 5, 10], chars=".oO")
    assert s[0] == "."
    assert s[-1] == "O"


def test_empty_chars_raises():
    with pytest.raises(ValueError):
        heatmap([1, 2, 3], chars="")


def test_single_value():
    s = heatmap([42])
    assert s == " "


def test_negative_values():
    s = heatmap([-3, 0, 3])
    chars = " ░▒▓█"
    assert s[0] == chars[0]
    assert s[-1] == chars[-1]
