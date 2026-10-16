---
name: pdf-table-evidence
description: Extract or audit PDF tables with pdfplumber and preserve page, table/cell coordinates, raw text, and visual evidence. Use when every exported value needs a verifiable PDF location; not OCR-only scans or unsupported precision claims.
---

# PDF tables with coordinate evidence

pdfplumber supplies PDF object inspection, table finding and visual debugging. This workflow adds a reproducible evidence ledger and ambiguity review. Read [source evidence](references/source.md).

## Inputs and readiness

Obtain a permitted PDF, its hash, required pages/tables/columns and output schema. Treat extraction settings as part of the result. Runtime requires a reviewed pdfplumber installation; visual verification needs a renderer/viewer. The library has no OCR engine. For scans or missing text, report the need for a separately approved OCR workflow rather than inventing cell values.

## Workflow

1. Inspect page dimensions, rotation, crop box and available text/lines. Identify target tables by evidence; the largest table is not necessarily the requested table.
2. Use table objects from `find_tables` where coordinate evidence is needed. Record full-page coordinates `(x0, top, x1, bottom)` in PDF points, page number convention (1-based), crop origin and any coordinate transform. Do not mix bottom-origin `y0/y1` with top-origin `top/bottom`.
3. Align extracted rows with table row/cell geometry. Preserve null/merged cells, repeated headers and continuation pages explicitly. Do not shift cells left to hide a missing value.
4. Store each cell's raw text, normalized value, unit/locale rule, page and bbox, table/row/column identity, settings/version, and review state. Keep raw numbers and normalized numbers separate; distinguish a blank from zero and a dash from a missing value.
5. Render or inspect the page with a table overlay/crop and verify alignment. Reconcile row counts and totals only when the source defines them. Record discrepancies and unreadable cells rather than forcing a plausible total.
6. Deliver structured data and its evidence ledger. If visual review or extraction did not run, mark it not run; a JSON coordinate check alone cannot establish that the PDF contains the value.

## Boundaries and output

Do not bypass encryption, upload private PDFs, run embedded PDF actions, or expose document metadata unnecessarily. Keep extraction read-only and derived outputs separate from the original. A file hash identifies bytes and does not grant permission to process them.

Use [example](references/example.md) and [synthetic case](assets/case.json). The fixture is a mock table-object export, not an actual PDF extraction; the local tests do not invoke pdfplumber or validate rendering.
