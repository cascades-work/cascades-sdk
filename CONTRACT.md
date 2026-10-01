# Cascades public developer contract

This repository is the public integration boundary for Cascades.

The private platform repository, `cascades-work/cascades`, contains the runtime
implementation. This repository exposes the supported contracts required to
build against Cascades without exposing the execution engine or private
application source.

## Contract layers

| Layer | Public artifact | Authority |
| --- | --- | --- |
| HTTP API | `api/openapi.yaml` | mirror of private platform `apis/cascades.openapi.yaml` |
| Compatibility mirror | `contracts/api.yaml` | compatibility path for existing SDK tooling |
| Stable JSON schemas | `schemas/*.schema.json` | developer-facing views derived from OpenAPI components |
| Python SDK | `src/cascades_sdk/` | public client and authoring surface |
| JS/TS contract package | `packages/cascades-sdk/` | JavaScript/TypeScript contract surface |
| MCP integration | `packages/mcp-server/` | public MCP adapter |
| VS Code integration | `packages/vscode-extension/` | editor integration |
| CLI boundary | `cli/` | documented public client surface |

## Private implementation boundary

The following are not part of the public contract:

- scheduler internals;
- worker and executor implementation;
- queue and persistence implementation;
- private control-plane services;
- internal admin routes and implementation-only endpoints;
- production infrastructure and deployment secrets;
- private tests, fixtures, build internals, and operational tooling.

A public contract describes what an integration may rely on; it does not expose
how Cascades implements that behavior.

## Source of truth

Canonical HTTP source:

`cascades-work/cascades:apis/cascades.openapi.yaml`

Public mirrors:

- `api/openapi.yaml`
- `contracts/api.yaml`

The contract-mirror workflow validates both copies against the private source
using a read-only repository token.

## Versioning

The OpenAPI `info.version` is the API contract version.

- patch: compatible clarification or documentation;
- minor: additive public capability;
- major: intentionally incompatible public contract change.

Incompatible changes to a documented public interface require a major contract
version change.

## Promotion model

Private platform change
→ canonical OpenAPI update
→ public mirror
→ parity validation
→ SDK validation
→ public release.

Do not copy private implementation code into this repository to satisfy a
public integration requirement. Add or extend a contract, schema, SDK method,
plugin interface, or documented endpoint instead.


## Machine-readable enforcement

The repository root contains `contract.manifest.json`, a deny-by-default declaration of the supported public surface and forbidden private implementation roots.

`scripts/validate_contract_boundary.py` validates that:

- required public artifacts remain present;
- forbidden private implementation roots are not copied into the SDK repository;
- the canonical and compatibility OpenAPI mirrors remain identical; and
- the published API contract carries a semantic-version-shaped version.

The `Public contract boundary` GitHub Actions workflow runs this validator on pull requests and on pushes to `main`.

These checks enforce the technical boundary. They do not replace or amend the legal terms in `LICENSE`; the license remains the authority for permitted use and redistribution.
