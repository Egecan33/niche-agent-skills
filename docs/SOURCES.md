# Sources and file-level license review

Reviewed on 2026-10-16 using read-only GitHub resources at the exact commits below. Remote source code was inspected as text and was not executed. The original workflows add task-specific interpretation and safety/evidence requirements; they are not claims that upstream tools natively produce those outputs.

| Source | Pinned commit | Reviewed license | Upstream capability | Workflow added here |
| --- | --- | --- | --- | --- |
| [langchain-ai/agentevals](https://github.com/langchain-ai/agentevals) | [946ad15b9f2c](https://github.com/langchain-ai/agentevals/commit/946ad15b9f2ce9bc9843edd2bb773bd07d78ca7e) | [MIT](https://github.com/langchain-ai/agentevals/blob/946ad15b9f2ce9bc9843edd2bb773bd07d78ca7e/LICENSE) | Rule-based trajectory matching and tool-argument matching; optional LLM judges are a separate mode. | Versioned order/argument regression contracts, semantic-argument safeguards, and negative controls. |
| [theory/pgtap](https://github.com/theory/pgtap) | [21ceed193bf3](https://github.com/theory/pgtap/commit/21ceed193bf370892d530c5115680839ee322851) | [PostgreSQL](https://github.com/theory/pgtap/blob/21ceed193bf370892d530c5115680839ee322851/README.md) | PostgreSQL TAP-emitting assertions, including query-result and error assertions. | Tenant/role/operation RLS matrices with positive controls, adversarial writes, and bypass-role checks. |
| [schemathesis/schemathesis](https://github.com/schemathesis/schemathesis) | [0a5ea2fef518](https://github.com/schemathesis/schemathesis/commit/0a5ea2fef5189617214c04a2a474659d6399f963) | [MIT](https://github.com/schemathesis/schemathesis/blob/0a5ea2fef5189617214c04a2a474659d6399f963/LICENSE) | Schema-driven API test generation, response validation, failure reports and reproductions. | Bounded disposable-target probes, failure triage and minimized regression artifacts. |
| [Arize-ai/openinference](https://github.com/Arize-ai/openinference) | [2925fc3eb2ae](https://github.com/Arize-ai/openinference/commit/2925fc3eb2aea3fe4cd32395279243b129b23082) | [Apache-2.0](https://github.com/Arize-ai/openinference/blob/2925fc3eb2aea3fe4cd32395279243b129b23082/LICENSE) | OpenTelemetry-compatible semantic conventions and instrumentation/masking support. | Evidence-based latency/error investigation, overlap-aware timing and instrumentation-gap reporting. |
| [rrweb-io/rrweb](https://github.com/rrweb-io/rrweb) | [9b9a1ff30dd2](https://github.com/rrweb-io/rrweb/commit/9b9a1ff30dd281d00317b0fbece3dbd90a9e0a80) | [MIT](https://github.com/rrweb-io/rrweb/blob/9b9a1ff30dd281d00317b0fbece3dbd90a9e0a80/LICENSE) | DOM snapshots, interaction recording/replay and configurable masking/blocking. | Consent-gated interpretation of a sanitized session into a cited SOP and automation requirements. |
| [bespokelabsai/curator](https://github.com/bespokelabsai/curator) | [98bb706d2261](https://github.com/bespokelabsai/curator/commit/98bb706d226107265175170906400e20775ef28c) | [Apache-2.0](https://github.com/bespokelabsai/curator/blob/98bb706d226107265175170906400e20775ef28c/LICENSE) | Bulk inference/data-curation pipelines with prompt/parse interfaces and structured output support. | Source-grounded test generation with provenance, abstention cases, semantic review and split isolation. |
| [jsvine/pdfplumber](https://github.com/jsvine/pdfplumber) | [4c64b92d5cac](https://github.com/jsvine/pdfplumber/commit/4c64b92d5caccd71c645e98e0fabb0c4dba7ff45) | [MIT](https://github.com/jsvine/pdfplumber/blob/4c64b92d5caccd71c645e98e0fabb0c4dba7ff45/LICENSE.txt) | Character/line/rectangle inspection, table objects and visual debugging; no OCR engine. | Page-and-coordinate evidence ledger for extracted cells with visual checks and reconciliation. |

## Exact files and scope

The complete machine-readable review is in [sources.lock.json](../sources.lock.json). Each entry records Git blob identity, pinned URL, nearest reviewed license scope and reuse status. Root and closer license files were checked for the listed paths; no file-header override was observed in those consulted files. This is a review of these paths at these commits, not a blanket license approval for future additions.

### langchain-ai/agentevals

- [LICENSE](https://github.com/langchain-ai/agentevals/blob/946ad15b9f2ce9bc9843edd2bb773bd07d78ca7e/LICENSE) — root LICENSE; license notice only reproduced.
- [README.md](https://github.com/langchain-ai/agentevals/blob/946ad15b9f2ce9bc9843edd2bb773bd07d78ca7e/README.md) — root LICENSE; consulted, not copied.
- [python/agentevals/trajectory/match.py](https://github.com/langchain-ai/agentevals/blob/946ad15b9f2ce9bc9843edd2bb773bd07d78ca7e/python/agentevals/trajectory/match.py) — python/LICENSE; consulted, not copied.
- [python/LICENSE](https://github.com/langchain-ai/agentevals/blob/946ad15b9f2ce9bc9843edd2bb773bd07d78ca7e/python/LICENSE) — python/LICENSE; consulted, not copied.

### theory/pgtap

- [README.md](https://github.com/theory/pgtap/blob/21ceed193bf370892d530c5115680839ee322851/README.md) — README Copyright and License section; corroborated by META.json; license notice only reproduced.
- [META.json](https://github.com/theory/pgtap/blob/21ceed193bf370892d530c5115680839ee322851/META.json) — README Copyright and License section; corroborated by META.json; consulted, not copied.
- [doc/pgtap.md](https://github.com/theory/pgtap/blob/21ceed193bf370892d530c5115680839ee322851/doc/pgtap.md) — In-file Copyright and License section; corroborated by META.json; consulted, not copied.
- [sql/pgtap.sql.in](https://github.com/theory/pgtap/blob/21ceed193bf370892d530c5115680839ee322851/sql/pgtap.sql.in) — README Copyright and License section; corroborated by META.json; consulted, not copied.

### schemathesis/schemathesis

- [LICENSE](https://github.com/schemathesis/schemathesis/blob/0a5ea2fef5189617214c04a2a474659d6399f963/LICENSE) — root LICENSE; license notice only reproduced.
- [README.md](https://github.com/schemathesis/schemathesis/blob/0a5ea2fef5189617214c04a2a474659d6399f963/README.md) — root LICENSE; consulted, not copied.
- [docs/quick-start.md](https://github.com/schemathesis/schemathesis/blob/0a5ea2fef5189617214c04a2a474659d6399f963/docs/quick-start.md) — root LICENSE; consulted, not copied.

### Arize-ai/openinference

- [LICENSE](https://github.com/Arize-ai/openinference/blob/2925fc3eb2aea3fe4cd32395279243b129b23082/LICENSE) — root LICENSE; license notice only reproduced.
- [README.md](https://github.com/Arize-ai/openinference/blob/2925fc3eb2aea3fe4cd32395279243b129b23082/README.md) — root LICENSE; consulted, not copied.
- [spec/semantic_conventions.md](https://github.com/Arize-ai/openinference/blob/2925fc3eb2aea3fe4cd32395279243b129b23082/spec/semantic_conventions.md) — root LICENSE; consulted, not copied.
- [js/packages/openinference-core/docs/trace-config-and-masking.md](https://github.com/Arize-ai/openinference/blob/2925fc3eb2aea3fe4cd32395279243b129b23082/js/packages/openinference-core/docs/trace-config-and-masking.md) — root LICENSE; consulted, not copied.

### rrweb-io/rrweb

- [LICENSE](https://github.com/rrweb-io/rrweb/blob/9b9a1ff30dd281d00317b0fbece3dbd90a9e0a80/LICENSE) — root LICENSE; license notice only reproduced.
- [README.md](https://github.com/rrweb-io/rrweb/blob/9b9a1ff30dd281d00317b0fbece3dbd90a9e0a80/README.md) — root LICENSE; consulted, not copied.
- [guide.md](https://github.com/rrweb-io/rrweb/blob/9b9a1ff30dd281d00317b0fbece3dbd90a9e0a80/guide.md) — root LICENSE; consulted, not copied.
- [docs/recipes/record-and-replay.md](https://github.com/rrweb-io/rrweb/blob/9b9a1ff30dd281d00317b0fbece3dbd90a9e0a80/docs/recipes/record-and-replay.md) — root LICENSE; consulted, not copied.

### bespokelabsai/curator

- [LICENSE](https://github.com/bespokelabsai/curator/blob/98bb706d226107265175170906400e20775ef28c/LICENSE) — root LICENSE; license notice only reproduced.
- [README.md](https://github.com/bespokelabsai/curator/blob/98bb706d226107265175170906400e20775ef28c/README.md) — root LICENSE; consulted, not copied.
- [src/bespokelabs/curator/llm/llm.py](https://github.com/bespokelabsai/curator/blob/98bb706d226107265175170906400e20775ef28c/src/bespokelabs/curator/llm/llm.py) — root LICENSE; consulted, not copied.

### jsvine/pdfplumber

- [LICENSE.txt](https://github.com/jsvine/pdfplumber/blob/4c64b92d5caccd71c645e98e0fabb0c4dba7ff45/LICENSE.txt) — root LICENSE.txt; license notice only reproduced.
- [README.md](https://github.com/jsvine/pdfplumber/blob/4c64b92d5caccd71c645e98e0fabb0c4dba7ff45/README.md) — root LICENSE.txt; consulted, not copied.

## What is copied

Only upstream license notices are reproduced in `docs/upstream-licenses/`, with their copyright/permission/disclaimer text retained. The pgTAP notice is extracted from the pinned README's explicit Copyright and License section because that repository has no standalone LICENSE file. `META.json` and the in-file documentation notice corroborate its PostgreSQL-style terms. Terminal newlines in notice snapshots may be normalized; no operative text is changed.

No upstream implementation, README tutorial, test fixture, dataset, image or skill instruction is copied or translated. The workflows, prose examples, fixtures, scripts and tests are original local authoring under the root MIT license. Upstream API names and factual capabilities are cited so readers can inspect the source. See [third-party notices](../THIRD_PARTY_NOTICES.md) and [per-file copy provenance](FILE-PROVENANCE.csv).

## Future addition template

Before copying/adapting: record repository and immutable commit; exact upstream file and destination; nearest license/header/exception; required notices; modifications; reviewer/date; decision and reason. Missing/unclear rights means do not copy. Repository badges, source availability, or permissive licensing of an adjacent file do not establish permission for another file.

## Interoperability references

- [Agent Skills specification](https://agentskills.io/specification): shared file structure and metadata constraints.
- [Claude Code skills](https://code.claude.com/docs/en/skills): local discovery/invocation paths.
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills): standalone skill authoring/local discovery.
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins): distribution is a separate layer.
- [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security) and [changelog](https://supabase.com/changelog): live platform context checked on the review date; no SQL or project settings were changed.
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html): restricted role/bypass and policy semantics.

These live documentation pages are linked and summarized independently, not vendored. Installed skill-authoring, documentation, testing, Supabase and PDF guidance informed the process and is not redistributed.
