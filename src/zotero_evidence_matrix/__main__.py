"""Command-line entry point for the local evidence-matrix generator."""

import argparse
import sys
from pathlib import Path

from .matrix import MatrixValidationError, build_matrix, render_matrix


def main() -> int:
    """Convert one evidence CSV into a Markdown matrix."""
    parser = argparse.ArgumentParser(description="Render a CSV evidence matrix as Markdown.")
    parser.add_argument("input", type=Path, metavar="INPUT.csv")
    parser.add_argument("output", type=Path, metavar="OUTPUT.md")
    arguments = parser.parse_args()

    if arguments.input.resolve() == arguments.output.resolve():
        print("Input and output paths must differ", file=sys.stderr)
        return 2

    try:
        rendered = render_matrix(build_matrix(arguments.input))
    except MatrixValidationError as error:
        print(error, file=sys.stderr)
        return 2

    arguments.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
