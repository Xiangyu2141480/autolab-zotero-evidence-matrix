# Zotero Evidence Matrix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local CLI that converts a constrained Zotero-note CSV into a citation-linked Markdown evidence matrix.

**Architecture:** A small standard-library Python package separates CSV validation/parsing from Markdown rendering. The CLI calls that library, reports domain errors to stderr, and writes only the requested output path.

**Tech Stack:** Python 3.11+, standard library, pytest, Ruff, pip-audit, GitHub Actions.

---

### Task 1: CSV model and validation

**Files:**
- Create: `tests/test_matrix.py`
- Create: `src/zotero_evidence_matrix/matrix.py`

- [x] **Step 1: Write a failing test**

```python
def test_build_matrix_groups_rows_and_keeps_citekeys(tmp_path):
    source = tmp_path / "notes.csv"
    source.write_text("title,citekey,topic,claim,limitation\nA,a2024,Methods,Useful,Small sample\n", encoding="utf-8")
    assert build_matrix(source)[0].citekey == "a2024"
```

- [x] **Step 2: Run it to verify it fails**

Run: `python -m pytest tests/test_matrix.py -q`
Expected: an import failure because the package does not yet exist.

- [x] **Step 3: Write minimal implementation**

```python
@dataclass(frozen=True)
class EvidenceRow: ...

def build_matrix(source: Path) -> list[EvidenceRow]: ...
```

- [x] **Step 4: Run the test to verify it passes**

Run: `python -m pytest tests/test_matrix.py -q`
Expected: `1 passed`.

Execution evidence: `python -m pytest tests/test_matrix.py -q` first failed with `ModuleNotFoundError: No module named 'zotero_evidence_matrix'` before the package existed; after implementation, the same command reported `1 passed in 0.07s`. Validation follow-up: `python -m pytest tests/test_matrix.py -q -k missing_required_header` and `python -m pytest tests/test_matrix.py -q -k whitespace_only_required_value` each first failed because `MatrixValidationError` did not exist; after implementation, `python -m pytest tests/test_matrix.py -q` reported `3 passed in 0.06s`.

### Task 2: Deterministic Markdown renderer

**Files:**
- Modify: `tests/test_matrix.py`
- Modify: `src/zotero_evidence_matrix/matrix.py`

- [x] **Step 1: Write failing rendering tests** for topic grouping, citekey rendering, and pipe escaping.
- [x] **Step 2: Run targeted tests** and confirm the expected missing-`render_matrix` import failure.
- [x] **Step 3: Implement `render_matrix(rows)`** with sorted topic headings and escaped table cells.
- [x] **Step 4: Run targeted tests** and confirm all pass.

Execution evidence: `python -m pytest tests/test_matrix.py -q -k render_matrix` first failed during test collection with `ImportError: cannot import name 'render_matrix'`, proving the requested API was absent. After the minimal renderer was added, the same command reported `2 passed, 3 deselected in 0.02s`; the full module test run reported `5 passed in 0.03s`.

### Task 3: CLI boundaries and documentation

**Files:**
- Modify: `tests/test_matrix.py`
- Create: `src/zotero_evidence_matrix/__main__.py`
- Create: `README.md`
- Create: `examples/notes.csv`
- Create: `.github/workflows/ci.yml`
- Create: `pyproject.toml`

- [ ] **Step 1: Write failing CLI tests** for output generation and rejected input/output collision.
- [ ] **Step 2: Run tests** and confirm failure because the CLI is absent.
- [ ] **Step 3: Implement CLI** to call the library, create a UTF-8 output, and return non-zero for domain errors.
- [ ] **Step 4: Add run instructions, data-safety disclosure, MIT license, synthetic example, and CI** running tests, Ruff, pip-audit, and credential-pattern scan.
- [ ] **Step 5: Run full verification**: `pytest -q`, `ruff check .`, `pip_audit`, `git diff --check`, and secret scan.
- [ ] **Step 6: Commit and push a branch; create a PR** after reviewing diff.

## Plan self-review

The three tasks cover each specified input/output behavior, all validation boundaries, no-network safety, test proof, documentation, license, and CI. The plan has no unbounded feature work; it is one local transformation only.
