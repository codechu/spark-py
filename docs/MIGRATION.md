# Migration guide

## 0.1 → 0.2

**Short version:** nothing changes for callers. The public API,
return values, and edge-case behavior are identical. The 0.2 release
is an internal refactor only.

### What changed

`sparkline` and `heatmap` previously duplicated the same min/max
linear-scaling-to-glyph-ramp loop. In 0.2 that logic moved to a
single private helper:

```python
# codechu_spark/_helpers.py
def _glyph_ramp(values: list[float], chars: str) -> str:
    ...
```

`sparkline` and `heatmap` now both delegate to `_glyph_ramp` after
their own input validation and (in `sparkline`'s case) optional
downsampling.

### What did **not** change

| Aspect                                 | Status      |
| -------------------------------------- | ----------- |
| Function names and import paths        | unchanged   |
| Signatures (positional + keyword args) | unchanged   |
| Default `chars` ramps                  | unchanged   |
| Return types and exact glyph output    | unchanged   |
| Empty / all-equal / single-value behavior | unchanged |
| `ValueError` on empty `chars`          | unchanged   |
| `ValueError` on `NaN` in input         | unchanged   |
| `bar_chart` (entirely)                 | unchanged   |

### How we verified

The existing test suite (which pins exact-string outputs for every
public function, including edge cases) passes against 0.2 without
modification. No test was loosened or removed in the refactor.

### Action required

None. Upgrade with:

```bash
pip install -U codechu-spark
```

If you were importing private names (e.g. anything starting with
`_`), they may have moved — but you weren't, right?

### Why the refactor

- Shrinks `sparkline.py` and `heatmap.py` to their renderer-specific
  concerns.
- Makes the scaling algorithm easy to audit in one place.
- Sets up a clean seam for future shared concerns (e.g. percentile
  clipping, log scaling) without re-introducing duplication.

See [CHANGELOG.md](../CHANGELOG.md) for the release entry.
