# Example: integer response contract

Input: an approved local inventory API declares `GET /stock/{sku}` with a 200 JSON response containing required integer `quantity >= 0`. A captured response is `{"quantity":"3"}` with status 200 and content type application/json.

Expected output: implementation/schema discrepancy at `$.quantity`, string observed versus integer required. Do not silently coerce the response to make the check pass. Whether the application or schema should change needs the intended API contract.

Probe design includes: existing SKU baseline, unknown SKU with its declared error response, empty/boundary SKU cases supported by the schema, and quantity response type/range checks. The local JSON case validates only a deliberately small contract subset; it is not an OpenAPI parser.

Manual integration shape, not executed here:

```sh
schemathesis --version
schemathesis run --help
# After reviewing targets and current limiting/filter options:
schemathesis run openapi.json --url http://127.0.0.1:8000
```

The final line is only a command shape. Add the approved operation filters and budgets supported by the installed version before running it. A loopback address is not enough if schema references or redirects escape the target. Do not use a real token in documentation, shell history, or a saved reproducer.
