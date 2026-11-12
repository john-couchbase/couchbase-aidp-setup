# SQL inference: setup through deployment

This is the complete route used for the Air demo, consolidated November 11, 2026. Historical success is evidence, not a guarantee that today's deployment is healthy. Read the linked guides for exact credential handling and incident evidence. No secret values belong in this guide.

## 1. Identify the two connections

The application connects to a database with a cluster username/password. The SQL AI Function connects to a model with a Model Service key ID/token. These are separate credentials and network hops.

Record privately: organization/project, function-host cluster and region, datastore cluster/collection, model ID/region/endpoint, credential names/expiry, authorized callers and budget. Do not assume the datastore also hosts the function.

Our example used HOLCluster for SQL completion with Virginia Nova Micro, a separate john-ai-learning datastore, and a direct-model fallback. Managed Agent Memory was not required or enabled by this SQL work. These names describe our implementation; they are not required resource names for another installation.

## 2. Confirm eligibility before creating resources

Check the current [AI Functions prerequisites](https://docs.couchbase.com/ai/build/ai-functions.html) and tenant eligibility. Confirm Query Service, required cluster configuration, deployment region and permission to enable functions. Do not resize a cluster merely to follow this example. Obtain the actual price and authorization first.

## 3. Create and verify the model key

1. Sign in to the correct Capella organization and open AI Data Plane → Access Control → Models.
2. Choose Generate API Key. Name it for the application and purpose; choose the deployed model's region, approved expiry and allowed source addresses.
3. Generate and download the credentials privately. Keep the key ID and token distinct. Do not commit the download or paste it into chat.
4. When entering a token field, use only the raw token, without quotes, `Bearer`, or `API_KEY=`. Use the downloaded credential file only where the form explicitly supports it.
5. Copy the model endpoint from the actual deployment. Test one small direct request using that token and model before configuring SQL. The bundled `scripts/probe_model.py` accepts a hidden token prompt. Test embeddings separately if embeddings are part of the workload; a completion does not verify Titan embeddings.

See [keys and access](keys-and-access.md) for key types, region scope, expiry, rotation and repeated sign-out. A Capella Model Service key is not an OpenAI provider key. An OpenAI-compatible client does not change which key is required. [Official key instructions](https://docs.couchbase.com/ai/api-guide/api-start.html).

## 4. Enable and bind the AI Function

In AI Data Plane → AI Functions (or the cluster's AI Functions page), choose Enable AI Functions, select the required functions and the AI Data Plane model. Supply its matching key ID/token or supported downloaded file, then select the intended operational cluster. Follow the current form through completion. Enabling one cluster does not enable others.

For the demo, enable Completion and bind Nova Micro. Use the actual deployed signature rather than assuming another function or version accepts the same payload. Private networking is a separate configuration choice; review its current region requirements and reversibility before enabling it. [Official setup](https://docs.couchbase.com/ai/build/ai-functions.html).

Wait for readiness, then run the constant completion below. A Healthy badge alone is insufficient.

```sql
SELECT RAW default:ai_completion({
  "system_prompt": "Reply only OK",
  "user_prompt": "Connection test",
  "max_tokens": 100
});
```

Require meaningful returned text, not merely SQL transport success. Nested error objects count as failure. Save a sanitized timestamp/request ID and result category.

## 5. Give the backend execution access

Create a dedicated Advanced cluster credential on the function host. Our verified role used **Global Function Execute** and **Query Curl Access**. These grant cluster-wide function execution, not execution of only ai_completion; they do not grant direct document access or administration. Review the exact role grant before applying it. Add only separately justified data privileges when a query actually reads documents.

Keep the runtime datastore credential separate. Store secrets outside the repository in a private file or server-side secret manager. Confirm TLS and the host from Capella. Never put credentials in frontend variables or browser code.

Check each network gate independently:

| Hop | Gate |
|---|---|
| Laptop/backend → cluster | Cluster allowed IPs |
| Laptop/backend → direct model | Model key allowed IPs |
| SQL function → model | Function-origin networking and model admission |

A laptop-only model rule does not automatically admit the SQL service. Do not guess its egress IP. Verify supported networking with current docs/support. Broad access requires explicit authorization. Our temporary unrestricted model-key diagnostic was restored afterward; it was not a permanent setup requirement. The shared cluster already had a broad rule; that observation is not a recommendation to copy it.

## 6. Test through the SDK, then the application

Use the same dedicated backend identity to execute a parameterized query:

```sql
SELECT default:ai_completion($payload) AS response;
```

Bind `payload` with the SDK's named parameters, not string interpolation. The observed result was a row containing a response array containing response text. Parse the actual envelope, reject embedded service errors, then validate the model's JSON against the application's classification schema. Do not accept malformed output as success.

Use bounded readiness/query timeouts. Preserve a direct inference fallback for query, connection, parsing and schema failures. Log a sanitized failure category and which path actually succeeded; reserve usage budget for both attempts. Do not log raw exceptions that may contain credentials.

For the Air implementation, the local SQL configuration was private; hosted opt-in used `AIR_SQL_ENABLED=1` and private `AIR_SQL_JSON`. Existing `AIR_MODEL_JSON` and `AIR_RUNTIME_JSON` stayed separate. These are application conventions, not Capella settings. Inspect the active adapter's expected schema before creating a config; do not invent a JSON shape from the variable name.

## 7. Verify the real flow and isolation

Run a normal request and a storm request through the local backend. Confirm SQL classification, direct recovery where designed, persisted results, receipts/history, Commands status and Cost all agree. Exercise a controlled fallback in an isolated test rather than breaking shared production credentials.

Open two independent visitor sessions. Trigger a storm in one and confirm the other run is unaffected. Verify visitor/run scoping in stored records and queries; separate visual state alone is not isolation.

## 8. Deploy only after local success

Put the authorized scoped credentials into sensitive server-side Vercel settings for the intended environment. Never copy production secrets into public examples. Check hosted network admission separately; laptop success does not establish Vercel connectivity. Keep direct fallback configuration intact.

Deploy and test the actual hosted storm flow. Confirm backend-reported SQL status, successful classifications, fallback labels, persisted per-visitor data and costs. Keep source on the authorized demo branch and match the deployed commit; do not merge the original demo as a side effect. Roll back or disable the SQL adapter if integration fails while retaining the known working direct path.

## 9. Account for usage honestly

Inspect the full completion envelope and SDK metadata. Our tested SQL function returned text and query metadata, not provider token usage. Query duration and result bytes are not tokens. Measured direct usage and estimated SQL usage must remain separate.

The demo estimates SQL tokens as UTF-8 bytes divided by four, rounded up, using the supplied prompts and returned text. Old rows may reconstruct output from saved JSON. This is not the model tokenizer and omits hidden overhead. Reference rates are not a verified Capella invoice. Failed SQL attempts remain unpriced. See [hosting and costs](hosting-and-costs.md) for limits, shared-resource allocation and billing caveats.

## 10. Diagnose and maintain

- Direct fails: check key type/value/expiry, endpoint, model/region and allowed origin first.
- Direct passes, SQL lacks privilege: inspect the exact execution/CURL role error.
- Direct passes, SQL returns 5010: check binding, function-origin admission and service response. Our incident persisted after the temporary IP test; support applied a workaround, then browser, scoped SDK, local and Vercel tests passed. The workaround mechanism and permanent code fix were not confirmed. Do not claim AV-150881 was proven to be the cause.
- Key generation signs out: inspect partial creation, reauthenticate once and make one controlled retry; report recurrence instead of creating duplicates.
- Healthy but inference fails: retain the failing request evidence; readiness is not functional verification.

The [incident log](incident-lessons.md) preserves the investigation and support-workaround status. When keys rotate or models are redeployed, update the function binding and any separate direct-model secrets, retest each caller, then retire old credentials. Record expiry reminders, current budget, rollback configuration and unresolved support ticket privately. Remove temporary network rules and disposable test resources after their approved window.

## Handoff evidence

Record each as passed, failed, disabled or untested: direct model; constant SQL; scoped SDK; local request; fallback; hosted request; visitor isolation; persistence; usage display. Include timestamp, deployment/commit, model/function identity, sanitized request IDs and remaining limitations. Do not label all of AIDP connected merely because SQL works.
