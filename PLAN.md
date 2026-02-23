# Plan: Up Banking Finance Analysis Skills

## Overview

Build a set of Claude Code skills that query the Up Banking API to answer financial questions like spending breakdowns, savings rate, regular expenses, and budgeting advice.

## Architecture

### Token Management

The Up API requires a Bearer token. Store it in an environment variable `UP_API_TOKEN`. Skills will read from this and pass it via `Authorization: Bearer $UP_API_TOKEN` header.

**Setup:** User generates a personal access token from the Up app and adds `export UP_API_TOKEN=xxx` to their shell profile (or a `.env` file in this repo, gitignored).

### Core Script: `bin/up`

A single shell script that wraps the Up API. All skills invoke this script rather than calling `curl` directly. This keeps auth, pagination, rate-limit handling, and JSON parsing in one place.

```
bin/up accounts           # list all accounts
bin/up transactions       # list transactions (supports flags below)
  --since YYYY-MM-DD
  --until YYYY-MM-DD
  --category <slug>
  --account <id>
  --status SETTLED|HELD
  --limit N               # max transactions to fetch (handles pagination)
bin/up categories         # list all categories
bin/up tags               # list all tags
bin/up ping               # verify token works
```

Output is JSON, which Claude can then interpret and summarise.

**Pagination:** The API pages at ~100 results. The script should follow `links.next` automatically up to `--limit` (default: 1000).

**Rate limiting:** Respect `X-RateLimit-Remaining` header; sleep briefly if it gets low.

### Skills

Each skill is a `.claude/skills/*.md` file that defines a prompt template and invokes `bin/up` as needed.

#### 1. `spending` — "What am I spending the most money on?"

- Fetch settled transactions for a period (default: last 30 days).
- Group by category, sum amounts, sort descending.
- Present a ranked table of categories with totals and percentages.
- Exclude internal transfers between own accounts (these have specific category slugs).
- Optionally break down a single category into individual transactions.

#### 2. `savings` — "How much money am I saving?"

- Fetch all accounts to get current balances (saver vs transactional).
- Fetch income transactions (category: salary, interest, etc.) for the period.
- Fetch expense transactions for the period.
- Calculate: income − expenses = net savings.
- Show savings rate as a percentage of income.
- Show saver account balances and growth over the period.

#### 3. `regulars` — "What are my regular expenses?"

- Fetch 90 days of settled transactions.
- Identify recurring merchants/descriptions that appear multiple times at regular intervals.
- Group by merchant, show frequency (weekly/fortnightly/monthly/quarterly), average amount, and total.
- Flag any that have changed significantly in amount recently.

#### 4. `budget` — "How should I budget?"

- Depends on output of `spending` and `savings` analysis.
- Fetch 90 days of transactions for a broader picture.
- Categorise spending into needs (rent, groceries, utilities, transport) vs wants (dining, entertainment, shopping) vs savings.
- Compare against common frameworks (e.g. 50/30/20 rule).
- Suggest specific areas where spending could be reduced based on the data.
- Provide a proposed monthly budget based on actual income and spending patterns.

#### 5. `transactions` — General-purpose transaction search

- A lower-level skill for ad-hoc queries like "how much did I spend at Woolworths last month?"
- Accepts natural language, translates to appropriate `bin/up` flags.
- Presents results as a table with date, description, amount, category.

## Implementation Order

1. **`bin/up` script** — Foundation that everything else depends on.
2. **`transactions` skill** — Simplest skill, validates the script works end-to-end.
3. **`spending` skill** — Most directly answers the headline question.
4. **`savings` skill** — Requires account + transaction data.
5. **`regulars` skill** — Requires pattern detection logic.
6. **`budget` skill** — Builds on all of the above.

## File Structure

```
claude-up/
├── CLAUDE.md
├── AGENTS.md
├── PLAN.md
├── .env.example          # UP_API_TOKEN=up:yeah:xxxxxxxx
├── .gitignore             # .env
├── bin/
│   └── up                # Shell script wrapping the API
└── .claude/
    └── skills/
        ├── transactions.md
        ├── spending.md
        ├── savings.md
        ├── regulars.md
        └── budget.md
```

## Open Questions

1. **Script language:** Shell (`jq` for JSON) keeps it simple and dependency-free. Alternatively, a Python script would make pagination/grouping logic easier. Preference?
2. **Date defaults:** Default to last 30 days for most queries, last 90 for regulars/budget. Sensible?
3. **Caching:** Should we cache API responses locally to avoid repeated calls within a session, or always fetch fresh?
