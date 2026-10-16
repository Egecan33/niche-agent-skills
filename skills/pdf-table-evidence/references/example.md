# Example: a verifiable cell

Input: a machine-generated synthetic page, width 612 and height 792 PDF points, unrotated and uncropped. A two-column table has bbox `[40,100,240,160]`; the quantity cell is `[140,120,240,140]`, raw text `1,250`, with an explicit en-US integer grouping rule.

Illustrative output:

```json
{"page":1,"table_id":"t1","row":1,"column":1,"bbox":[140,120,240,140],"coordinate_system":"x0-top-x1-bottom-pdf-points","raw_text":"1,250","normalized_value":1250,"visual_review":"not_run"}
```

Reject evidence with an out-of-page or reversed bbox, an unknown coordinate system, or a page number using an undeclared convention. Geometry must be tied to the table cell, not just a broad page box. A valid bbox does not prove the text, grouping rule or row association is correct.

A real integration would open the permitted PDF, inspect the target page, call `find_tables(table_settings=...)`, pair `Table.extract()` rows with `Table.rows` cell geometry and preserve both. Inspect a debug overlay using the library's image/table debugging facilities or a trusted renderer. These are integration steps to execute later, not results from this draft. Never claim the mock fixture was rendered or extracted.
