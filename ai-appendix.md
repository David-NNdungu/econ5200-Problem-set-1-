# AI Appendix — Phase 4: P.R.I.M.E. Adversarial Review

This appendix records my Phase 4 adversarial review: the exact prompt, the complete model response, and the changes made after evaluating the response.

## Exact Prompt

```text
[Prep] Act as a partner reviewing an analytics deliverable before it
goes to a client board. You are looking for the objection that would
embarrass us in the room.

[Request] I audited a retailer's "average basket value" metric. I found
the naive mean was inflated by a right-skewed B2B tail and by a change
in what was logged between years. I recommend the dashboard show a
trimmed mean with an explicit B2B exclusion rule. Give me the three
strongest objections to that recommendation, ordered by how likely the
client is to raise them, and for each one tell me what evidence would
settle it.

[Iterate] Be specific to this metric. Do not give me generic data
quality advice.

[Mechanism Check] For each objection, say whether it is a question
about the data, about the statistic, or about the business definition
of the metric -- these need different kinds of answer.

[Evaluate] Which single additional analysis would most reduce our
exposure?
```

## Raw Model Response (Unabridged)

1. "Why doesn't your corrected average reconcile to consumer revenue divided by completed consumer orders?"
Type: Business definition, with a statistical consequence.
A trimmed mean drops real purchases as well as unwanted observations. If average basket value is meant to equal revenue per completed consumer transaction, trimming changes the metric. Right skew among legitimate consumer orders is not itself measurement error.
Evidence that settles it: For each year, reconcile the retained completed consumer orders to an independent finance ledger, then compare revenue/order count with the proposed trimmed mean. Show the number of orders and revenue removed by trimming. If the trimmed mean fails this identity, use the arithmetic mean on the correctly defined population and label any trimmed series as a separate typical-basket indicator.

2. "Are you comparing the same kinds of orders in both years?"
Type: Data.
Excluding B2B does not repair newly logged cancelled orders. The cancellations may have intended basket values but no recognized revenue, so they should not enter a completed-order measure.
Evidence that settles it: Build a year-by-customer-type-by-status table. Recompute both years under the same completed-consumer rule and verify those order IDs and amounts against finance. Recalculate the growth rate with each fault repaired separately and with both repaired.

3. "How did you choose the trim rate and decide which large orders are B2B?"
Type: Statistic for trimming; business definition for B2B classification.
A price cutoff can remove legitimate large consumer orders. A 10% trim at each end also removes 20% of valid transactions, and a changing tail can make its growth rate differ from revenue growth.
Evidence that settles it: Identify B2B using account classification rather than basket size. Show results at 0%, 5%, 10% and 20% trimming on the same completed-consumer population, and check whether the recommendation changes. In real data, inspect account records and ambiguous classifications.

The single most useful additional analysis is the finance reconciliation in objection 1. It simultaneously tests the metric definition and whether the proposed statistic estimates it. A stable trimmed series is not sufficient evidence that it measures average revenue per completed consumer order.

## Changes Made After the Review

- I kept the raw review unchanged, including the objections to my initial recommendation.
- I tested the strongest objection by matching completed consumer order IDs, amounts, counts and revenue to the finance ledger saved before contamination.
- I calculated the number of valid orders and the revenue removed by trimming.
- I changed my recommendation from a 10% trimmed mean to the arithmetic mean of completed consumer orders after the reconciliation.
- I checked the logging concern using customer-type and order-status counts and the four repair scenarios.
- I checked that averaging the two repair orders accounted for the interaction between the faults.
- I compared 0%, 5%, 10% and 20% trimming on the same completed consumer population.
- I retained account type as the B2B exclusion rule rather than using a basket-value cutoff.
- I limited my confidence statement to the simulated data and identified the independent checks needed for a real retailer.
- I revised the board slide and README to reflect the final recommendation.

## Result of the Additional Analysis

The strongest objection was that the trimmed mean might not measure revenue per completed consumer order.

The reconciliation confirmed this concern. In 2024, the corrected arithmetic mean was $61.52, while the 10% trimmed mean was $51.95. In 2025, the corrected arithmetic mean was $59.55, while the trimmed mean was $49.83.

Trimming removed 2,236 valid consumer orders in 2024 and 2,486 in 2025. Their revenue belonged in the average, so removing them changed the meaning of the metric.

I therefore revised my recommendation to the arithmetic mean of completed consumer orders, excluding B2B accounts and cancelled orders consistently in both years. This reconciled to the saved finance ledger.

The corrected metric showed a 3.19% decline, compared with the dashboard's reported 8.59% growth. The growth overstatement was 11.78 percentage points.
