# Keys and access

## Choose the right credential

| Credential | What it authenticates | Where to inspect |
|---|---|---|
| Capella login | Browser organization/project access | Current signed-in account and roles |
| Management API token | Resource management | Organization/project API key settings |
| Model Service token | Inference against a deployed model | AI Data Plane → Access Control → Models |
| Cluster username/password | SDK, data and SQL++ access | Operational cluster → Connect / Cluster Access |
| Provider integration key | Upstream model provider used by a service | AI Data Plane → Integrations |
| Agent Memory token | One deployed memory server | Access Control → Agent Memory |

These are different authentication boundaries. Using the OpenAI SDK with a Capella base URL requires the Capella Model Service token. An OpenAI provider key belongs at OpenAI or its configured integration, not in the Capella model-token slot. A cluster username is not a Model Service API Key ID.

## Create a Model Service key

Confirm organization and the model's AWS region. In Access Control's Models view choose Generate API Key, give it a descriptive name and bounded expiry, select that region, add the approved source IP/CIDR, then generate and download immediately. Preserve the returned ID and token distinctly. Download is one-time; a later list entry does not recover the token. Current docs describe region-level model access; do not promise single-model restriction unless the current UI/API actually supports it. Changing caching, async processing or certain security features may require a new compatible key. [Official key guide](https://docs.couchbase.com/ai/api-guide/api-start.html).

Use current UI labels if navigation changes. On narrow screens tabs may become selectors. Match Virginia (`us-east-1`), Ohio (`us-east-2`) and Oregon (`us-west-2`) exactly; similarly named models in another region are not interchangeable.

## Token entry and validation

For a field labeled API Key Token, paste only the raw secret. Do not prepend `API_KEY=`, quotes or `Bearer `. `Bearer` belongs in the HTTP Authorization header, added by the client. Environment-file syntax is different: a `.env` file uses `NAME=value`; a raw-token file contains the token alone. Check empty files, whitespace, placeholder values and accidental wrong downloads privately. Do not output the secret or raw errors containing it.

Capella masks stored provider keys. Testing a separate local key does not prove that the masked integration has the same value. Verify integration identity or have its owner update the intended integration, then test the service dependency again.

## Browser signs out while generating

Record the visible page, exact action, UTC time and whether a success screen was ever shown. Reauthenticate once, inspect the key list for a partial creation, then make one controlled retry. If sign-out recurs, stop the loop and prepare a report. Do not diagnose a bad model token from a browser session loss or repeatedly create duplicate keys. Do not extend organization session policy or bypass authentication to work around it.

A documented Management API route may be an alternative when a valid authorized management credential exists; verify current schema and permissions first. Switching tools does not bypass a rejected permission or credential-handoff requirement.

## Independent network gates

Cluster allowlists, model-key allowed IPs and memory-server allowlists are separate. Authorizing a laptop does not authorize Vercel or cluster-originated AI Function calls. Verify the egress origin for each hop. Broad IPv4 access removes a network restriction even when credentials remain required; get specific authorization rather than silently adding it. Keep expiry and scope in private project records, not in this reusable skill.
