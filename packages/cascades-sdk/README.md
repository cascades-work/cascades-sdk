# @cascades-work/cascades-sdk (npm)

Scoped **[noirstack](https://www.npmjs.com/org/cascades-work)** package on the public npm registry. This tarball ships the **mirrored HTTP contract** (`contracts/api.yaml`) plus **LICENSE** and a small **ESM entry** for path resolution — aligned with the **[cascades-sdk](https://pypi.org/project/cascades-sdk/)** Python package on PyPI.

The platform source of truth is **[cascades-work/cascades → `apis/cascades.openapi.yaml`](https://github.com/cascades-work/cascades/blob/main/apis/cascades.openapi.yaml)**. Sync the mirror in this repo before cutting a release (see the repo root **`README.md`** / **`RELEASE.md`**).

**Bump `version` in this directory’s `package.json` for each npm release** (npm does not allow re-publishing the same version). Prefer **`npm version patch|minor|major`** from **`packages/cascades-sdk`** (see **`RELEASE.md`**).

## Entry points

ESM consumers:

```js
import { apiYamlPath, packageRoot } from "@cascades-work/cascades-sdk";
// apiYamlPath → absolute path to bundled contracts/api.yaml
```

Subpath **`@cascades-work/cascades-sdk/api.yaml`** is declared in **`exports`** for tools that resolve the YAML path (behavior depends on your bundler / Node version — when in doubt, use **`apiYamlPath`** and `fs.readFile`).

The published tarball only includes paths listed in **`package.json` → `files`** (plus `package.json` itself). **`npm run build`** copies **`contracts/api.yaml`** and **`LICENSE`** from the repo root; **`prepack`** and **`prepublishOnly`** run **`build`** so **`npm pack`** and **`npm publish`** never ship stale or extra source files.

## Pack from repo root

After **`npm install`** at the SDK repo root:

```bash
npm run pack:npm -- --dry-run
# equivalent: npm pack -w @cascades-work/cascades-sdk --dry-run
```

Bare **`npm pack`** at the repo root will not work — the root `package.json` is **private** and only wires workspaces.

## Publish

Maintainers: **`RELEASE.md`** (npm section). Local:

```powershell
.\scripts\publish_npm.ps1
```

Requires **`npm login`** (or **`NPM_TOKEN`**) with permission to publish **`@cascades-work/cascades-sdk`** (`publishConfig.access` is **public**).

After the first successful publish, confirm org visibility and team access, for example:

```bash
npm access ls-packages noirstack
```

Then in the npm UI, ensure **`@cascades-work/cascades-sdk`** appears under the **cascades-work** org and grant the **developers** team read/write as needed.
