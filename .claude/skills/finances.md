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
bin/up cache-clear                   # Clear cached API responses
```

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
- Transfers between the user's own accounts appear as transactions where the description matches internal transfer patterns. Exclude these when calculating spending/income totals.
- Filter with this jq pattern (matches "Transfer from/to", "Cover from/to", "Forward from/to", "Auto Transfer from/to", "Quick save transfer from/to", "Round Up", "Final interest payment from"):
  ```
  .description | test("^(Transfer (from|to)|Cover (from|to)|Forward (from|to)|Auto Transfer (from|to)|Quick save transfer (from|to)|Round Up|Final interest payment from)"; "i")
  ```
- Any user-specific transfer exclusions (e.g. round-trip transfers to other banks) should be documented in `AGENTS.md` or other user-supplied context.

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
6. **Check `PERSONAL.md`** (if it exists) for user-specific exclusions, known values, or configuration before running analysis.

## Validation (MANDATORY)

**Every financial analysis MUST end with a "Validation" section.** This is not optional. If the validation section is missing from your output, the analysis is incomplete. Include whichever checks below are applicable to the analysis performed, and always include "Show Your Working."

### Show Your Working (always required)
Include the date range, total transaction count before and after filtering, and what exclusions were applied. Example: "Based on 342 transactions from 2025-03-01 to 2025-05-31 (685 raw, 343 excluded: 315 internal transfers, 28 bank fee-avoidance)."

### Income = Expenses + Net (when computing income or expenses)
Verify that `income - expenses = net savings/surplus`. If it doesn't balance, there's a categorisation or filtering error. Present this check explicitly.

### Category Exhaustiveness (when grouping by category)
Sum category totals and compare to the overall total. The difference reveals uncategorised or missed transactions. Report if >1% of transactions are unaccounted for.

### Transaction Count Cross-Check (when presenting aggregated results)
Report total transactions included in the aggregation. Compare to the raw filtered count for the same period. A mismatch indicates a filtering bug.

### Spot-Check Samples (when presenting category or merchant totals)
Show 2-3 sample transactions from the largest categories so the user can eyeball whether they're categorised correctly. This catches systematic miscategorisation.

### Month-Over-Month Sanity Bounds (when covering 2+ months)
Flag any month where spending or income deviates by more than 50% from the median for that category. Large deviations aren't necessarily wrong, but they should be called out.

### Known-Value Anchoring (when PERSONAL.md has relevant values)
Compare computed values against known values from `PERSONAL.md`. Report any discrepancies. If a known value would be useful for validation but isn't in `PERSONAL.md`, suggest adding it.
