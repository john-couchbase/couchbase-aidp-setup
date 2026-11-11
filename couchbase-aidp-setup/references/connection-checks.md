# Connection checks

## Direct inference first

Retrieve the Model Endpoint from the chosen deployment. Use its actual model identifier, not a friendly display name or an internal AI Function gateway URL. The inference route is `/v1/chat/completions`; normalize a base already ending in `/v1` to avoid duplicating it. Send the Model Service token as a Bearer credential. Management tokens do not substitute. [Official API usage](https://docs.couchbase.com/ai/api-guide/api-use.html).

The bundled probe performs one small text-completion test and reports HTTP status, success/nonempty output and selected safe metadata. It does not validate tool calling, embeddings, structured output, caching or SQL. It rejects non-HTTPS URLs, embedded credentials, query strings and redirects so it cannot accidentally forward a token to a redirected host. Verify the exact endpoint independently before use. HTTP 200 with an error body or empty choices is not success. Provider text is intentionally not printed.

| Observation | Next check |
|---|---|
| 401 / unauthorized | Token type, raw value, expiry, intended provider and integration |
| 403 | Roles, model scope, IP admission; HTML gateway rejection differs from JSON service error |
| 404 | Verified endpoint, path and model availability |
| 429 | Which limit: app allowance, provider rate, quota or concurrent operations |
| 500/503 | Service error and request ID; compare minimal direct call with application call |
| Timeout/TLS/DNS | Routing, allowlist, service readiness, SDK trust setup; keep TLS verification on |

The bundled probe is single-shot. Choose any subsequent retry explicitly, with bounded backoff for a retryable response and within the approved budget. Do not retry authentication failures indefinitely. [API error reference](https://docs.couchbase.com/ai/api-guide/api-errors.html).

## Database

Confirm the cluster is on, endpoint uses TLS, correct cluster credentials are configured, and the caller is admitted. Check service connectivity rather than assuming every timeout is a password problem. Read a known permitted record or perform a minimal query; verify required services and indexes for the actual workload. Parameterize SQL++ and confine lookups to the active visitor/run.

A Basic credential cannot be converted into Advanced; create a narrowly scoped replacement when needed and migrate only its intended callers. Separate SQL-function execution from unrelated data access where practical. Inspect the exact missing privilege and current RBAC documentation instead of granting broad administration. [Cluster access](https://docs.couchbase.com/cloud/clusters/cluster-rbac.html).

## SQL AI Functions

Current documentation lists paid 8.0+ clusters, Query Service, Developer Pro/Enterprise and multiple AZs. If a tenant UI permits a different configuration, record the discrepancy and confirm support before resizing or declaring compatibility. The binding uses the selected model's key ID and token. Advanced credentials require Query Curl Access. [AI Functions](https://docs.couchbase.com/ai/build/ai-functions.html).

Suggested diagnostic order from the demos:

1. Confirm the current app actually implements SQL inference. Setting a legacy environment flag cannot activate code that only makes direct HTTP calls.
2. Test the target model directly with the same intended credential and model. A missing valid region key leaves this comparison untested.
3. Inspect the enabled function and selected binding without printing stored definitions or internal credentials.
4. Run one constant-input completion using the deployed function's actual signature. A prior test used:

```sql
SELECT RAW default:ai_completion({
  "system_prompt": "Reply only OK",
  "user_prompt": "Connection test",
  "max_tokens": 100
});
```

5. Capture the query request ID and parse nested results. A returned `InternalServerError` object is failure even if the SQL request itself succeeded.
6. For an explicit `query_execute_global_functions` missing-role error, check Global Function Execute. Earlier environments used different external/CURL role terminology; verify current privileges. If the next error changes to an internal service error, the permission fix solved only that first failure.
7. If direct inference passes but SQL fails, narrow the issue to binding, SQL-origin networking or the function service. Do not conclude gateway failure without evidence. Only wire the app to SQL after a successful query and end-to-end application test.

Record SQL and direct paths separately for latency, usage and caching. Do not infer cache hits from speed. A larger output limit helped a historical empty-result case but is not a universal fix for authentication or internal errors.
