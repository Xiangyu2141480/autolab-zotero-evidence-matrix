# Zotero Evidence Matrix

Convert a constrained, local Zotero-note CSV into a topic-grouped Markdown evidence matrix.

## Quickstart (first run)

Requires Python 3.11 or newer. From a fresh checkout, create an isolated environment, install, and run the synthetic example:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m zotero_evidence_matrix examples\notes.csv evidence-matrix.md
Get-Content evidence-matrix.md
```

The command produces a topic-grouped Markdown table like [examples/expected-matrix.md](examples/expected-matrix.md). The input and output must be different paths. Invalid CSV data is reported concisely on standard error and produces a nonzero exit code.

For a 60-second walkthrough, use [the demo script](docs/DEMO_60_SECONDS.md). The validation materials are private preparation only; this project is not currently public or collecting feedback.

## CSV schema

The header must include these nonblank columns:

`title,citekey,topic,claim,limitation`

Optional columns are `authors` and `year`. Citekeys may contain letters, numbers, `.`, `_`, `:`, `+`, and `-`; topics cannot contain line breaks. See [examples/notes.csv](examples/notes.csv) for synthetic sample data.

## Data safety

This program processes files only on the local machine. It makes no network requests, sends no data to external services, and does not access Zotero directly. Use only CSVs you are permitted to process; the included example is synthetic.

## License

MIT. See [LICENSE](LICENSE).
