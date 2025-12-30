# slama.dev (Hugo)

## Prerequisites

- [Hugo](https://gohugo.io/installation/) (extended version)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python, ruff)
- [Node.js](https://nodejs.org/) (html-validate, pa11y, prettier)
- [lychee](https://github.com/lycheeverse/lychee) (link checking)

## Setup

```bash
uv sync
npm install
uv run pre-commit install
```

## Development

```bash
./site serve   # Start dev server (with drafts)
./site build   # Build the site
./site check   # Run checks (HTML, links, accessibility)
./site upload  # Upload to VPS
./site all     # Build and upload (default)
```

## Pre-commit Hooks

Runs on commit via `uv run` and `npx`:
- **ruff** - Python linting and formatting
- **prettier** - SCSS formatting
