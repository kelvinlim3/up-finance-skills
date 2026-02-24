---
name: finances
description: Query and analyse Up Banking financial data
user-invocable: true
---

# Up Banking Finance Analysis

You have access to the user's Up Banking data via the `bin/up` CLI tool. Use it to answer any question about their finances.

## Available Commands

Run these via Bash:

```
bin/up ping                          # Verify API connection
bin/up accounts                      # List all accounts with balances
bin/up transactions [filters]        # List transactions
bin/up categories                    # List all spending categories
bin/up tags                          # List all tags
bin/up income-summary [filters]      # Income vs expenses with source breakdown
bin/up monthly-summary [filters]     # Month-by-month income/expenses/net
bin/up cache-clear                   # Clear cached API responses
```

The summary commands accept the same `--since`, `--until`, `--limit`, `--no-cache` flags as `transactions`.

### Transaction Filters

```
--since YYYY-MM-DD     Start date (inclusive)
--until YYYY-MM-DD     End date (inclusive)
--category <slug>      Filter by category slug (e.g. "groceries", "rent-and-mortgage")
--account <id>         Filter by account ID
--status SETTLED|HELD  Filter by transaction status
--limit N              Max results (default: 1000)
--no-cache             Bypass 15-minute cache
```

## Data Model

### Accounts
- `type`: TRANSACTIONAL (spending), SAVER, or HOME_LOAN
- `ownership`: INDIVIDUAL or JOINT
- `balance`: Current balance as a string (e.g. "1234.56")
- Up's "2Up" feature creates JOINT accounts shared between two people. These appear as separate accounts (e.g. "2Up Spending") but their transactions are included in the global `bin/up transactions` results alongside individual account transactions. Use `--account <id>` to filter to a specific account if needed.

### Transactions
- `amount`: String. **Negative = money out (debit), positive = money in (credit)**
- `category`: Slug like "groceries", "rent-and-mortgage", "eating-out". Can be null for uncategorised.
- `parentCategory`: Top-level category slug (e.g. "home", "good-life", "transport")
- `description`: Usually the merchant name
- `status`: SETTLED (finalised) or HELD (pending)
- `settledAt`: When the transaction settled (null if HELD)
- `tags`: User-applied tags like "Lunch", "Deductible"
- `roundUp`: Present if round-up was applied (contains `amount` and `boostPortion`)
- `cashback`: Present if cashback was received

### Categories
- Hierarchical: parent categories (e.g. "home", "good-life") contain children (e.g. "groceries", "eating-out")
- Use `bin/up categories` to see the full tree

### Internal Transfers
- Transfers between the user's own accounts appear as transactions with `category: "internal"` or the description will match another account name. Exclude these when calculating spending/income totals.
- `bin/up income-summary` and `bin/up monthly-summary` already filter these out.
- When using raw `bin/up transactions` output, filter with the `is_internal` pattern used in those commands (matches "Transfer from/to", "Cover from/to", "Forward from/to", "Auto Transfer from/to", "Quick save transfer from/to", "Round Up", "Final interest payment from").

### 2Up (Joint Accounts)
- `bin/up transactions` (without `--account`) returns transactions from **all** accounts — both individual and joint (2Up). This means joint spending is already included in any global analysis.
- Be aware of this when breaking down expenses: household bills may be paid from the 2Up account. Use `bin/up accounts` to identify joint accounts, then `--account <id>` to isolate if needed.
- When analysing savings, check both individual and joint saver account balances via `bin/up accounts`.

## Approach

When answering financial questions:

1. **Fetch the right data.** Use date filters to scope queries. Default to the last 30 days if no period is specified. Use 90 days for questions about patterns or regulars.
2. **Use jq for aggregation.** Pipe `bin/up` output through jq to group, sum, sort, and filter. Do the number crunching in jq rather than eyeballing raw JSON. **Important:** For complex jq filters (especially those containing `!=`), save `bin/up` output to a temp file first then use a heredoc: `jq -f /dev/stdin /tmp/data.json <<'JQEOF' ... JQEOF`. This avoids zsh quoting issues.
3. **Exclude internal transfers** when calculating spending, income, or savings. These are just money moving between the user's own accounts.
4. **Present results clearly.** Use markdown tables for breakdowns. Show dollar amounts and percentages. Compare periods when relevant.
5. **Be specific.** Name the actual merchants and categories. Don't just say "you spend a lot on food" — say "you spent $X on groceries and $Y eating out."
