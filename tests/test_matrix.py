import sys
from pathlib import Path

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
