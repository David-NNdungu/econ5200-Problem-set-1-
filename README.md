# ECON 5200 Problem Set 1 — The Measurement Audit
David Ndungu

## Overview

I simulated 23,621 completed consumer orders over two years and recorded the true average before adding two measurement problems: 114 large B2B orders and 858 cancelled orders that appeared only in the second year's log.

I defined average basket value as consumer revenue divided by the number of completed consumer orders.

## Results

| Measure | Result |
|---|---:|
| True average basket value in 2024 | $61.52 |
| True average basket value in 2025 | $59.55 |
| True year-on-year change | -3.19% |
| Dashboard's reported growth | +8.59% |
| Growth overstatement | 11.78 percentage points |

I repaired each problem separately and then repaired both. Averaging the two repair orders attributed 6.23 percentage points of the gap to B2B orders and 5.55 to changed logging.

## Recommendation

I compared the median, a 10% trimmed mean, and the mean after excluding B2B orders. For each alternative, I explained its assumptions and when it would be inappropriate.

My initial recommendation was a trimmed mean after excluding B2B and cancelled orders. The AI review questioned whether that statistic reconciled to revenue per completed consumer order. It did not, because trimming removed valid consumer purchases.

I changed my recommendation to the arithmetic mean of completed consumer orders, excluding B2B accounts and cancelled orders consistently in both years. This recovered the recorded truth and reconciled to the saved finance ledger.

These results describe a simulation. Applying the correction to a real retailer would require checking account classifications, order status and revenue against independent records.

## Files

- `Econ_5200_PS1.ipynb`: completed notebook with calculations, explanations and the board slide.
- `src/basket_metrics.py`: reusable functions for the column audit and alternative basket statistics.
- `ai-appendix.md`: the P.R.I.M.E. prompt, full AI review response and change log.

## Verification

I used basic pandas filters, groupby operations, direct arithmetic and short loops. I used `scipy.stats.trim_mean` for trimming.

Seven module assertions passed on independent examples. Additional checks verified unique order IDs, the bias decomposition and reconciliation of completed consumer orders to the saved finance ledger.
