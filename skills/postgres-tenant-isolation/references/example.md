# Example: two tenants, one shared database role

Input contract: members may read/write their own tenant's notes, anon has no access, and updates may not transfer a note to another tenant. Fixture IDs are symbolic; map them to disposable UUIDs only in a reviewed integration setup.

| Effective role / identity | Operation | Target | Expected |
| --- | --- | --- | --- |
| authenticated / member A | SELECT | tenant A | Own row returned |
| authenticated / member A | SELECT | tenant B | Empty set |
| authenticated / member B | SELECT | tenant A | Empty set |
| anon / none | SELECT | protected notes | Empty set or grant error, as specified |
| authenticated / member A | INSERT | tenant B | Error; no inserted row |
| authenticated / member A | UPDATE | A row to B tenant | Error; original row unchanged |
| authenticated / member A | DELETE | tenant B | Zero effects; B row still present |

Original SQL assertion sketch; **not runnable until the target, schema, fixture, test role/claims, and pgTAP search path are supplied**:

```sql
-- Already inside an isolated test transaction and restricted test identity.
select results_eq(
  $$select id from test_notes where tenant_id = 'tenant-a' order by id$$,
  $$values ('note-a'::text)$$,
  'own tenant has a visible positive control'
);
select is(
  (select count(*)::integer from test_notes where tenant_id = 'tenant-b'),
  0,
  'other tenant is invisible'
);
```

Check write post-state after restoring the appropriate observing role. Do not infer a write was rejected just because the caller saw no returned row. The bundled JSON audits a proposed matrix; it does not execute SQL or verify RLS.

Official context: [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [Supabase changelog](https://supabase.com/changelog), [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html). Grants, RLS, and Data API exposure are distinct checks. Verify all three in the target project.
