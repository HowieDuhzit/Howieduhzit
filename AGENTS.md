# Howieduhzit

GitHub profile README repository with automated stats, badges, and Web3 integration.

## What This Repo Is

- **Profile README** — the main `README.md` is auto-updated by GitHub Actions
- **Not a typical app** — no build/test/lint pipeline; it's scripts + workflows + markdown

## Key Gotcha

**`README.md` is machine-generated.** Manual edits get overwritten by workflows.
- `update-readme.yml` runs every 6 hours (GitHub stats, badges, Twitter, blog posts)
- `stats-generator.yml` runs daily (stats.json artifact)

If you need to change README content, edit the source in `scripts/update_readme.py` or the workflow YAML — not the README directly.

## File Map

| File | Purpose |
|------|---------|
| `README.md` | Auto-updated profile page |
| `README-HACKS.md` | Documents the automation features |
| `scripts/update_readme.py` | Python: fetches GitHub stats, Twitter, RSS, writes README |
| `custom-badges-generator.py` | Generates shields.io badge URLs for funding section |
| `solana-tip-component.jsx` | React component for Solana crypto tipping |
| `.github/workflows/update-readme.yml` | Runs `update_readme.py` every 6h (stats + badges) |
| `.github/workflows/stats-generator.yml` | Generates `stats.json` daily |
| `.github/FUNDING.yml` | GitHub Sponsors, Buy Me a Coffee, Solana, etc. |

## Python Dependencies

The update script requires: `PyGithub`, `requests`, `beautifulsoup4`, `lxml`

Install: `pip install PyGithub requests beautifulsoup4 lxml`

## Conventions

- Badge colors: `FF6B35` (orange), `9945FF` (Solana purple), `1a1a1a` (dark)
- Solana integration uses SNS domains (`howieduhzit.sol`) not raw wallet addresses
- Workflows commit as `GitHub Action` with emoji prefixes
