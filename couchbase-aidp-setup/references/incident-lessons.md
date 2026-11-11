# Incident lessons and support handoff

This ledger distinguishes firsthand test observations, reports supplied by the user, and hypotheses. It is historical guidance, not a current outage bulletin. Last consolidated November 11, 2026.

| Signature | Evidence from our work | Reusable response |
|---|---|---|
| Model shows Running/Healthy but prompts return 503 | User relayed Couchbase support's finding: an old gateway build (`1.0.0-155`) did not support serverless | Verify current gateway/service status and run a direct prompt after an upgrade. Do not attribute every 503 to that version. |
| API key creation blocked by gateway datastore | User relayed a deleted gateway datastore and a suggestion to deploy in another region, or remove all regional models/functions to recreate it | This was a support-directed workaround, not permission or a safe universal recipe. Regional teardown can affect others. |
| Managed memory deployment remains deploying | Independent saved provider key failed chat and embedding tests with 401; later user relayed `Embedding model health check failed: unauthorized` | Validate the actual embedding integration. The local and masked stored keys were not proven identical. |
| Destroy stalls after deploy | User relayed support's explanation that destroy waited for deployment attempts; fail-fast fix was planned | Check release/tenant status and jobs. Do not treat promised delivery as completed, or create more resources while old jobs remain. |
| SQL missing global function privilege | Observed explicit `query_execute_global_functions` failure; narrow advanced-role credential removed that error | Diagnose least privilege against actual function; Basic-to-Advanced requires a new credential. |
| SQL then returns nested InternalServerError | Constant-input completion failed after permission repair; internal credential retrieval succeeded in one diagnostic | Upstream/binding issue remained unresolved. A fresh Virginia direct test was not completed; gateway cause was not confirmed. Internal token retrieval alone does not validate the model credential. |
| Capella signs out during model key creation | Repeated UI sign-out while creating a Virginia Model Service key; no generated test key confirmed | Browser-session/key-creation issue, not proof of model authorization failure. One controlled retry, inspect partial creation, then report. |
| Older AI Function returned empty text | Original Air migration notes reported improvement when max_tokens rose from low values to 500 | Historical model/function-specific behavior. Do not claim 500 universally fixes it or costs nothing. Reproduce with bounded tokens and parse actual results. |
| Cache story differs across paths | Original notes changed their diagnosis; current direct adapter trusts returned cache verdicts | Measure each path. Latency or repeated prompt alone does not prove a cache hit, SQL caching or semantic caching. |
| Old docs say live memory/SQL; current app does not | Legacy Air architecture and current `air_live` runtime coexist | Inspect entry point and active code. Do not apply legacy env flags, provisioning or reset scripts to new run-scoped storage. |
| Hosted smoke test hits daily allowance | Local/code checks can pass while real inference remains unverified | Report allowance exhaustion; do not change budget automatically or call the integration fully tested. |

## Gather once, report clearly

Privately collect: organization/tenant, project, cluster/server/model IDs, region, deployed version, UTC timestamp, operation, sanitized request/response, HTTP status, request ID, duration, last successful operation and exact change since then. Separate browser sign-out screenshots from API errors. Avoid tokens, private customer data, full config files and unredacted HAR exports. Share identifiers only with the intended support recipient.

Use one minimal reproduction and one independent comparison when justified. After the same failure recurs without a changed dependency or new evidence, stop retrying and report the boundary still failing. Do not send a support message unless the user authorizes sending it.

Short first-person draft:

> Hey, I’m trying to [operation] in [Capella section and region]. When I [action], I get [exact sanitized error or sign-out]. I checked [one meaningful comparison]. Could you look at [request/deployment ID, shared privately] from [UTC time]?

For the recent key issue: “I’m in AI Data Plane → Access Control → Models, creating a Virginia key for Nova Micro to test SQL inference. It keeps signing me out before I can finish.” Do not say the key was generated or tested if it was not.
