---
name: postgres-tenant-isolation
description: Design pgTAP regression tests for Postgres or Supabase tenant isolation and RLS role-operation matrices. Use for cross-tenant reads/writes, ownership reassignment, or policy regressions; not general SQL tuning or proof based on an admin connection.
---

# Tenant isolation with pgTAP

pgTAP provides SQL assertions, not a tenant authorization model. This workflow adds an explicit access matrix and positive/negative controls. Read [source evidence](references/source.md) and inspect the actual policies before generating SQL.

## Inputs and readiness

Request only the relevant schema, policies, grants, membership rule, trusted claim mechanism, and disposable database target. Identify owner/superuser/BYPASSRLS roles, functions/views, and the effective role used by tests. Runtime needs PostgreSQL, pgTAP, a TAP runner, and the intended auth environment. Supabase-specific claims cannot be inferred from plain Postgres. If these are missing, deliver the matrix and SQL design with an explicit not-run status.

## Workflow

1. Build a role × operation × tenant relationship matrix. Include anon, member A, member B, and nonmember; distinguish the `authenticated` database role from a tenant identity. Define allowed rows and allowed effects before writing assertions.
2. Seed two synthetic tenants and at least one visible own row. Verify an allowed read returns the expected row, so a broken auth setup cannot make all deny tests pass vacuously.
3. Run policy assertions under the real restricted role and test claims, using the project's reviewed test helpers where available. An owner, service role, or BYPASSRLS connection is an administration control, not evidence of client isolation.
4. Check SELECT, INSERT, UPDATE, and DELETE separately. RLS-denied reads/updates/deletes may return zero rows instead of errors. Assert result sets, RETURNING values, and post-state; use SQLSTATE assertions only where an error is expected by the actual grants/policy.
5. Test forged tenant IDs on insert and reassignment on update, as well as own-tenant success. Review both visibility (`USING`) and permitted new rows (`WITH CHECK`, including PostgreSQL's fallback semantics); also account for SELECT requirements, views, and SECURITY DEFINER boundaries.
6. In the authorized disposable target, run the TAP suite inside isolated transactions/fixtures, restore state, and capture assertion count, failures, effective role, and extension/server versions. Rollback does not neutralize every external side effect; exclude triggers that call live services.

## Boundaries and output

Do not modify live policies, grant roles, disable RLS, create extensions, use real JWTs/service keys, or connect to production as a side effect of test design. SQL context simulation does not prove end-to-end HTTP/JWT behavior.

Deliver the matrix, test SQL or integration plan, positive controls, and actual run status. [Example](references/example.md) and [synthetic case](assets/case.json) show the expected evidence. Current Supabase behavior must be checked against its official docs before execution.
