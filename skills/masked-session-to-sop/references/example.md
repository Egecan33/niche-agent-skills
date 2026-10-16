# Example: save a draft

Input: consent permits workflow documentation in a synthetic sandbox. Events: e1 open Drafts at t=0; e2 type `[masked]` at t=1; e3 click Save at t=2; e4 visible “Draft saved” at t=3. A second session ends at e3.

Expected SOP output:

1. Open Drafts (e1).
2. Enter the user-supplied draft text; recorded content is unknown (e2).
3. Select Save (e3) and wait for the observed confirmation (e4).

For the second session, report “save requested; result unknown.” Do not merge evidence from another session to certify its outcome.

Automation requirement: locate the Save control through a stable accessible name or reviewed test ID, wait for the confirmation with a bounded timeout, and stop on timeout to avoid a duplicate write. Whether resubmission is safe depends on the application's idempotence contract. No locator is proven merely by this event summary.

Native preparation must verify masking/blocking against the pinned rrweb API. `maskAllInputs` protects input content, `maskTextClass`/`maskTextSelector` cover selected text, and `blockClass`/`blockSelector` omit selected subtrees. This is a design inventory, not a complete privacy guarantee. The fixture contains only normalized synthetic events; the privacy/consent flags are test assertions, not independently verified consent records.
