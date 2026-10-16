# Niche Agent Skills

Seven evidence-focused workflows for Claude Code and Codex, built around useful open-source tools. Catch a changed tool argument, a cross-tenant row leak, a misleading trace calculation, or a PDF cell that cannot be traced back to the page.

**Version 0.1.0 — early release.** The skills, examples, and offline checks are ready for review and local use. Real Claude/Codex discovery and behavioral evaluations have **not** been run. Upstream integrations have **not** been executed. This repository supplies instructions and synthetic teaching cases; it does not install the seven tools or include API access.

## Pick a workflow

| Skill | Useful when | Tool foundation |
| --- | --- | --- |
| [agent-trajectory-regression](skills/agent-trajectory-regression/SKILL.md) | The final answer is correct, but tool order or arguments regressed | AgentEvals |
| [postgres-tenant-isolation](skills/postgres-tenant-isolation/SKILL.md) | Tenant isolation needs positive and negative role/operation checks | pgTAP |
| [openapi-contract-probes](skills/openapi-contract-probes/SKILL.md) | Generated edge cases need a bounded target and reproducible triage | Schemathesis |
| [trace-failure-diagnosis](skills/trace-failure-diagnosis/SKILL.md) | Agent/RAG traces contain overlapping spans, errors or retries | OpenInference |
| [masked-session-to-sop](skills/masked-session-to-sop/SKILL.md) | A consented, sanitized UI session should become an evidenced SOP | rrweb |
| [grounded-synthetic-datasets](skills/grounded-synthetic-datasets/SKILL.md) | Synthetic QA needs provenance, abstentions and leakage controls | Curator |
| [pdf-table-evidence](skills/pdf-table-evidence/SKILL.md) | Every extracted table cell needs a page and coordinate trail | pdfplumber |

Each directory contains `SKILL.md`, a worked input/output example, pinned source evidence, and a synthetic case with passing and failing controls. Our workflows are independently authored; they are not upstream-endorsed features. [Sources and attribution](docs/SOURCES.md) separate tool capabilities from the workflow added here.

## Start locally

Requires Python 3.10+ only for the repository's offline checks:

```sh
python3 scripts/validate_package.py
python3 scripts/check_fixture.py
python3 -m unittest discover -s tests -v
```

These commands do not contact services or install dependencies. Passing them means package/fixture invariants passed, not that a model followed the skill or a real tool integration works. See [evaluation](docs/EVALUATION.md) and the [validation record](docs/VALIDATION.md).

Review a selected skill, then manually copy its complete directory to a host's local skill location using the [installation guide](docs/INSTALLATION.md). Do not overwrite an existing directory without inspecting it. No installer changes your configuration automatically.

Try an explicit request after installation:

```text
Claude Code: /agent-trajectory-regression Compare these sanitized traces. Protect call order and amount=12; do not replay tools.
Codex CLI/IDE: $agent-trajectory-regression Compare these sanitized traces. Protect call order and amount=12; do not replay tools.
```

Use one matching skill at a time. If a required dependency or artifact is missing, the skill prepares a bounded plan or manual analysis and reports what was not run.

## Trust and reuse

Examples contain only original synthetic data. Skills grant no tools or credentials and define boundaries for database tests, API calls, telemetry, recording, generation and PDF processing. Review source artifacts as untrusted data before any execution.

Original skill instructions, scripts, tests, and synthetic examples are licensed under [MIT](LICENSE). Reproduced upstream license notices keep their own terms and copyright; they are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). No upstream implementation or example code is vendored. Each source is pinned in [sources.lock.json](sources.lock.json), including the exact files and license scope reviewed.

Public source distribution is separate from plugin catalog distribution. No plugin catalog submission or real-runtime certification is claimed. The earlier general-purpose draft is retained outside this repository and is not part of the release.

[Türkçe rehber](docs/KULLANIM-TR.md) · [Compatibility](docs/COMPATIBILITY.md) · [Contributing](CONTRIBUTING.md)
