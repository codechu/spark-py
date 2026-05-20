# Contributing to codechu-spark

Thanks for thinking about contributing. `codechu-spark` is a small
stdlib-only library for single-row text visualizations — sparklines,
labeled bar charts, heatmaps.

This library was originally extracted from [Disk Cleaner](https://github.com/codechu/disk-cleaner)
via [codechu/cli-py](https://github.com/codechu/cli-py), but is maintained
independently with its own release cadence.

## Development setup

```bash
git clone https://github.com/codechu/codechu-spark-py.git
cd codechu-spark-py
pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## Workflow

- Branch names: `feature/<short>`, `fix/<short>`, `refactor/<short>`,
  `docs/<short>`, `test/<short>`.
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).
- One change per PR.

## Tests

- `pytest -q` must pass; coverage stays at **≥90 %**.
- Cover the edge cases on every renderer: empty input, single
  value, all-equal values, custom `chars`, width < len, width > len.

## Public API discipline

The public surface is `sparkline`, `bar_chart`, and `heatmap`.
Default glyphs are part of the contract — changing them requires a
major version bump. Adding a new renderer is a minor bump.

No runtime dependencies. If you need one, the answer is almost
always "no, write it in stdlib".

## Style

- `ruff check` + `ruff format` clean.
- Type hints on public APIs (`from __future__ import annotations`).
- Renderers return strings — no `print`, no I/O, no ANSI escapes.

## Security

If you find a security issue, see [SECURITY.md](SECURITY.md) — do not
open a public issue for it.
