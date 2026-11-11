# Catalog, policy and tracing

## Keep the roles distinct

The model proposes a response or tool call. The application/framework validates and executes allowed functions. Agent Catalog stores/retrieves tools, prompts and metadata; it is not the executing framework. Agent Tracer records observable activity. Managed Memory is a separate storage/recall service. [Catalog integration](https://docs.couchbase.com/ai/build/integrate-agent-with-catalog.html).

Inspect the installed `agentc` version and the project's public API usage before modifying integration code. Publish tools/prompts to the intended remote catalog, retrieve a known item, verify schema and version, and execute a bounded permitted call through the app. Named lookup does not demonstrate semantic tool search. A local list of demo commands is not proof of a live catalog. Internal SDK attributes seen in prototypes are not stable APIs to copy into new projects.

## Evidence to expose

Use the same run/session ID through these records:

| Stage | Minimum evidence |
|---|---|
| Policy match | Policy name, version/content revision and facts that matched |
| Selection | Candidate/selected tool names and concise selection reason |
| Execution | Actual call ID, validated arguments, result/status |
| Skipped or failed | Distinct state and actual reason; no fabricated result |
| Decision | Outcome supported by returned evidence and policy |
| Saved state | Receipt/reference and real persistence result |

Hotel policy revisions were content hashes, not Git SHAs. Do not silently change their meaning. Keep a published policy and application manifest in sync; mismatches should be explicit. Keep tool bindings request-local so one visitor's selection cannot overwrite another's.

## Tracer verification

Instrument a root span and relevant model/tool events. Model callbacks alone do not necessarily capture executed tool results; record results through the appropriate callback/tool integration. [Spans and callbacks](https://docs.couchbase.com/ai/build/agent-tracer/add-spans-callbacks.html).

After a small request, verify the exact session's trace was persisted and inspect it in Agent Tracer, selecting the correct cluster/app/date range. Check forwarding errors, dropped logs and flush behavior before a short-lived runtime exits. Console logs or UI activity are not remote trace readback. [Viewing traces](https://docs.couchbase.com/ai/build/agent-tracer/view-traces.html).

Do not store credentials, authorization headers or unnecessary personal content in traces. Use synthetic demo data. Display evidence and a short decision explanation, not a claim to expose internal model thoughts. Keep model calls, tool results, policy metadata and memory read/write distinct when diagnosing where a run stopped.
