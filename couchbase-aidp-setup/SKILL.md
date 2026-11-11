---
name: couchbase-aidp-setup
description: Use when setting up or troubleshooting Couchbase Capella and AI Data Plane connections, API keys, model inference, SQL AI Functions, Agent Catalog, Agent Tracer, managed Agent Memory, or a hosted demo's backend. Not for visual-only design changes or as permission to create paid resources.
---

# Couchbase AI Data Plane setup

Help someone get a working connection and explain what is actually connected. This is a practical, independently maintained runbook built from the hotel and Air demos, not an official Couchbase support policy. Documentation was checked on November 11, 2026. Recheck changing APIs, eligibility, prices and incidents before acting.

## Start here

1. Identify the current project, entry point, environment, Capella organization, cluster and model region. Inspect the running implementation and sanitized config names. Legacy handover instructions may describe a different backend.
2. Identify the layer: browser login, management API, database, inference, SQL function, catalog/tracing or managed memory. Use [keys and access](references/keys-and-access.md) before asking for a key.
3. Record what is observed, what is only reported, and what is still untested. Read [incident lessons](references/incident-lessons.md) for familiar failure signatures; a familiar symptom does not establish the same cause.
4. Run the smallest authorized test at the failing layer. Preserve HTTP status, error category, UTC time and request ID; redact secrets and customer content. A web page loading, a listed model or a Healthy badge is not a successful inference test.
5. After a fix, repeat that test through the actual application runtime. Report connected, failed, disabled and unverified separately.

## Route to the relevant guide

| Need | Read |
|---|---|
| Which API key, where to create it, expiry, region, sign-out | [Keys and access](references/keys-and-access.md) |
| Direct model works/fails; database timeout; SQL inference | [Connection checks](references/connection-checks.md) |
| Memory provisioning, provider authorization, readback/recall | [Managed memory](references/managed-memory.md) |
| Tools, policy versions, selection, execution and traces | [Catalog and tracing](references/catalog-and-tracing.md) |
| Vercel, separate visitors, cost, pause/resume | [Hosting and costs](references/hosting-and-costs.md) |
| Known incidents and a short support report | [Incident lessons](references/incident-lessons.md) |
| Official references and evidence age | [Sources and audit](references/sources-and-audit.md) |

## Work within the current authorization

Explain the concrete change before modifying credentials, network access, roles or paid resources; follow the active environment's approval and credential-handoff rules. Existing permission only covers its stated resource, scope, duration and budget. This skill does not carry previous approvals into another project. Prefer inspection and targeted tests over redeployment.

Keep secrets server-side. Do not ask for keys in chat, screenshots, Git commits or frontend environment variables. Use the approved secret store or a private file outside the repository. Never print a raw credential, config, function definition or provider error that may echo one. A downloaded file's name is not evidence of its credential type.

A model test may cost money. Use one synthetic prompt, a bounded token limit, no automatic retries and the existing approved budget. The optional `python scripts/probe_model.py --endpoint URL --model MODEL` reads a raw token from `CB_MODEL_TOKEN` or a hidden terminal prompt and returns a sanitized result. Use only an endpoint independently verified from Capella; see its limitations in connection checks. Offline tests run with `python -m unittest discover -s scripts -p 'test_*.py'`.

## Completion means evidence

Give a short table: component, actual test, result, remaining action. Include the active runtime/region and evidence timestamp in the private project notes. Never equate saved receipts with managed memory, named tool lookup with vector search, a command reference with Agent Catalog, or UI activity with persisted traces. Describe observable tool choices and rationale, not private model thoughts.

This skill is self-contained. For a separate UI task, use the available Couchbase design/UI skills; they are optional and not dependencies of backend setup. Do not change design while repairing a connection unless asked.
