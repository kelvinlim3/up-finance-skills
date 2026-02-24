# Prompt History

Come up with a PLAN.md for creating a set of skills for yourself to support me in analysing my finances. My financial data is available via the up API https://developer.up.com.au/. I want to be able to ask questions like "What am I spending the most money on?" and "How much money am I saving?" and "What are my regular expenses?" and "how should I budget?"

I responded to your open questions. Also the skills feel too specific to the example questions I provided, rather than focusing on the fundamental building blocks needed for financial analysis. Maybe we don't need multiple skills - maybe it's just one that knows enough about bin/up ? I'm not sure.

FYI I have put my Up token in .env. Please proceed with implementation.

What am I spending the most money on?

Exclude charity and look back 90 days. I want to get a better sense of base line recurring expenses vs "one-offs"

Go back 12 months, I want to get a sense of how much money I'm saving/distributing from regular salary, excluding some one off-large incomes.

The bank australia and westpac outgoing should be "canceled out" by matching incomings - this is shuffling money to and from to avoid fees on those accounts. Validate this, then exclude from analysis, and document in AGENTS.md

Re-present your previous tables/summary with these new changes

Include charity in final table as an outgoing - I set aside % of income for charity regularly but distribute it irregularly, but don't count it as "savings"

Remove things specific to me (e.g. the bank australia arrangement) from bin/up - that script needs to stay agnostic to who is using it. Any me-specific things need to be in AGENTS.md

How much do I typically spend on eating out each week?

Which restaurant is "Baked Since 95"?

Write a README.md, and include an analysis of "what would need to be true" (i.e. what needs to change in current state-of-the-art tools, how would the industry need to develop) for this skill to be distributable and useable by mainstream consumers.

Revisit saving rate analysis, and include 2Up transactions

Encode what you learned about 2Up into the finance skill - it will be the same for everyone using this tool.

Given you are providing financial summaries, what are some techniques you could apply to validate your output? Don't implement anything yet, just come up with options.

Encode 2, 3, 4, 5, 6, 8 and 10 into finance skill. Also, remove the summary commands from up command and don't rely on them - they may have quirks specific to user (update finance skill for this change as well). "Known values" (if any) will be provided by user in PERSONAL.md. If there is a known value that would be useful to compare against, inform the user in your output.

I want to get a sense of my regular expenses vs one-off, going back 3 months.

You didn't provide evidence of the validation step that the finance.md instructed you to take. Please figure out why not and update that skill accordingly.

now re-do the original analysis

I want to get a sense of my savings rate.

Thinking about buying an investment property. I can fund a 20% deposit from other holdings. How expensive a property can I afford to service off my salary, while still keeping a buffer in savings rate?
