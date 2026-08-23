# Zotero Evidence Matrix Design

## Goal

Turn a local CSV of researcher-authored paper notes into a Markdown evidence matrix grouped by topic, retaining the supplied cite key. The tool never makes network calls and does not interpret or generate research content.

## Interface

`python -m zotero_evidence_matrix INPUT.csv OUTPUT.md`

The required CSV columns are `title`, `citekey`, `topic`, `claim`, and `limitation`; optional columns are `authors` and `year`. Rows are grouped by trimmed topic in case-insensitive alphabetical order. Each row renders one Markdown table entry with `[@citekey]`; fields are escaped to keep table structure valid.

## Errors and safety

Missing headers, blank required values, duplicate cite keys within a topic, malformed CSV input, or an output path equal to the input path return a non-zero exit and a concise error. The tool only reads the explicit input path and writes the explicit output path. It neither retains source content nor contacts a service.

## Testing

Tests cover a valid two-topic conversion, Markdown escaping, missing required data, malformed CSV mapping, duplicate keys in one topic, concise CLI validation errors, and input/output path collision. A fixture is synthetic and contains no personal data.
