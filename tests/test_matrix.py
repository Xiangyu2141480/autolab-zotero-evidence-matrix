import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from zotero_evidence_matrix.matrix import build_matrix


def test_build_matrix_groups_rows_and_keeps_citekeys(tmp_path):
    source = tmp_path / "notes.csv"
    source.write_text(
        "title,citekey,topic,claim,limitation\n"
        "A,a2024,Methods,Useful,Small sample\n",
        encoding="utf-8",
    )

    assert build_matrix(source)[0].citekey == "a2024"


def test_build_matrix_rejects_a_missing_required_header(tmp_path):
    from zotero_evidence_matrix.matrix import MatrixValidationError

    source = tmp_path / "notes.csv"
    source.write_text(
        "title,citekey,topic,claim\nA,a2024,Methods,Useful\n",
        encoding="utf-8",
    )

    with pytest.raises(MatrixValidationError, match="Missing required CSV columns: limitation"):
        build_matrix(source)


def test_build_matrix_rejects_a_whitespace_only_required_value(tmp_path):
    from zotero_evidence_matrix.matrix import MatrixValidationError

    source = tmp_path / "notes.csv"
    source.write_text(
        "title,citekey,topic,claim,limitation\nA,a2024,Methods,   ,Small sample\n",
        encoding="utf-8",
    )

    with pytest.raises(
        MatrixValidationError,
        match="Blank required value for 'claim' in row 2",
    ):
        build_matrix(source)
