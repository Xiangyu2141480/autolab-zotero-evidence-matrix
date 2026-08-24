# Public Exposure Audit — 2026-08-24

## Verdict

**Do not change visibility yet.** The source files below are suitable for a public review, but the currently reachable Git history would also reveal commit metadata. In particular, the squash merge commit has an author display name and GitHub noreply address. Rewriting history is prohibited by studio policy, so this identity exposure requires explicit user acceptance before any public release.

## Files that a public `main` would expose

```
.github/workflows/ci.yml
.gitignore
LICENSE
README.md
docs/superpowers/plans/2026-08-24-zotero-evidence-matrix.md
docs/superpowers/specs/2026-08-24-zotero-evidence-matrix-design.md
examples/notes.csv
pyproject.toml
src/zotero_evidence_matrix/__init__.py
src/zotero_evidence_matrix/__main__.py
src/zotero_evidence_matrix/matrix.py
tests/test_matrix.py
```

If this release-readiness branch is merged, these additional files would also be public:

```
docs/DEMO_60_SECONDS.md
docs/FEEDBACK_TEMPLATE.md
docs/PUBLIC_EXPOSURE_AUDIT.md
docs/RECRUITMENT_DRAFT.md
docs/VALIDATION_LEDGER.md
examples/expected-matrix.md
```

## Reachable history before this PR

| Commit | Subject |
|---|---|
| `b840296` | docs: define zotero evidence matrix MVP |
| `cb2137e` | chore: ignore local development artefacts |
| `432b516` | Add CSV evidence matrix parser |
| `60d8a17` | Record matrix parser TDD evidence |
| `46c91e8` | Validate required evidence CSV fields |
| `a012c85` | Render grouped Markdown evidence matrix |
| `3a39d15` | Reject Markdown injection in topics and citekeys |
| `8ee4a9c` | Add local evidence matrix CLI |
| `30f6721` | Validate duplicate and malformed evidence CSV data |
| `16e7dd6` | Pin audited build backend baseline |
| `44cb0bb` | Harden markdown headings and CLI file errors |
| `7f6a4e1` | Verify release artifacts in CI |
| `a0b7593` | feat: add local Zotero evidence matrix CLI (#1) |

The remote feature branch makes the detailed commits reachable today; changing repository visibility would expose both it and `main`. No history rewrite, force-push, or remote deletion is authorised.

## Scan results and license review

- Full reachable-history credential regex scan: no matches.
- Full reachable-history file-content email scan: no matches. Git commit metadata is separately flagged above.
- `git fsck --full --no-reflogs`: clean.
- Tracked files contain source code, synthetic CSV data, tests, documentation, CI configuration, and one MIT license. No third-party images, datasets, model weights, copied papers, or proprietary input files are tracked.
- The included sample author name is explicitly synthetic. Do not replace it with a real person.
