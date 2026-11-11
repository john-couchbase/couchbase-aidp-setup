# Validation record

November 11, 2026. This validates the skill and its helper, not current cloud connectivity.

- Official references reviewed for key types, model endpoints, SQL eligibility, RBAC, managed memory, catalog, tracing and cluster scheduling.
- Historical support explanations are explicitly labeled user-relayed reports; unresolved SQL/key creation issues are not presented as repaired.
- Independent application review passed six scenarios: wrong token for 503, SQL permission then internal error, receipts versus managed memory, stalled deployment/deletion, repeated browser sign-out, and hosted networking/budget isolation.
- Eight offline unit tests pass for endpoint normalization, unsafe URL rejection, nonempty completion, HTTP-200 error response, empty response, sanitized HTTP errors, redirect rejection and raw-token validation.
- No paid calls, key creation, resource changes or production connectivity tests were performed during this audit.
- The standalone package has no design-skill dependency and contains no tenant credentials or private deployment identifiers.

Run the helper tests from the repository root:

```sh
python -m unittest discover -s couchbase-aidp-setup/scripts -p 'test_*.py' -v
```
