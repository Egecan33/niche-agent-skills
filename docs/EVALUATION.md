# Validation and evaluation design

Keep three evidence layers separate. The source tree alone cannot establish host compatibility or model quality.

## 1. Offline package and fixture checks

`validate_package.py` checks this package's narrow two-field frontmatter profile, names, inline relative links, JSON structure, source/license pins, file hygiene, and evaluation coverage. It is not a general YAML/Markdown parser, an official validator or a complete secret scanner. It never fetches remote links or runs upstream code.

`check_fixture.py` checks 33 original normalized teaching scenarios across seven workflows, including negative controls. Installed `skills/*/assets/case.json` files contain task data; case verdicts and hand-authored answer oracles live separately in `evals/oracles/teaching.json`, which the local checker loads evaluator-side. The grounded-dataset source includes a locator-to-text inventory: a nonempty but nonexistent or empty-text locator fails provenance validation. Locator existence does not establish answer entailment.

These are teaching-case invariants: simplified call comparison, reported row-set auditing, one integer-property API contract, span interval unions, session evidence references, hand-authored answer oracles, and mock PDF cell ledgers. They are not substitutes for upstream libraries or general domain validators. JSON does not execute RLS, render PDFs, replay rrweb, or prove semantic entailment. Worked prose examples intentionally explain outcomes and are not blind evaluation tasks.

The unit suite mutates inputs to test meaningful rejection behavior and checks CLI exit status. Run all three README commands. Preserve outputs and the reviewed file inventory for a release; the validation record reports what actually ran.

## 2. Upstream integration smoke tests — not run

Use isolated, reviewed environments and synthetic data only:

- AgentEvals: convert fixtures to real supported messages, run exact/strict matching, and verify changed argument/order controls fail.
- pgTAP: create reviewed disposable tenant/auth fixtures, run an own-row positive control and the CRUD matrix under restricted roles, verify TAP output, and restore state.
- Schemathesis: use a disposable loopback API with a deliberate contract bug, bounded operations/budget and no external schema refs; reproduce the failure.
- OpenInference: instrument a synthetic nested/overlapping/error trace and compare exported kind/status/timing with the analysis.
- rrweb: record only a consented synthetic page after masking verification; verify native replay and event evidence without external networking.
- Curator: use an explicitly selected local/mock backend where supported, or authorize a provider/budget separately; verify row/source linkage and rejection reports without CodeExecutor.
- pdfplumber: generate or obtain a permitted synthetic machine-readable PDF, extract real table objects and review rendered overlays against cell geometry.

Record exact dependency versions and commands. Missing dependencies are a not-run result, not a pass.

## 3. Real host/behavior evaluations — not run

`evals/cases.json` is an **evaluator manifest**, schema version 2: 28 routing prompts and seven behavior tasks. A behavior entry points to an input-only file in `evals/inputs/` and evaluator-only assertions/outcomes in `evals/oracles/behavior.json`. Each oracle is bound to the input's SHA-256 so a changed input requires deliberate re-review. Model inputs contain no grading labels, oracle answers, or evaluator assertions.

The seven `held-out-v1` inputs use different records, quantities, source IDs/text, spans, sessions and coordinates from installed teaching examples. For example, the trace task has a different timeline and the dataset task uses a different source window and a missing locator. These are separate from the teaching checks; the offline checker does not grade model outputs on these tasks. The fixtures are public and cannot establish that the model has never encountered their content elsewhere.

A negative routing prompt is a near-miss relative to that particular skill; another skill may be appropriate. Harmful or unconsented activity should be declined by host policy independently of routing.

For each host/version and model, install only the reviewed skill in a disposable project, confirm its loaded path, and run fresh sessions:

1. For routing, give the unmodified prompt without naming the skill. Record observed skill loading, ambiguity, false positives and false negatives.
2. For behavior, prepare a disposable workspace containing only the selected complete skill directory and a copy of its held-out input named `input.json`. Give the model only the manifest's `prompt` text plus that input, with explicit skill invocation. Do not give it the manifest, either oracle file, checker/tests, evaluation documentation, or access to the source repository/parent directories. Enforce that boundary in the evaluation environment and disable fetching public answers; hiding a path in a prompt alone is insufficient. If isolation cannot be enforced, record the run as potentially contaminated rather than blind.
3. Use at least three repetitions per condition when estimating reliability. Keep task/data fixed and record environment, timing and missing capabilities.
4. After execution, a separate evaluator reads the frozen output/transcript and the corresponding entry in `evals/oracles/behavior.json`. Grade observable assertions and boundary violations, not echoed wording. Run the same input without the skill as a baseline under the same isolation. Report denominators, each failure and limitations; do not average a privacy/scope breach away.
5. Review outputs with a human before changing descriptions or expected answers. Keep a held-out prompt/source set for later revisions.

Use `evals/run-result.template.json` as an empty record. Save real runs in an ignored `eval-runs/` directory and sanitize before sharing. Do not commit prompts, traces or environment details containing private data. The initial release claims neither measured trigger accuracy nor model-quality improvement.
