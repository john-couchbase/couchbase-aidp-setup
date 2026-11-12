# Couchbase setup and troubleshooting

A separate skill for connecting Capella and the AI Data Plane, and finding the next useful check when something fails.

[Open the demo library](https://couchbase-demo-library.vercel.app/) · [Detailed guide](README-REFERENCE.md)

![Couchbase Internal Demo Library](docs/images/demo-library.png)

## What it helps with

- Choose the right API key and region.
- Test model inference and database access separately.
- Check SQL functions, memory, catalog, and tracing.
- Record failures clearly without exposing credentials.

For the full SQL setup, follow [SQL start to finish](couchbase-aidp-setup/references/sql-start-to-finish.md): keys, function binding, permissions, local testing, Vercel, fallback and costs.

## Start here

Copy the complete `couchbase-aidp-setup/` folder into `~/.codex/skills/` or `~/.claude/skills/`. Keep its references and scripts.

Start a new session and ask your agent to read the skill. For cloud uploads, package each complete skill folder as a ZIP. Installation details and environment limits are in the [detailed guide](README-REFERENCE.md).

Try this request:

> Use couchbase-aidp-setup. My model shows Healthy but prompts fail. Check the failing layer and explain what is verified.

## How it works

These files guide the coding agent. They do not connect services, start paid resources, or grant access on their own. The agent still needs your project, tools, and permission for the work.

Use the [design skills](https://github.com/john-couchbase/agent-skills) for interfaces and the [setup skill](https://github.com/john-couchbase/couchbase-aidp-setup) for backend connections.

## Updates and feedback

- Pull the latest repository before copying skills to another machine.
- Update installed folders and cloud ZIPs after changes. A GitHub push does not update them automatically.
- Report the skill name, your request, and the result that needs improving.

The [detailed guide](README-REFERENCE.md) preserves background, boundaries, and supporting references. These are practical project skills, not an official Couchbase brand manual or support package.
