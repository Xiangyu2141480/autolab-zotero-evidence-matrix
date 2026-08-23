"""CSV parsing for a local evidence matrix."""

import csv
from dataclasses import dataclass
from pathlib import Path


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
        return [EvidenceRow(**row) for row in csv.DictReader(source_file)]
