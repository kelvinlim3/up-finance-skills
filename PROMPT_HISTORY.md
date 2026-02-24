# Prompt History

## 2026-02-24
Come up with a PLAN.md for creating a set of skills for yourself to support me in analysing my finances. My financial data is available via the up API https://developer.up.com.au/. I want to be able to ask questions like "What am I spending the most money on?" and "How much money am I saving?" and "What are my regular expenses?" and "how should I budget?"

## 2026-02-24
I responded to your open questions. Also the skills feel too specific to the example questions I provided, rather than focusing on the fundamental building blocks needed for financial analysis. Maybe we don't need multiple skills - maybe it's just one that knows enough about bin/up ? I'm not sure.

## 2026-02-24
FYI I have put my Up token in .env. Please proceed with implementation.

## 2026-02-24 08:56:50
What am I spending the most money on?

## 2026-02-24 08:58:33
Exclude charity and look back 90 days. I want to get a better sense of base line recurring expenses vs "one-offs"

## 2026-02-24 09:06:23
Go back 12 months, I want to get a sense of how much money I'm saving/distributing from regular salary, excluding some one off-large incomes.

## 2026-02-24 09:15:58
The bank australia and westpac outgoing should be "canceled out" by matching incomings - this is shuffling money to and from to avoid fees on those accounts. Validate this, then exclude from analysis, and document in AGENTS.md

## 2026-02-24 09:17:55
Re-present your previous tables/summary with these new changes

## 2026-02-24 09:20:04
Include charity in final table as an outgoing - I set aside % of income for charity regularly but distribute it irregularly, but don't count it as "savings"

## 2026-02-24 09:22:01
Remove things specific to me (e.g. the bank australia arrangement) from bin/up - that script needs to stay agnostic to who is using it. Any me-specific things need to be in AGENTS.md

## 2026-02-24 09:28:41
How much do I typically spend on eating out each week?

## 2026-02-24 09:31:22
Which restaurant is "Baked Since 95"?

## 2026-02-24 09:48:15
Write a README.md, and include an analysis of "what would need to be true" (i.e. what needs to change in current state-of-the-art tools, how would the industry need to develop) for this skill to be distributable and useable by mainstream consumers.

## 2026-02-24 12:03:04
Revisit saving rate analysis, and include 2Up transactions

## 2026-02-24 12:14:41
Encode what you learned about 2Up into the finance skill - it will be the same for everyone using this tool.
