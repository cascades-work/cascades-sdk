# Cascades (VS Code Extension)

Cascades workflow and orchestration client for VS Code. Browse, run, and monitor workflows directly from the editor.

## Features

- **Cascades: Getting Started** — guided onboarding walkthrough
- **Cascades: Set Session Cookie** — authenticate with your Cascades deployment
- **Cascades: Open Dashboard** — view workflows, triggers, and run history
- **Cascades: Open Workflow Builder** — visual DAG editor for workflows
- **Cascades: List Workflows** — browse the workflow catalog
- **Cascades: Show Run Status** — check execution results by run ID
- **Cascades: Insert Code Example** — pasteable Python snippets for common workflows
- **Cascades: Open Documentation** — quick section picker with all doc URLs

All error messages include links to the relevant documentation for quick troubleshooting.

## Commands

| Command | Description |
|---|---|
| `Cascades: Getting Started` | Onboarding walkthrough with setup steps |
| `Cascades: Set Session Cookie` | Authenticate with your deployment |
| `Cascades: Open Dashboard` | Opens the web dashboard |
| `Cascades: Open Workflow Builder` | Opens the visual DAG builder |
| `Cascades: List Workflows` | Browse the workflow catalog |
| `Cascades: Show Run Status` | Check execution results |
| `Cascades: Open Documentation` | Quick section picker |
| `Cascades: Insert Code Example` | Pasteable Python snippets |
| `Cascades: About` | Version and links |

## Configuration

| Setting | Default | Description |
|---|---|---|
| `cascades.baseUrl` | `https://cascades.work` | Your Cascades deployment URL |
| `cascades.sessionCookie` | — | Session cookie (set via the Authenticate command) |

## Links

- Cascades Platform: https://cascades.work
- Documentation: https://cascades.work/docs
- Company: https://noirstack.com
- Support: https://github.com/cascades-work/cascades-sdk/issues
- GitHub: https://github.com/cascades-work/cascades-sdk
- Extension Repository: `packages/vscode-extension/`

## Publishing

From `packages/vscode-extension/`:

1. Install dependencies: `npm install`
2. Compile extension: `npm run compile`
3. Package VSIX: `npx vsce package --no-dependencies`
4. Publish: `npx vsce publish`
