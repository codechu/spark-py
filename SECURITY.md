# Security policy

`codechu-spark` is a pure-stdlib text-rendering library. Its public
functions take lists of numbers and return strings — no I/O, no
subprocess, no deserialization, no ANSI escape emission.

## Supported versions

| Version | Supported |
|---|:---:|
| `main` branch | ✅ |
| Latest minor release (0.x) | ✅ |
| Older releases | ❌ |

## Reporting a vulnerability

### Preferred path — GitHub Security Advisory (private)

Open a **private** advisory at
[github.com/codechu/codechu-spark-py/security/advisories/new](https://github.com/codechu/codechu-spark-py/security/advisories/new).

### Alternative — Email

Write to `security@codechu.com`.

## Scope — what to report

**In scope:**

- Uncaught exceptions on valid inputs (NaN, ±inf, empty, very long
  lists).
- Resource exhaustion — bounded-time rendering becoming unbounded on
  adversarial inputs (e.g. enormous `width` or `chars` parameters).
- Caller-supplied `chars` that escape the renderer's output as
  terminal-control sequences (we make no effort to sanitize, but it
  shouldn't crash us either).

**Out of scope:**

- Visual rendering bugs (squashed gradients, misaligned bars). File
  those as regular issues.
- Terminal interpretation of the output (e.g. font missing the
  default glyphs). That's a font / terminal issue.

## Process

Reports are reviewed on a best-effort basis — no fixed SLA. We aim
for coordinated disclosure within **90 days** of the report.

## Public disclosure

Once a confirmed fix is released:

- A summary is added to the CHANGELOG under the `### Security`
  category.
- A GitHub Security Advisory is published.
- If a CVE was assigned, its number is referenced.
