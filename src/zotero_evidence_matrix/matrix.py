"""CSV parsing for a local evidence matrix."""

import csv
from dataclasses import dataclass
from pathlib import Path

REQUIRED_COLUMNS = ("title", "citekey", "topic", "claim", "limitation")


class MatrixValidationError(ValueError):
    """Raised when an evidence-matrix CSV does not meet input requirements."""


@dataclass(frozen=True)
class EvidenceRow:
    title: str
    citekey: str
    topic: str
    claim: str
    limitation: str
    authors: str | None = None
    year: str | None = None


def build_matrix(source: Path) -> list[EvidenceRow]:
    """Read evidence rows from a UTF-8 CSV file."""
    with source.open("r", encoding="utf-8", newline="") as source_file:
        reader = csv.DictReader(source_file)
        fieldnames = reader.fieldnames or []
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
        if missing_columns:
            raise MatrixValidationError(
                f"Missing required CSV columns: {', '.join(missing_columns)}"
            )

        rows = []
        for row_number, row in enumerate(reader, start=2):
            required_values = {
                column: (row[column] or "").strip() for column in REQUIRED_COLUMNS
            }
            for column, value in required_values.items():
                if not value:
                    raise MatrixValidationError(
                        f"Blank required value for '{column}' in row {row_number}"
                    )
            optional_values = {
                column: row[column] for column in ("authors", "year") if column in row
            }
            rows.append(EvidenceRow(**required_values, **optional_values))

        return rows


def render_matrix(rows: list[EvidenceRow]) -> str:
    """Render validated evidence rows as a topic-grouped Markdown matrix."""
    groups: dict[str, list[EvidenceRow]] = {}
    for row in rows:
        topic = row.topic.strip()
        groups.setdefault(topic, []).append(row)

    sections = []
    for topic in sorted(groups, key=str.casefold):
        table_rows = [
            f"| {_escape_cell(row.title)} | {_escape_cell(row.claim)} | "
            f"{_escape_cell(row.limitation)} | [@{_escape_cell(row.citekey)}] |"
            for row in groups[topic]
        ]
        sections.append(
            "\n".join(
                [
                    f"## {topic}",
                    "",
                    "| Title | Claim | Limitation | Citation |",
                    "| --- | --- | --- | --- |",
                    *table_rows,
                ]
            )
        )
    return "\n\n".join(sections) + ("\n" if sections else "")


def _escape_cell(value: str) -> str:
    return (
        value.replace("|", "\\|")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "<br>")
    )
