# Zotero Evidence Matrix

Convert a constrained, local Zotero-note CSV into a topic-grouped Markdown evidence matrix.

## Run

Requires Python 3.11 or newer. From a checkout, install the package and its development tools:

```powershell
python -m pip install -e ".[dev]"
python -m zotero_evidence_matrix examples/notes.csv evidence-matrix.md
```

The input and output must be different paths. Invalid CSV data is reported concisely on standard error and produces a nonzero exit code.

## CSV schema

The header must include these nonblank columns:

`title,citekey,topic,claim,limitation`

Optional columns are `authors` and `year`. Citekeys may contain letters, numbers, `.`, `_`, `:`, `+`, and `-`; topics cannot contain line breaks. See [examples/notes.csv](examples/notes.csv) for synthetic sample data.

## Data safety

This program processes files only on the local machine. It makes no network requests, sends no data to external services, and does not access Zotero directly. Use only CSVs you are permitted to process; the included example is synthetic.

## License

MIT. See [LICENSE](LICENSE).
