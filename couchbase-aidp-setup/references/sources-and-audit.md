# Sources and audit boundary

Reviewed November 11, 2026. Revisit linked documentation before changing live systems; version, region, roles, UI labels and pricing can change.

## Primary references

- [AI Data Plane overview](https://docs.couchbase.com/ai/get-started/intro.html)
- [Management and Model Service keys](https://docs.couchbase.com/ai/api-guide/api-start.html)
- [Model endpoint and inference calls](https://docs.couchbase.com/ai/api-guide/api-use.html)
- [AI Functions prerequisites and binding](https://docs.couchbase.com/ai/build/ai-functions.html)
- [Cluster credential types](https://docs.couchbase.com/cloud/clusters/cluster-rbac.html)
- [AI Data Plane errors](https://docs.couchbase.com/ai/api-guide/api-errors.html)
- [Managed memory deployment](https://docs.couchbase.com/agent-mem/current/managed/deploy-agent-mem-managed.html)
- [Memory keys](https://docs.couchbase.com/agent-mem/current/api-guide/managed/api-start.html)
- [Memory access levels](https://docs.couchbase.com/agent-mem/current/api-guide/managed/api-intro.html)
- [Memory SDK quickstart](https://docs.couchbase.com/agent-mem/current/get-started/get-started-agent-mem-managed.html)
- [Memory API](https://docs.couchbase.com/agent-mem/current/agent-memory-api-reference/rest-api.html)
- [Catalog](https://docs.couchbase.com/ai/build/integrate-agent-with-catalog.html)
- [Trace instrumentation](https://docs.couchbase.com/ai/build/agent-tracer/add-spans-callbacks.html)
- [Trace inspection](https://docs.couchbase.com/ai/build/agent-tracer/view-traces.html)
- [Cluster off/on behavior](https://docs.couchbase.com/cloud/clusters/off-on-schedule.html)
- [OpenAI errors](https://developers.openai.com/api/docs/guides/error-codes)

## Project evidence used

The supplied conversation contains repeated setup tests and user-relayed support explanations. Local source review covered Air's current README, legacy migration guide, direct-model adapter and HTTP entry point; Harborline's README, operations notes, memory diagnostics and integration adapter. Project filenames are provenance, not assumed installation paths for future users. Private configuration files, tokens and tenant IDs are not bundled.

Current-code distinctions found during this audit: Air's hosted direct-model path is separate from its legacy SQL-capable implementation; its command catalogue is not Agent Catalog integration. Hotel database receipts and trace logging are separate from managed-memory readiness. References that say “healthy” or “working” are dated observations, not live guarantees.

This audit did not start cloud resources, create keys, re-test production inference or repair the unresolved key-creation sign-out. Future users should gather new evidence before claiming a service is currently connected.
