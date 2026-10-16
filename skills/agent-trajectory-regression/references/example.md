# Example: lookup before preparing a change

Input: the tool path must be `lookup_record(record_id=7)` then `prepare_change(record_id=7, amount=12)`. The amount and record ID are significant. Transport request IDs may vary, but duplicate calls are significant. This is a synthetic workflow; no real record is modified.

Expected analysis:

| Candidate | Verdict | Evidence |
| --- | --- | --- |
| Same calls and arguments | Pass | Two calls at positions 0 and 1 |
| prepare_change then lookup_record | Fail | Required prerequisite is reversed |
| Correct order, amount=120 | Fail | Significant argument differs |
| prepare_change called twice | Fail | Unexpected repeated side-effect intent |

Illustrative output:

```json
{"case_id":"changed-amount","status":"fail","path":"calls[1].arguments.amount","expected":12,"observed":120,"execution":"manual contract analysis"}
```

AgentEvals integration sketch, not executed here: import `create_trajectory_match_evaluator` from `agentevals.trajectory.match`, select `trajectory_match_mode="strict"` and `tool_args_match_mode="exact"`, then supply normalized messages as `outputs` and `reference_outputs`. Consult the pinned source before constructing complete message objects. The local fixture compares simplified call records; it is not a substitute for testing AgentEvals message normalization or its matching semantics.
