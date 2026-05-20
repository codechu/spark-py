# Tests — codechu-spark

Run the suite from the repo root:

```bash
pytest -q
```

With coverage:

```bash
pytest --cov=codechu_spark --cov-report=term-missing
```

## Coverage gate

The coverage floor is **90 %**. PRs that drop below it are rejected;
add tests with your change.

## Conventions

- Cover edge cases on every renderer: empty input, single value,
  all-equal values, custom `chars`, `width<len`, `width>len`.
- Assert exact output strings — they're part of the public contract.
- No terminal control codes in output; if a test sees one, that's
  a regression.
