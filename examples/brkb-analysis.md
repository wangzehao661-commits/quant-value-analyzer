# Berkshire Hathaway Class B (BRK.B) Validation Example

This example was generated to validate that `$quant-value-analyzer` works on a non-A-share company. It is for research and skill demonstration only, not investment advice.

## Input Prompt

```text
Use $quant-value-analyzer to analyze Berkshire Hathaway Class B (BRK.B) with the latest annual report, F-Score, B-Score, doubt tracking, and conservative DCF valuation.
```

## Report

# Berkshire Hathaway Class B (BRK.B) Quantitative Value Analysis

**Analysis date**: 2026-06-03  
**Ticker**: BRK.B  
**Market**: NYSE  
**Current price used in validation**: about $471.51  
**Primary sources**: Berkshire Hathaway 2025 Annual Report, Berkshire Hathaway 2026 Q1 Report, BRK.B market quote  
**Adaptation note**: Berkshire Hathaway is an insurance, investment holding, and operating-business conglomerate. Standard F-Score, B-Score, and FCF DCF outputs should be treated as screening signals, not mechanical investment conclusions.

## 1. Quantitative Health Check

### 1.1 Valuation Temperature

| Metric | Current value | Judgment |
|---|---:|---|
| Current price | about $471.51 | Near the conservative valuation midpoint in this validation run |
| Dividend yield | 0% | Berkshire does not pay dividends; shareholder return mainly comes from retained earnings and opportunistic repurchases |
| Valuation method | Operating-business DCF plus investment/cash adjustment | A standalone industrial-company DCF is not enough for Berkshire |

No extreme valuation doubt was triggered from this validation run. The key question is not whether Berkshire is a poor business; it is whether the current price offers enough margin of safety.

### 1.2 F-Score

The script returned:

| Item | Result | Score |
|---|---|---:|
| Net income positive | Passed | 1 |
| Operating cash flow positive | Passed | 1 |
| Operating cash flow greater than net income | Failed | 0 |
| ROA improved year over year | Failed | 0 |
| Long-term debt ratio improved | Passed | 1 |
| Current ratio improved | Passed | 1 |
| No equity issuance | Passed | 1 |
| Gross margin improved | Failed | 0 |
| Asset turnover improved | Failed | 0 |

**F-Score: 5/9**  
**Triggered doubts**: B, C, D

Interpretation: for Berkshire, this score is a warning to adjust the framework, not a direct distress signal. GAAP net income is heavily affected by investment portfolio mark-to-market changes, and ordinary industrial-company margin and turnover ratios are less informative for an insurance and holding company.

### 1.3 B-Score

| Dimension | Subitem | Score | Comment |
|---|---|---:|---|
| Earnings quality | Profit stability | 0/1 | GAAP earnings are volatile because of investment marks |
| Earnings quality | Cash flow quality | 0/1 | Operating cash flow to GAAP net income is distorted |
| Earnings quality | Capex efficiency | 1/1 | Free cash flow conversion remains solid |
| Business model | Gross margin level | 0.75/1.5 | Mixed business portfolio |
| Business model | ROE level | 0.75/1.5 | Recent average ROE is moderate to good |
| Capital allocation | Financial conservatism | 0.5/1 | Balance sheet is conservative, but insurance liabilities require separate interpretation |
| Capital allocation | Shareholder return | 0/1.5 | Zero dividend under the default rubric |
| Capital allocation | Capital discipline | 1.5/1.5 | Strong long-term capital discipline |

**Quantitative B-Score: 4.5/10**  
**Triggered doubt**: E

Full qualitative B-Score:

| Dimension | Score | Max |
|---|---:|---:|
| Quantitative subtotal | 4.5 | 10 |
| Customer stickiness and pricing power | 1.5 | 1.5 |
| Cycle resilience | 1.5 | 1.5 |
| R&D / brand investment persistence | 1.0 | 1.5 |
| Management integrity and ability | 1.0 | 1 |

**Full B-Score: 9.5/15**  
**Rating: AA / medium**

The raw quantitative score is conservative and partly distorted by Berkshire's structure. Qualitatively, the company scores better on moat, capital allocation, liquidity, and management quality.

## 2. Business Model And Moat

Berkshire's value comes from four broad sources:

1. Insurance operations and float.
2. BNSF railroad.
3. Berkshire Hathaway Energy and regulated utility assets.
4. Manufacturing, service, retail subsidiaries, public equities, cash, and short-term Treasury bills.

| Moat source | Evidence | Strength |
|---|---|---|
| Insurance float | Long-term low-cost capital source | Wide |
| Capital allocation | Long record of disciplined acquisitions, investments, and repurchases | Wide |
| BNSF rail network | Hard-to-replicate physical network | Wide |
| Utility assets | Regulated, stable, capital-intensive assets | Moderate |
| Reputation | High certainty of closing and long-term ownership culture | Wide |

**Overall moat rating: wide**

## 3. Management And Capital Allocation

Berkshire does not pay dividends, which triggers a weak shareholder-return score in the default rubric. For Berkshire, this doubt is mostly rejected: retained earnings, disciplined reinvestment, and repurchases at attractive prices are the main shareholder-return mechanisms.

The more relevant ongoing risk is succession and future capital allocation at Berkshire's current scale.

## 4. Valuation

Method used for validation: operating-business FCF DCF plus investment portfolio / cash adjustment.

Key assumptions:

| Assumption | Value |
|---|---:|
| Base FCF | $25.042B |
| Stage-one growth | 3.0% |
| Stage-one years | 5 |
| Terminal growth | 2.5% |
| Discount rate | 8.5% |
| Investment/cash adjustment | $534.9B |
| Equivalent Class B shares | 2.157335B |
| Current price | $471.51 |

Valuation output:

| Item | Value |
|---|---:|
| Stage-one present value | $107.408B |
| Terminal present value | $329.822B |
| Operating-business enterprise value | $437.229B |
| Equity value after investment/cash adjustment | $972.129B |
| Estimated intrinsic value per B share | $450.62 |
| Current price | $471.51 |
| Margin of safety | -4.64% |

Sensitivity:

| g1 / WACC | 7.5% | 8.5% | 9.5% |
|---|---:|---:|---:|
| 1% | $470.48 | $433.61 | $407.27 |
| 3% | $491.24 | $450.62 | $421.60 |
| 5% | $513.61 | $468.92 | $437.01 |

## 5. Doubt Tracking

### Doubt B: earnings quality

- Trigger: operating cash flow did not cover GAAP net income.
- Result: partly rejected.
- Reason: Berkshire's GAAP earnings include investment portfolio mark-to-market effects.
- Investment meaning: focus on operating earnings, underwriting quality, cash flow, and per-share book value growth.

### Doubt C: gross margin decline

- Trigger: consolidated gross margin declined.
- Result: partly rejected.
- Reason: consolidated gross margin is not very meaningful across insurance, railroad, utility, manufacturing, retail, and investment operations.
- Investment meaning: use segment operating profit and insurance combined ratio instead.

### Doubt D: asset turnover decline

- Trigger: asset turnover declined.
- Result: partly rejected.
- Reason: large cash, Treasury bill, and equity investment balances reduce ordinary turnover ratios.
- Investment meaning: use per-share intrinsic value growth and capital allocation quality instead.

### Doubt E: zero dividend

- Trigger: zero dividend yield.
- Result: rejected.
- Reason: Berkshire's shareholder return model is retained earnings plus opportunistic repurchases.
- Investment meaning: zero dividend is not automatically negative; judge retained-earnings return and repurchase discipline.

## 6. Final Summary

| Area | Judgment |
|---|---|
| Business quality | High-quality, resilient, wide-moat holding company |
| Quantitative score | Conservative and structurally penalized by GAAP and holding-company accounting |
| Moat | Wide |
| Management | Strong historical capital allocation; succession remains a monitoring point |
| Valuation | Around fair value to slightly expensive under conservative assumptions |
| Final view | Great company, but current price does not show an obvious margin of safety |

## Sources

- Berkshire Hathaway 2025 Annual Report: https://www.berkshirehathaway.com/2025ar/2025ar.pdf
- Berkshire Hathaway 2026 Q1 Report: https://www.berkshirehathaway.com/qtrly/1stqtr26.pdf

This example is for skill demonstration and research only. It is not financial advice.
