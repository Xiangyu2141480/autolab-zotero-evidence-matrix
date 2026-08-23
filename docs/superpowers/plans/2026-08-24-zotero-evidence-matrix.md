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

Security follow-up evidence: focused tests for a line-broken topic and a citekey containing `]` plus a line break first failed with `DID NOT RAISE`. The parser and renderer now share validation that rejects topics with line breaks and accepts citekeys only matching `[A-Za-z0-9][A-Za-z0-9_.:+-]*`; `python -m pytest tests/test_matrix.py -q` then reported `7 passed in 0.05s`.

### Task 3: CLI boundaries and documentation

**Files:**
- Modify: `tests/test_matrix.py`
- Create: `src/zotero_evidence_matrix/__main__.py`
- Create: `README.md`
- Create: `examples/notes.csv`
- Create: `.github/workflows/ci.yml`
- Create: `pyproject.toml`

- [x] **Step 1: Write failing CLI tests** for output generation and rejected input/output collision.
- [x] **Step 2: Run tests** and confirm failure because the CLI is absent.
- [x] **Step 3: Implement CLI** to call the library, create a UTF-8 output, and return non-zero for domain errors.
- [x] **Step 4: Add run instructions, data-safety disclosure, MIT license, synthetic example, and CI** running tests, Ruff, pip-audit, and credential-pattern scan.
- [x] **Step 5: Run full verification**: `pytest -q`, `ruff check .`, `pip_audit`, `git diff --check`, and secret scan.
- [x] **Step 6: Commit locally after reviewing diff.** No push or PR is authorized for this local-only task.

Execution evidence: First, `python -m pytest tests/test_matrix.py -q` reported `2 failed, 7 passed`; both failures said `No module named zotero_evidence_matrix.__main__`, confirming the CLI was absent. After adding `__main__.py`, the same command reported `9 passed in 0.30s`.

Verification evidence: `python -m pytest -q` reported `9 passed in 0.23s`; `python -m ruff check .` reported `All checks passed!`; `git diff --check` exited successfully; and the credential-pattern scan reported `credential scan: no matches`. The local interpreter has Ruff 0.4.10 and no `pip_audit` module, so an audit could not run locally without installing dependencies; the CI workflow installs and invokes the exact configured `pip-audit==2.10.0`.

Review repair evidence: duplicate citekeys within one trimmed topic and malformed quoted CSV each first failed (`DID NOT RAISE` and a non-malformed validation message, respectively); after strict parsing, `csv.Error` mapping, and duplicate detection, the focused run reported `2 passed, 10 deselected`. The concise CLI validation-error test already passed against the existing `MatrixValidationError` boundary. Following the authorized `python -m pip install -e '.[dev]'`, the pinned tools installed (`pytest 9.1.1`, `ruff 0.12.10`, `pip-audit 2.10.0`). Fresh checks reported `12 passed in 0.36s` and `All checks passed!`; `pip_audit` completed but reported `207 known vulnerabilities in 32` packages in the shared interpreter, including unrelated globally installed dependencies, and three packages it could not audit because they are not on PyPI. No production dependency is declared by this project.

Isolated audit repair evidence: the build backend requirement now pins `setuptools==84.0.0`, and CI upgrades both `pip` and `setuptools` before installing the project. In a fresh ignored `.venv`, `python -m pip install --upgrade pip setuptools` installed `pip 26.2.1` and `setuptools 84.0.0`; `python -m pip install -e '.[dev]'` installed the pinned development tooling. Fresh venv verification reported `12 passed in 0.38s`, `All checks passed!`, and `No known vulnerabilities found`. The auditor skips the local package because it is not published on PyPI, as expected.

Final quality repair evidence: tests for `[click](javascript:alert(1))` in a parsed/directly rendered topic heading and in CLI output, plus a missing-input CLI test, first reported three failures: two unsafe unescaped headings and one traceback. Topic headings now escape Markdown control punctuation, and CLI `OSError` boundaries report `Unable to read input file` or `Unable to write output file` with a nonzero status. The focused test run reported `3 passed, 12 deselected`; the full venv suite reported `15 passed in 0.60s` and Ruff reported `All checks passed!`.

## Plan self-review

The three tasks cover each specified input/output behavior, all validation boundaries, no-network safety, test proof, documentation, license, and CI. The plan has no unbounded feature work; it is one local transformation only.
