# Compatibility and dependencies

The portable entry point is YAML frontmatter plus Markdown. This package deliberately uses only `name` and `description`; names agree with directory names. Each skill's relative references and synthetic asset travel with it. See the [Agent Skills specification](https://agentskills.io/specification).

| Layer | What is established | What remains unverified |
| --- | --- | --- |
| Format | Local profile checks and bundled links | Official parser/runtime acceptance |
| Local discovery paths | Verified against host documentation | Actual Claude Code and Codex loading |
| Workflow examples | Original synthetic cases and negative controls | Model execution and trigger accuracy |
| Tool integrations | Pinned source/API references and explicit prerequisites | Installed-library behavior in this environment |
| Plugin distribution | Documented separately | Manifests, catalogs and submission |

No host variables, command interpolation, allowed-tools grants, hooks or MCP server configuration are bundled. Implicit selection remains controlled by the host.

## Execution prerequisites by workflow

| Workflow | Needed for real execution | Useful fallback |
| --- | --- | --- |
| Trajectory | AgentEvals and compatible message objects; optional judge requires a separate model client | Manual sanitized-trace comparison |
| Tenant isolation | Postgres, pgTAP, TAP runner, disposable schema/auth fixtures | Access matrix and SQL design |
| OpenAPI | Schemathesis, exact schema, authorized disposable API | Contract/probe plan and captured-response triage |
| Trace diagnosis | Sanitized export; instrumentation/exporter/backend only for new traces | Analyze supplied normalized spans |
| Session SOP | Consented sanitized export; rrweb runtime for native replay | Cite a sanitized summary with limitations |
| Synthetic datasets | Curator and an authorized inference backend for generation | Hand-authored pilot and provenance review |
| PDF tables | pdfplumber and a renderer for extraction/visual checking; separate OCR for scans | Audit a supplied extraction ledger |

Python 3.10+ runs repository checks using only the standard library. Upstream dependency requirements vary by pinned tool version and are intentionally not installed or claimed by these checks.
