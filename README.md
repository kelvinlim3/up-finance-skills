# claude-up

A Claude Code skill for analysing personal finances via the [Up Banking API](https://developer.up.com.au/).

Ask natural language questions about your money — "what am I spending the most on?", "how much am I saving?", "what are my regular expenses?" — and get answers backed by real transaction data.

## How it works

A shell script (`bin/up`) wraps the Up API, handling authentication, pagination, rate limiting, and caching. A Claude Code skill (`.claude/skills/finances.md`) teaches Claude how to use the script and interpret the data. Claude composes the right queries and uses `jq` to aggregate results for whatever question you ask.

There are no hardcoded analyses. The skill gives Claude the building blocks (account data, transaction data with filters, category taxonomy) and lets it reason about any financial question.

## Setup

1. Get a personal access token from the Up app (or https://api.up.com.au)
2. Copy `.env.example` to `.env` and add your token
3. Verify it works: `bin/up ping`
4. Ask Claude a question about your finances, or invoke the skill with `/finances`

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- `jq` for JSON processing
- `curl` for API requests
- An [Up Banking](https://up.com.au) account with API access

## Example questions

- "What am I spending the most money on?"
- "How much do I spend on eating out each week?"
- "What are my regular recurring expenses?"
- "How much money am I saving each month?"
- "How should I budget?"
- "Show me all my transactions at Woolworths last month"

## Personalisation

The script (`bin/up`) is user-agnostic. User-specific configuration (like transactions to exclude from analysis, how to treat certain income/expense categories) goes in `PERSONAL.md`, which Claude reads automatically (referenced from `CLAUDE.md`). This keeps the tool generic while allowing per-user customisation.