# Example: source-supported refund window

Wholly synthetic source `policy-01@v1`, section 1: “Unopened items can be returned within 14 days.” Source group `returns-policy` belongs to evaluation only.

Expected accepted row:

```json
{"id":"q1","source_id":"policy-01","source_revision":"v1","evidence":"section-1","question":"How long is the unopened-item return window?","answer":"14 days","answerable":true,"split":"eval","source_group":"returns-policy","generation":"hand-authored synthetic pilot"}
```

Reject a row answering “30 days” even if its schema and citation exist. Add “What is the return shipping fee?” with an abstention because the source says nothing about it. A paraphrase of q1 generated from the same source group cannot be moved into train.

A real Curator implementation may subclass `curator.LLM`, define `prompt` and `parse`, and use a structured response format. This package does not ship a live model client or a hidden default provider. Select and authorize the provider and budget separately, then test the adapter against the pinned API before claiming integration.

The fixture source contains a locator-to-text inventory; a row must name an existing, nonempty source section. Hand-reviewed answers for this teaching source live outside the installed skill in the repository's evaluator-only `evals/oracles/teaching.json`. The offline equality check is deliberately narrow; neither locator existence nor answer equality automates general semantic entailment.
