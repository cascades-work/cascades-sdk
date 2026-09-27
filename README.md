<p align="center">
  <a href="https://cascades.work">
    <img src="https://raw.githubusercontent.com/cascades-work/.github/main/assets/branding/social/repository-banner.png" alt="Cascades" width="640" />
  </a>
</p>

# Cascades SDK

The public developer surface for **Cascades**. This repository contains the
supported API contract, SDKs, schemas, examples, MCP/editor integrations, and
developer documentation needed to build with Cascades without exposing the
private application implementation.

The full Cascades platform repository remains private. See
[CONTRACT.md](./CONTRACT.md) for the public/private boundary.

## Repository map

```text
cascades-sdk/
├── README.md
├── CONTRACT.md
├── LICENSE
├── SECURITY.md
├── docs/
│   ├── concepts/
│   ├── authentication/
│   ├── flows/
│   ├── executions/
│   └── plugins/
├── api/
│   ├── openapi.yaml
│   └── schemas/
├── sdk/
│   ├── typescript/
│   ├── python/
│   └── java/
├── examples/
│   ├── hello-flow/
│   ├── webhook-trigger/
│   ├── scheduled-flow/
│   └── ai-workflow/
├── schemas/
│   ├── flow.schema.json
│   ├── task.schema.json
│   └── execution.schema.json
└── cli/
    └── public client interface
```

Existing implementations remain in place for compatibility:

- Python SDK: `src/cascades_sdk/`
- JS/TS contract package: `packages/cascades-sdk/`
- MCP server: `packages/mcp-server/`
- VS Code extension: `packages/vscode-extension/`

## Contract

The canonical HTTP contract is authored in the private Cascades platform at
`apis/cascades.openapi.yaml` and mirrored here to `api/openapi.yaml` and
`contracts/api.yaml`.

Current API contract version: **2.4.0**.

## Python

```bash
pip install cascades-sdk
```

```python
from cascades_sdk import CascadesClient, SessionCookieAuth

client = CascadesClient(
    "https://your-cascades-host",
    SessionCookieAuth("session-cookie-value"),
)
```

## Build with Cascades, not inside Cascades

External applications should depend on documented API operations, schemas,
SDKs, plugins, MCP tools, and supported extension points. Scheduler, execution
engine, workers, queues, persistence, private control-plane internals, and
deployment implementation are not public API.

## Contract synchronization

```bash
python scripts/sync_contract.py ../cascades/apis/cascades.openapi.yaml
python scripts/verify_contract_mirror.py --against ../cascades/apis/cascades.openapi.yaml
```

## Security

See [SECURITY.md](./SECURITY.md).

## License

This repository is distributed under the **Cascades Proprietary License —
SDK & Integration Terms**. See [LICENSE](./LICENSE).

You may use these SDK Materials to build your own applications, integrations,
automations, and plugins against documented Cascades interfaces. The license
does not grant rights to the private Cascades platform source or permission to
redistribute a modified or standalone Cascades SDK.
