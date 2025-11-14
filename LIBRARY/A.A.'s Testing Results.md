# How the Analysis Works

## Data Alignment
Each date in 2025 is marked with the number of AI anomalies and whether that day falls within 24 hours or 72 hours of a solar, geomagnetic, or Schumann event.

## Window Testing
The model compares the average number of LLM incidents inside those environmental windows to the average outside them.

## Permutation Testing
It then shuffles the "window" labels 10,000 times to estimate how likely the observed difference is by chance.

- `perm_p < 0.05` → statistically significant overlap
- `perm_p ≥ 0.05` → no reliable correlation

## Expected Interpretation
A significant result shows that AI anomalies and environmental activity often overlap in time.

## Null Hypothesis
- **H₀:** Solar weather has no measurable effect on anomaly frequency
- **H₁:** Solar weather has a measurable effect on anomaly frequency

---

## CSV File Guide

### 🟢 daily_llm_with_flags.csv
Contains every calendar day in the dataset (data from before 11/10/2025).

**Columns include:** the number of LLM incidents and binary flags showing whether each day falls within 24h or 72h of any environmental event (Solar, Geomagnetic, Schumann, Other).

**Use it for:** time-series plotting, correlation checks, or adding new variables later.

### 🟣 window_comparison_by_subtype.csv
Summarizes the statistical tests. This file tells you which correlations are statistically meaningful.

**Columns:**
- `window` – 24h or 72h proximity
- `em_type` – Solar, Geomagnetic, Schumann, Other, or Any EM
- `mean_in` – average LLM incidents inside the window
- `mean_out` – average outside the window
- `IRR` – incident-rate ratio (how much higher the rate was inside)
- `perm_p` – p-value from 10,000 permutations

### 🔵 lag_curve_by_subtype.csv
Shows how incident averages shift 0–3 days after each environmental event type.

**Useful for:** spotting lag effects—for example, if anomalies peak one day after a geomagnetic storm instead of the same day.
