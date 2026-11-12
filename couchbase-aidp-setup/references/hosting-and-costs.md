# Hosting, isolation and cost

These are implementation lessons from the demos, not a universal hosting prescription.

## Small hosted architecture

A static frontend plus a small server runtime can keep credentials out of the browser. Vercel functions supported the demos; that does not make every Couchbase SDK/runtime combination deployable unchanged. Verify runtime language, package compatibility, request duration, connection setup and outbound networking. A frontend deployment does not prove database or inference access.

Keep encrypted server variables separate from public build variables. Reuse clients when the runtime permits; do not depend on process memory for durable sessions, global budgets or locks. An always-available link must not depend on a sleeping laptop or local embedding endpoint. Inspect whether a configured local endpoint is actually used before claiming remote semantic search works.

Fixed egress/private networking may cost more. Dynamic hosted egress does not match the developer's laptop IP. Broader allowlisting is a deliberate security choice with scoped credentials and abuse controls, not an automatic setup step. Database, inference and memory network admission remain separate.

## Independent visitors

Use server-issued, authenticated visitor sessions and run-scoped records in a dedicated collection. Bind ownership on every read, write, reset, history and approval operation. A new collection alone does not establish isolation. Use parameterized queries and concurrency-safe state transitions; never trust a client-supplied run ID without checking ownership.

Test two independent sessions: start both, trigger a storm/change in one, reset it, reopen history and attempt the other run's identifier. The second visitor's state must remain unchanged and inaccessible. Test duplicate requests and stale workers so actions are not applied twice. Keep shared budget enforcement atomic while per-visitor limits remain separate.

## Cost worksheet

Report dates and units, not an old monthly figure as current billing:

`fixed estimate = active hours × active hourly quote + off hours × off quote`

Then add model usage, managed-memory compute/provider usage, hosting, storage/backup, networking and taxes where applicable. Distinguish estimated spend, current quote and actual billed spend. A demo room price is not a cloud bill. Historical figures from our chat are examples, not current quotes.

Check the tenant's actual configuration before downsizing. Preserve services required by catalog/search/tracing/memory, and verify eligibility for SQL Functions. A smaller node that removes a necessary service is not an equivalent saving. A serverless inference model does not make the operational database serverless or free.

Daily request/step reservations are not dollar caps. A step may invoke several calls, fail, retry or consume provider resources separately. Preserve the user's existing allowance; do not raise it just to make a smoke test pass. Record the reset timezone and actual counter units.

## Pause and resume

Inventory resources individually. Turning off a database preserves its configuration/data but disconnects clients and still incurs the quoted off/storage and possible network/backup costs. Linked services and maintenance have separate behavior. [Cluster scheduling](https://docs.couchbase.com/cloud/clusters/off-on-schedule.html).

Do not assume a failed deletion is free or that pausing one service stops another. Verify terminal state and current billing evidence; preserve data and exported non-secret configuration. Resuming requires checking the current budget, credentials, expiry, network access and dependencies, then a small end-to-end read/write/inference test. An assistant subscription upgrade does not pay Capella or provider charges.

## Deploying a verified SQL path

Keep SQL explicitly opt-in and retain a direct fallback plus a rollback switch. Store the SQL-host credential separately from the run-data credential in sensitive server variables. Test a protected preview with the actual server runtime, then repeat a bounded request and isolation test at the public production alias. A successful fallback is service continuity, not proof that SQL worked: assert the recorded inference path. Validate nonempty results, stored decisions, command labels and incomplete usage reporting. Publish source and sanitized evidence separately from private configuration; identify the exact deployed revision/branch.


## Measured usage versus estimates

Keep three categories separate: provider-reported token counts, approximate token estimates, and unavailable usage. Direct fallback usage must remain visible when the preceding SQL attempt has unknown usage. Count both attempts when supported by saved evidence, and do not infer cache misses from absent cache metadata.

If explicitly requested, a text-size heuristic can give a rough SQL estimate. Label it beside the number, document the method and dated rate source, and retain measured fields unchanged. A rate from an AWS reference example is not confirmation of the tenant’s Capella credit price. Aggregate model counters cannot be assigned to one visitor when other traffic shares that model.

Per-run saved results are not a complete billing ledger: failed calls without results, reset/expired records, storage, shared clusters, networking and hosting can be missing. Do not add an old database quote to model costs and call it the current total. Verify each resource and avoid counting a shared cluster’s whole bill as this demo’s incremental cost.
