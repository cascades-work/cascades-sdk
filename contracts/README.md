# HTTP contract mirror

The canonical Cascades HTTP contract is maintained in the private platform
repository at:

`cascades-work/cascades:apis/cascades.openapi.yaml`

Preferred public path: `api/openapi.yaml`

Compatibility path: `contracts/api.yaml`

Both files must remain byte-equivalent to the canonical platform OpenAPI file
after LF normalization.

## Sync locally

```bash
python scripts/sync_contract.py ../cascades/apis/cascades.openapi.yaml
python scripts/verify_contract_mirror.py --against ../cascades/apis/cascades.openapi.yaml
```

CI checks out the private platform using the read-only
`CASCADES_READ_TOKEN` secret. Fork pull requests cannot receive that secret,
so maintainers must run the parity gate from an upstream branch before merge.
