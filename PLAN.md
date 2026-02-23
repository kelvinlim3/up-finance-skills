# Plan: Up Banking Finance Analysis

## Overview

Build a single Claude Code skill backed by a `bin/up` CLI tool, giving Claude the ability to query the Up Banking API and reason about any financial question.

The skill doesn't encode specific analyses — it teaches Claude what `bin/up` can do and lets Claude compose the right queries and interpret the results for whatever question is asked.

## Architecture

### Token Management

The Up API requires a Bearer token. Store it in `UP_API_TOKEN` env var. The `bin/up` script reads it from there.

**Setup:** User generates a personal access token from the Up app and adds `export UP_API_TOKEN=xxx` to their shell profile (or a `.env` file in this repo, gitignored).

### Core Script: `bin/up`

A shell script (using `jq` for JSON processing) that wraps the Up API. Handles auth, pagination, rate limiting, and caching.

```
bin/up ping                # verify token works

bin/up accounts            # list all accounts (id, name, type, balance)

bin/up transactions        # list transactions with filters:
  --since YYYY-MM-DD
  --until YYYY-MM-DD
  --category <slug>
  --account <id>
  --status SETTLED|HELD
  --limit N                # max transactions to fetch (default: 1000)

bin/up categories          # list all categories (id, name, parent)

bin/up tags                # list all tags
```

Output is JSON. Claude interprets and summarises it.

**Pagination:** The API pages at ~100 results. The script follows `links.next` automatically up to `--limit`.

**Rate limiting:** Check `X-RateLimit-Remaining` header; sleep briefly if it gets low.

**Caching:** Responses are cached to `tmp/cache/` keyed by a hash of the query parameters. Cache files are valid for 15 minutes (checked via file mtime). The `--no-cache` flag bypasses the cache. `bin/up cache-clear` removes all cached data.

### Skill: `finances`

A single skill file at `.claude/skills/finances.md`. It contains:

- Description of what `bin/up` commands are available and what they return.
- Guidance on how to compose queries (e.g. "to analyse spending, fetch transactions for the period and group by category").
- Tips on interpreting Up API data (e.g. amounts are negative for debits, internal transfers have specific category slugs, round-ups are in a separate field).
- Conventions for presenting results (tables, percentages, comparisons over time).

The skill does **not** hardcode specific analyses. Instead it gives Claude enough context about the tool and data model to answer any financial question by composing the right `bin/up` calls and reasoning over the results.

## Implementation Order

1. **`bin/up` script** — The foundation. Start with `ping` and `accounts`, then `transactions` (with pagination + caching), then `categories` and `tags`.
2. **`.claude/skills/finances.md`** — The skill that teaches Claude how to use `bin/up`.
- jq
3. **Test end-to-end** — Verify with a few example questions.

## File Structure

```
claude-up/
├── CLAUDE.md
├── AGENTS.md
├── PLAN.md
├── .env.example           # UP_API_TOKEN=up:yeah:xxxxxxxx
├── .gitignore             # .env, tmp/
├── bin/
│   └── up                 # Shell script wrapping the API
├── tmp/
│   └── cache/             # Cached API responses (gitignored)
└── .claude/
    └── skills/
        └── finances.md    # Single skill teaching Claude how to use bin/up
```
