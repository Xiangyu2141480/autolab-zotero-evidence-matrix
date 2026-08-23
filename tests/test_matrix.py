import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from zotero_evidence_matrix.matrix import (
    EvidenceRow,
    MatrixValidationError,
    build_matrix,
    render_matrix,
)


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


def test_render_matrix_groups_topics_in_case_insensitive_order_and_keeps_citekeys():
    rows = [
        EvidenceRow("Z paper", "z2024", "zebra", "Last", "Limited"),
        EvidenceRow("A paper", "a2024", "  Alpha  ", "First", "Limited"),
    ]

    rendered = render_matrix(rows)

    assert rendered.index("## Alpha") < rendered.index("## zebra")
    assert "| A paper | First | Limited | [@a2024] |" in rendered
    assert "| Z paper | Last | Limited | [@z2024] |" in rendered


def test_render_matrix_escapes_pipes_and_line_breaks_in_table_cells():
    row = EvidenceRow(
        "A | paper\nrevised",
        "a2024",
        "Methods",
        "Claim | detail\ncontinued",
        "A\nlimitation | note",
    )

    rendered = render_matrix([row])

    assert "| A \\| paper<br>revised | Claim \\| detail<br>continued | A<br>limitation \\| note | [@a2024] |" in rendered


def test_render_matrix_rejects_a_topic_containing_a_line_break():
    row = EvidenceRow("Paper", "safe2024", "Methods\n## Injected", "Claim", "Limit")

    with pytest.raises(MatrixValidationError, match="Topic may not contain line breaks"):
        render_matrix([row])


def test_render_matrix_rejects_a_citekey_outside_the_safe_grammar():
    row = EvidenceRow("Paper", "safe]\n[@injected", "Methods", "Claim", "Limit")

    with pytest.raises(MatrixValidationError, match="Citekey contains unsafe characters"):
        render_matrix([row])
