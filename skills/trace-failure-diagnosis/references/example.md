# Example: overlapping children

Synthetic trace in milliseconds:

| Span | Parent | Kind | Start/end | Status |
| --- | --- | --- | --- | --- |
| root | none | AGENT | 0–100 | ERROR |
| retrieve | root | RETRIEVER | 10–70 | ERROR |
| model | root | LLM | 50–90 | UNSET |

Expected: root wall time 100 ms. Children occupy the union 10–90 = 80 ms, leaving 20 ms not covered by these immediate child intervals. Their inclusive durations total 100 ms but overlap by 20 ms. That sum is not request latency; the uncovered interval is not automatically CPU self-time. No p95 or exact backend cause can be inferred from this single trace.

Illustrative finding: “retrieve span reports ERROR; root also reports ERROR. Inspect a sanitized exception type and backend timing before assigning the failure to the index. The model overlaps the retriever; parent links alone do not prove a sequential dependency.”

Use raw OTel IDs and time units consistently when adapting an actual export. The fixture's `kind` and millisecond fields are a normalized teaching schema, not a wire-compatible OpenTelemetry export. OpenInference's `openinference.span.kind` supplies operation kind; parent/timing/status come from the tracing representation.
