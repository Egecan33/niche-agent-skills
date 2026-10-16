# Validation record

Checked 2026-10-16 with Python 3.11.5. Only newly authored local validation/test code was executed; remote repository code was inspected as text.

| Check | Observed result | Meaning |
| --- | --- | --- |
| Static package validator | Passed for seven skills | Narrow metadata profile, links, source pins, layout and partial privacy scan |
| Offline synthetic cases | 33/33 expected issue sets matched | Teaching-case invariants, including deliberate failure controls |
| Unit and mutation tests | 38 tests passed | Validator/fixture rejection behavior, evaluation-data separation, locator provenance and read-only inventory CLI |
| License notices | Seven reviewed and retained | Six full notices match pinned Git blobs after terminal-newline normalization; pgTAP is the reviewed license section of its pinned README |
| Trigger dataset | 28 prompts prepared | Not executed as host routing evaluations |
| Behavior evaluation | Seven tasks prepared | No model/host evaluation executed |
| Held-out input separation | Seven distinct input-only artifacts, SHA-256 bound to evaluator-only outcomes | Static isolation/data-integrity checks only; no model run |
| Upstream integrations | Not run | No SQL, HTTP fuzzing, trace instrumentation, replay, Curator inference or PDF extraction/rendering |
| Claude Code / Codex host smoke tests | Not run | Local discovery, explicit invocation and model behavior remain unverified |

Reproduce local results from the repository root:

```sh
python3 scripts/validate_package.py
python3 scripts/check_fixture.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_package.py --inventory
```

The scanner checks sensitive file names, private home paths, common GitHub/AWS credentials, private-key markers and email addresses. It is intentionally partial. The publishable set was also reviewed for unintended personal files, real customer/session content, application/resume details, absolute local paths and credentials. The synthetic examples and source/license notices are the intended contents; no historical general-purpose draft is included.

The inventory CLI regression was reproduced on a macOS temporary path alias and corrected by using the same lexical root for inventory paths as file traversal. The existing test failed before the correction and passed afterward. This was a local tooling defect, not a claim about any upstream tool.

Post-publication review found that behavior tasks pointed at answer-bearing teaching cases and that dataset evidence accepted any nonempty locator. Both defects were reproduced with failing tests before correction. Teaching verdicts/answer oracles now live evaluator-side, behavior inputs use separate held-out records, and source locator-to-text inventories reject missing or empty source sections. Mutation tests also reject answer keys in model inputs/installed assets and detect input-oracle drift. These changes concern local evaluation quality; they do not establish upstream integration or host behavior.

GitHub CI was not run or claimed; the test results above are from local execution.

No measured trigger accuracy, model-quality improvement, end-to-end tenant security, native replay fidelity or PDF visual correctness is claimed. See [evaluation design](EVALUATION.md) for the next evidence layers.
