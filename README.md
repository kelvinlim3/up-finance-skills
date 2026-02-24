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

---

## What would need to be true for this to be a mainstream consumer product?

This project works well as a personal tool for someone comfortable with a CLI. But distributing it to mainstream consumers — people who just want to ask their bank "where's my money going?" — would require significant changes across the industry. Here's what would need to be true:

### 1. AI assistants need a standard way to install and use skills

Right now, this skill is a markdown file in a specific directory that only Claude Code knows how to find. There's no equivalent of an "app store" for AI skills. For mainstream distribution, we'd need:

- A **skill registry/marketplace** where users can browse, install, and manage skills — analogous to browser extensions or mobile app stores.
- A **standard skill format** that works across different AI assistants, not just Claude Code. Today every assistant (ChatGPT, Gemini, Claude) has its own incompatible plugin/tool/skill system, or none at all.
- **Sandboxed execution** so that installing a skill from a stranger doesn't give it access to your entire filesystem and shell. Current Claude Code skills run with the user's full permissions.

### 2. OAuth and secrets management need to be built into the skill runtime

This project requires the user to generate an API token, paste it into a `.env` file, and trust that the skill won't exfiltrate it. For consumers:

- Skills need a **built-in OAuth flow** — "Connect your Up account" that opens a browser, authorises, and stores the token securely without the user ever seeing it. MCP servers are moving in this direction but the UX is still developer-oriented.
- **Secrets must be isolated** per-skill, not stored in plaintext files. The runtime needs a keychain or vault abstraction.
- **Token scoping** matters too. Up's API currently offers a single all-or-nothing personal access token. A consumer product would need read-only scoped tokens so a finance analysis tool can't initiate transfers.

### 3. Banking APIs need to be more accessible

Up is unusual in offering a clean, well-documented REST API with personal access tokens. Most banks don't. For this to work broadly:

- **Open Banking standards** (like Australia's CDR, the UK's Open Banking, or the EU's PSD2) need to mature to the point where a consumer can connect any bank account to an AI assistant as easily as connecting Spotify to a smart speaker.
- **Aggregation services** (like Plaid, Basiq, Frollo) exist but add complexity, cost, and another party with access to your data. Ideally banks would offer direct API access with consumer-friendly auth flows.
- The **data models need standardising**. Up's category taxonomy, transaction format, and account types are all Up-specific. A skill that works across banks needs a common schema.

### 4. The AI needs to run somewhere the user trusts

This runs locally on your machine — your financial data never leaves your computer (except to call the Up API which is your own bank). That's a strong privacy property. But mainstream consumers use phones, tablets, and web browsers, not terminals. So:

- A **hosted version** would need to handle financial data, which means regulatory compliance (financial services licensing, data protection, potentially APRA oversight in Australia).
- Alternatively, **on-device AI** needs to get good enough to do the reasoning locally. Current local models aren't strong enough for the kind of multi-step financial analysis Claude does here.
- There's a middle ground where the AI runs in the cloud but the **data stays local** — the AI sends instructions ("fetch transactions, group by category") and the local device executes them. This is roughly what Claude Code does today, but packaging it for non-technical users is unsolved.

### 5. Personalisation needs to happen conversationally, not in config files

In this project, user-specific knowledge (like "exclude Bank Australia round-trips" or "charity isn't savings") lives in `AGENTS.md`, a markdown file the user edits. For consumers:

- The AI needs to **learn preferences through conversation** and persist them — "ignore those Bank Australia transfers" should just work without the user knowing about config files.
- These preferences need to be **portable and auditable** — the user should be able to see what the AI "knows" about their finances and correct it.
- There's a tension between **magic and transparency**. The more the AI silently learns, the harder it is for the user to understand why it's showing them what it's showing them.

### 6. Trust and accuracy standards are higher for financial advice

When Claude says "you're saving X% of your income", that number needs to be right. Today:

- There's **no verification layer** — the user has to spot-check the analysis themselves. A consumer product would need confidence scoring, the ability to drill into any number, and clear caveats about what's included/excluded.
- **Regulatory framing** matters. In Australia, personalised financial advice requires an Australian Financial Services Licence. A consumer product would need to carefully position itself as an information tool, not an adviser — similar to how budgeting apps disclaim today.
- The AI occasionally makes **arithmetic or categorisation errors**. For a consumer product, the aggregation logic (the `jq` equivalent) would need to be deterministic and tested, not generated on-the-fly by the AI.

### The gap in summary

The core capability works today: an AI can query a banking API, aggregate transaction data, and answer natural language questions about personal finances. What's missing is the infrastructure to deliver it safely, securely, and accessibly to people who don't use a terminal. That infrastructure — skill distribution, OAuth flows, banking API standards, privacy-preserving compute, conversational personalisation, and financial accuracy guarantees — is all being built in various places, but hasn't converged into a coherent consumer experience yet.
