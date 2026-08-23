import sys
import os
from pathlib import Path
from subprocess import run

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


def test_build_matrix_rejects_a_duplicate_citekey_within_a_topic(tmp_path):
    source = tmp_path / "notes.csv"
    source.write_text(
        "title,citekey,topic,claim,limitation\n"
        "A,a2024,Methods,Useful,Small sample\n"
        "B,a2024,Methods,Replicable,Single site\n",
        encoding="utf-8",
    )

    with pytest.raises(
        MatrixValidationError,
        match="Duplicate citekey 'a2024' in topic 'Methods'",
    ):
        build_matrix(source)


def test_build_matrix_maps_malformed_csv_to_a_validation_error(tmp_path):
    source = tmp_path / "notes.csv"
    source.write_text(
        "title,citekey,topic,claim,limitation\n"
        '"Unclosed,a2024,Methods,Useful,Small sample\n',
        encoding="utf-8",
    )

    with pytest.raises(MatrixValidationError, match="Malformed CSV:"):
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


def test_module_cli_writes_a_rendered_matrix(tmp_path):
    source = tmp_path / "notes.csv"
    destination = tmp_path / "matrix.md"
    source.write_text(
        "title,citekey,topic,claim,limitation\n"
        "A paper,a2024,Methods,Useful,Small sample\n",
        encoding="utf-8",
    )

    environment = os.environ | {"PYTHONPATH": str(Path(__file__).parents[1] / "src")}
    result = run(
        [sys.executable, "-m", "zotero_evidence_matrix", str(source), str(destination)],
        capture_output=True,
        encoding="utf-8",
        env=environment,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert destination.read_text(encoding="utf-8") == (
        "## Methods\n\n"
        "| Title | Claim | Limitation | Citation |\n"
        "| --- | --- | --- | --- |\n"
        "| A paper | Useful | Small sample | [@a2024] |\n"
    )


def test_module_cli_rejects_matching_input_and_output_paths(tmp_path):
    source = tmp_path / "notes.csv"
    source.write_text(
        "title,citekey,topic,claim,limitation\n"
        "A paper,a2024,Methods,Useful,Small sample\n",
        encoding="utf-8",
    )

    environment = os.environ | {"PYTHONPATH": str(Path(__file__).parents[1] / "src")}
    result = run(
        [sys.executable, "-m", "zotero_evidence_matrix", str(source), str(source)],
        capture_output=True,
        encoding="utf-8",
        env=environment,
        check=False,
    )

    assert result.returncode != 0
    assert result.stderr.strip() == "Input and output paths must differ"


def test_module_cli_reports_validation_errors_concisely(tmp_path):
    source = tmp_path / "notes.csv"
    destination = tmp_path / "matrix.md"
    source.write_text(
        "title,citekey,topic,claim\nA,a2024,Methods,Useful\n",
        encoding="utf-8",
    )

    environment = os.environ | {"PYTHONPATH": str(Path(__file__).parents[1] / "src")}
    result = run(
        [sys.executable, "-m", "zotero_evidence_matrix", str(source), str(destination)],
        capture_output=True,
        encoding="utf-8",
        env=environment,
        check=False,
    )

    assert result.returncode != 0
    assert result.stdout == ""
    assert result.stderr.strip() == "Missing required CSV columns: limitation"
