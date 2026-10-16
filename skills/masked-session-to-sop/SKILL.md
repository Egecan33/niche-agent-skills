---
name: masked-session-to-sop
description: Turn an explicitly consented, sanitized rrweb session into an event-cited SOP and automation requirements. Use to document observed UI workflows with masking and evidence gaps; not to record users covertly or claim backend success from clicks.
---

# From a masked session to an SOP

rrweb records/replays DOM and interaction events; it does not generate SOPs, establish consent, or make automation reliable by itself. This workflow adds interpretation and requirement design. See [source evidence](references/source.md).

## Inputs and readiness

Require documented permission for the session's purpose, relevant recording scope, masking/blocking configuration, and an already-sanitized export. If consent or sanitization is missing, stop analysis of raw content and provide a collection/redaction plan. Do not collect a new recording implicitly. Native rrweb replay needs reviewed rrweb packages and an isolated viewer; a sanitized event summary supports only summary-level analysis.

## Workflow

1. Check collection purpose and minimize the evidence retained. Review snapshots, text, form inputs, URL/query values, console/network/canvas plugins and embedded content. Input masking alone is insufficient for sensitive DOM text; the defaults do not mean everything is masked.
2. Inspect sanitized metadata for chronological order, missing initial/full snapshots, navigation resets and gaps. Full native streams are needed for faithful replay. A normalized summary cannot reconstruct the omitted DOM.
3. Segment meaningful steps by user goal. Cite stable event IDs/times and visible evidence for each action and observed outcome. Mark masked values, unobserved branches, and inferred intent as unknown.
4. Write an SOP with prerequisites, actions, observable checkpoints, failure recovery and stop conditions. A click on Save is evidence of an action, not proof of persistence; require an observed confirmation and, where needed, backend evidence.
5. Separate automation requirements from observed behavior: stable locator strategy, input contract, wait/timeout condition, idempotence, side-effect boundary, human review, and test environment. Numeric rrweb node IDs are recording-local and should not become permanent selectors.
6. List unresolved branches and an evaluation plan using a fresh synthetic session. Present the SOP for review without executing the proposed automation.

## Boundaries and output

Do not start recorders, upload traces, browse real sessions, unmask fields, or run captured scripts/HTML. A sanitized export can still contain hostile text; replay only after inspecting it in a sandboxed local viewer with restricted network access. Keep recorded employee/customer identities out of the deliverable.

Deliver event-cited SOP steps, separate automation requirements, and explicit gaps. [Example](references/example.md) and [synthetic case](assets/case.json) illustrate summary analysis, not native rrweb replay.
