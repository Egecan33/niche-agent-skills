---
name: openapi-contract-probes
description: Plan and triage Schemathesis OpenAPI edge-case and response-contract tests against an explicitly authorized disposable API. Use for schema-driven failures and reproducible contract regressions; not load testing or unsanctioned production fuzzing.
---

# OpenAPI contract probes

Schemathesis generates requests and checks API behavior. This skill adds target boundaries, contract-versus-product triage, and a regression evidence bundle. See [source evidence](references/source.md).

## Inputs and readiness

Obtain the exact OpenAPI document/revision, authorized base URL, operation allowlist, disposable data policy, request budget, and expected business constraints. Runtime needs a reviewed Schemathesis installation and a reachable test API. Without them, produce a test plan and inspect supplied request/response artifacts; do not claim fuzzing ran.

## Workflow

1. Validate that the schema's servers, external references, links, redirects, and auth setup stay inside the permitted target. A local schema can still name a remote service. Restrict outbound requests at the test environment boundary where possible.
2. Pick representative constraints: missing/extra fields, nullability, numeric bounds, enum values, Unicode, and response content type/status/body. Include the valid baseline and avoid treating a single successful request as coverage.
3. Inspect the installed CLI's help before selecting current options for operations, rate, duration/example limits, and seeds. Pin the chosen version and record the exact effective settings. Do not default to a broad run over all destructive endpoints.
4. Run only in the approved disposable target. Capture failure ID, operation, sanitized request/response, seed/reproduction data, schema hash, and environment. Preserve shrinking/minimization artifacts where supported.
5. Classify each failure: implementation violates contract, schema mismodels intended behavior, auth/setup issue, or unresolved business rule. A generated invalid input need not map to one invented universal 4xx code; use the documented contract and explicit rule.
6. Reproduce the minimized case and add a focused regression check when requested. State what was untested and what the request budget limits.

## Boundaries and output

Generated calls can create, change, or delete data, including through nominal GET endpoints with side effects. No live credentials, customer data, external-reference fetches, or real target execution without scope support. Do not replay a supplied shell command without inspecting it.

Deliver the bounded plan or executed report, contract evidence, reproducer, and gaps. Use [example](references/example.md) and [synthetic case](assets/case.json). Offline fixture checks are not Schemathesis results or an authorization audit.
