# Managed Agent Memory

## Deployment and prerequisites

Current managed-memory documentation requires a healthy AWS Capella 8+ cluster with Data, Index, Query and Search, an eligible region (currently Virginia or London), a dedicated bucket and an OpenAI integration for the embedding model and LLM. It permits one memory server per cluster. Configuration choices such as cluster, models and node count are not editable after deployment; verify these constraints and the price before creating resources. [Deployment guide](https://docs.couchbase.com/agent-mem/current/managed/deploy-agent-mem-managed.html).

Choose the actual approved integration for each dependency. A working Capella-hosted chat model does not prove that the OpenAI embedding key is valid. A provider key passing chat may still lack the configured embedding model or quota. Validate both configured dependencies with tiny authorized requests before a costly deployment attempt.

## Access once deployed

Create a server-specific Agent Memory key after deployment finishes. Choose Read for retrieval only; Write includes storing and changing memory; Admin is for administrative work, not the normal demo runtime. Save its token at creation. [Key setup](https://docs.couchbase.com/agent-mem/current/api-guide/managed/api-start.html), [access levels](https://docs.couchbase.com/agent-mem/current/api-guide/managed/api-intro.html).

Copy the server's Connect endpoint and admit the approved caller IP on that memory server. These are separate from the model endpoint and cluster allowlist. The Python package is `couchbase-agent-memory`; confirm the installed version's methods before copying code. [Managed quickstart](https://docs.couchbase.com/agent-mem/current/get-started/get-started-agent-mem-managed.html).

## Verify the feature, not just provisioning

The demo's evidence ladder is:

1. Service readiness and authenticated health.
2. A disposable user/session dedicated to the test.
3. Write a harmless distinctive fact using the service API.
4. Read the stored record back and check its fact/summary and identity.
5. Recall it by a meaningfully related query; validate relevance, not just nonempty results.
6. Repeat through the hosted app and verify another visitor cannot retrieve it.

For asynchronous extraction, observe completion within a bounded test window before calling recall a failure. Preserve identity, TTL and intended retention semantics. Clean up only the expressly disposable test records when authorized. The API/SDK surface is versioned; use the [REST reference](https://docs.couchbase.com/agent-mem/current/agent-memory-api-reference/rest-api.html) for current operations.

## If deployment is stuck

Inspect dependency errors, project events and service logs available to the account. `Embedding model health check failed: unauthorized` points to the embedding provider authorization path. Test that provider integration, not a new Capella model token. An independent local key failing does not establish what is stored in a masked integration.

Capture status and timestamp changes at a modest interval, stop after a bounded unchanged observation window, and escalate with IDs. Do not invent a universal provisioning duration. Deletion can also stall; preserve the bucket/configuration and inspect before attempting recreation. Never stack replacement servers while the original still exists. A promised fail-fast release is not evidence that it reached this tenant.

A gateway HTML 403 before admission does not diagnose backend model health. A health-only response, saved booking, database session document or local conversation history does not prove managed-memory extraction or recall works. If unavailable, label memory disabled/unverified while continuing independently working model/catalog/tracing features. Do not quietly label ordinary database persistence as Agent Memory.

Provider `invalid_api_key` is an authentication failure, while quota/rate errors need a different remedy. Repeated retries or adding `API_KEY=` to a raw token will not repair an invalid credential. [Official OpenAI errors](https://developers.openai.com/api/docs/guides/error-codes).
