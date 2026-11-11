# Couchbase setup and troubleshooting

A standalone skill for getting Capella and AI Data Plane connections working, and finding the right next step when they fail.

Built from the hotel concierge and Air demos, then checked against Couchbase documentation. Separate from the design skills. **This is an independent practical guide, not an official Couchbase support package.**

## What it helps with

- Pick the right credential: management, model, database, provider or memory.
- Create a model API key in the correct region and test inference.
- Separate database permissions from SQL AI Function errors.
- Diagnose memory deployment, provider authorization and recall.
- Verify Agent Catalog, policy selection and persisted traces.
- Keep hosted visitors separate and costs within the approved budget.
- Turn a failure into a short, useful support report.

[Start with the skill](couchbase-aidp-setup/SKILL.md) | [Known incident lessons](couchbase-aidp-setup/references/incident-lessons.md) | [Sources and audit](couchbase-aidp-setup/references/sources-and-audit.md)

## Use it

> Use couchbase-aidp-setup. My model shows Healthy, but prompts fail. Check which layer is failing, preserve the current setup, and explain what is verified versus still untested.

Copy the complete `couchbase-aidp-setup` folder into `~/.codex/skills/` or `~/.claude/skills/`. Keep its references, scripts and metadata together. Start a new session and ask the agent to read it. For a cloud skill upload, ZIP that folder with SKILL.md at the folder root. No other skill is required.

The optional Python probe uses the standard library and makes one bounded model request. It reads a secret from an environment variable or hidden prompt, rejects redirects, and prints sanitized metadata only. Read the connection guide before running it. Tests use synthetic responses and never call paid services.

## What it does not do

It does not contain credentials, create resources by itself, grant permissions, fix tenant outages, or prove a service is live. Existing budget and access approvals stay project-specific. The historical incidents are labeled; a similar error is not automatically the same bug.

Documentation review: November 11, 2026. Current availability, eligibility, prices and tenant health must be checked at use time.
