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


## SQL integration follow-up — November 11, 2026

Status: reproducible integration failure; root cause and vendor bug status unconfirmed. This follow-up does not erase the earlier, different SQL incident above.

- After the reported Virginia redeployment, Model Service key creation succeeded without sign-out. The downloaded key returned HTTP 200 with a completion from Nova Micro and HTTP 200 with a 1,024-dimension embedding from Titan v2.
- A newly associated completion function on a separate eligible cluster showed Healthy. Its first configuration used a database-style username as the model API Key ID. After user correction, the saved ID matched the downloaded Model Service ID.
- The edit form returned a short token-like value rather than the downloaded secret. It may be a placeholder; this does not establish incorrect import or prove the stored token matches. Do not print either value or repeatedly overwrite credentials based on this alone.
- Ordinary SQL succeeded; constant-input AI completion repeatedly returned 5010, Error evaluating ExpressionScan. Inspecting installed metadata confirmed the generated function exists and calls a local credential service before its model endpoint.
- An isolated read-only diagnostic of that same local credential lookup also failed (5010, ExpressionScan/projection). This narrows the failure boundary, but does not identify whether service availability, policy binding, permissions, credential storage, or another internal condition caused it.
- With explicit approval, the model key briefly allowed all IPv4 sources for one test. The same failure persisted; the original restriction was restored and verified. This is evidence against the allowlist being the only issue, not proof of propagation timing or of every network hop working. No standing approval for broad access carries forward.

### What to do next for this signature

1. Confirm current deployment, key region, function signature and active application database. Direct inference passing does not activate SQL inference in an app or move data between clusters.
2. Compare key identity privately and test the downloaded key directly against an independently verified public model endpoint. Never use an internal SQL gateway port as the public endpoint.
3. Inspect generated function metadata without publishing definitions, policy IDs or tokens. If isolating a credential lookup is authorized, return only safe status/field names; never return the credential itself.
4. Report the isolated failure and ask support to inspect Query-node credential-service logs, policy association and stored-credential handling. Do not call a generic 5010 a confirmed provider authentication error or confirmed product bug. Check explicit permissions rather than assuming ordinary SQL proves function/CURL privileges.
5. After a fix: rerun direct inference and SQL completion, verify nonempty successful output (not just HTTP/SQL success), test the actual app runtime with its scoped credentials, then verify visitor isolation and usage tracking. Reapply only the approved network rules. Record the confirmed cause and fix here when supplied and verified.


### Workaround verification — November 11, 2026

The user relayed that support applied a workaround and intended to file a bug ticket. Subsequent browser SQL tests on the affected cluster returned a nonempty `OK` answer and correctly returned `CANCELLATION` for a passenger request. The workaround is verified for these two SQL tests; its mechanism and a permanent production code fix remain unconfirmed.

Do not keep treating this incident as an active universal SQL outage. Also do not equate successful browser queries with hosted app integration: separate cluster credentials, network access, response parsing, fallback accounting and per-visitor isolation must still be tested. Hosted integration was initially deferred, then authorized; track its separate deployment evidence rather than inferring success from the local test. SQL responses observed here contain nested response text without token usage. Mark usage unknown rather than claiming zero cost, and account for both model attempts if SQL falls back to direct inference.

### Local runtime verification — November 11, 2026

The scoped SDK credential successfully ran the application’s SQL adapter. A full local storm completed four SQL classifications with no fallback, three direct recovery calls and one lower-priority skip. Results, tools and incomplete usage labels appeared in the UI. Injected connection/invalid-response tests exercised fallback and error redaction. This verifies the workaround in the local application; it does not identify the vendor fix mechanism.

### Hosted runtime verification — November 12, 2026 UTC

The Air preview and public Vercel deployment each completed four SQL classifications with no fallback, three direct recovery calls and one lower-priority skip. Saved decisions and SQL tools were verified; a second visitor remained unchanged and cross-session decision reads were denied. Existing SQL-cluster network admission was sufficient and was not widened. The dedicated execution-only credential is stored as a sensitive server variable. SQL costs remain incomplete because the function response supplies no token usage. This establishes the workaround in the hosted application, not a confirmed permanent vendor fix.
