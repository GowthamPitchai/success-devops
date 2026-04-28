# Class 3 - Git Strategy

**Date:** 2026-04-28
**Status:** COMPLETE
**Cost:** Rs.0

---

## What I built

- Public GitHub repo: `success-devops`
- Connected local folder via `git init` + `git remote add origin`
- `.gitignore` (Python, Terraform, secrets, OS junk)
- Top-level `README.md` (portfolio-grade)
- `.gitkeep` files in empty folders so structure is preserved
- Branch protection rule on `main` (or ruleset)

---

## The 3 most important things I learned

1. **Trunk-based development** = one main branch + short-lived feature branches; what FAANG uses.
2. **Git tracks files, not folders.** Empty folders need `.gitkeep` to be visible on remote.
3. **Branch protection** enforces PR-only workflow, status checks, linear history -- the technical floor every real team has.

---

## Where I got stuck and how I escaped

- `app-02-streamhub` was missing on GitHub -> empty folder -> dropped `.gitkeep` files everywhere needed.

---

## The interview answer in 60 seconds

> "Trunk-based development on GitHub. `main` is protected: pull-requests required, status checks must pass, linear history enforced, no force-pushes, no deletion. Conventional Commits for messages -- `feat:`, `fix:`, `chore:` etc. -- so changelogs are auto-generatable. Branches live <2 days, squash-merged. Same model as Google, Stripe, Shopify. For multi-team monorepos I add `CODEOWNERS` so the right people are auto-assigned to PRs touching their area."

---

## Conventional Commits cheat-sheet

| Prefix | Use |
|--------|-----|
| `feat:` | new feature |
| `fix:` | bug fix |
| `docs:` | doc change only |
| `chore:` | tooling, deps |
| `refactor:` | restructure, no behavior change |
| `test:` | adding/fixing tests |
| `ci:` | pipeline change |

---

## Connection to next class

**Class 4 = run ShopWave's first service on my laptop using Docker.** Now that the repo + git workflow exists, every code change from Class 4 onwards goes through: feature branch -> commit -> PR -> review -> merge to main.
