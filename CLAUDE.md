# CLAUDE.md — codechu-spark

Bootstrap per `codechu-org/ai/AGENTS.md` §0 before any work. Prefer
the local clone at `$org_home/codechu-org/ai/AGENTS.md` (if
`~/.config/codechu/config.toml` has `org_home` set); otherwise
WebFetch the public raw URL
<https://raw.githubusercontent.com/codechu/codechu-org/main/ai/AGENTS.md>.
This file lists only product-local overrides.

## Product-local notes

- Pure stdlib text-visualization library. **No** external runtime
  dependencies.
- Public API: `sparkline`, `bar_chart`, `heatmap`.
- Functions return plain strings only — no terminal control codes,
  no ANSI colors, no cursor movement. Colorization is the caller's
  job (see `codechu-cli`).
- Output glyphs are part of the public contract via the default
  `chars` argument. Changing a default glyph requires a major
  version bump.
- Coverage target: ≥90 %.

## Discipline reminders (org rules apply)

- Conventional Commits, no AI signature.
- No `--no-verify`, no force push, no unapproved publish.
- See `codechu-org/ai/AGENTS.md` for the full list.
