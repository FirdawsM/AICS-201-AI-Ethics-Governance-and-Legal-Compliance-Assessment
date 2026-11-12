# 06. Task 4: Algorithmic Fairness and Explainability

*All numbers come from `analysis/fairness_analysis.py` and are saved in `evidence/`.*

## 1. What is evaluated

Module **M3** (automated financial risk assessment) is the focus. It is the module most likely to be high-risk (Task 3) and the one where proxy variables (ER2) and unequal false outcomes (ER6) matter most. The model recommends *approve* or *decline* for an account limit. Staff review follows, but we test the model's recommendation, because Task 1 argues that review can become rubber-stamping (ER5).

## 2. Dataset and assumptions

Synthetic, 8,000 customers (see `data/data_dictionary.md`). Groups: **urban vs rural** and **male vs female**, plus the intersection **rural women vs urban men**.

- Underlying creditworthiness has the same distribution in every group, so a fair model should treat the groups alike.
- Two proxy features (basic phone, location changes) relate to group but not to repayment.
- Past decisions used for training were biased against basic-phone and thin-file customers. This planted bias gives the method something to find. The results show the method, not the behaviour of a real system.
- Because the data is synthetic, we know who would really have repaid (`repaid_true`). In a real deployment this is unknown for declined customers (the *selective labels* problem), so fairness metrics could only be estimated on a controlled sample of approvals.

## 3. Fairness measures and why

No single definition of fairness is correct, and they can conflict (S12, S3). I use four, each answering a different question:

| Measure | Question it answers | Why relevant here |
|---|---|---|
| **Impact ratio** (approval rate of group ÷ reference group) | Are groups approved at similar rates? | Common screening test. The four-fifths rule (0.8) is a rule of thumb, not a legal test under the NDPA or EU AI Act |
| **Equal opportunity** (approval rate among customers who *would repay*) | Do creditworthy people get the same chance? | Directly measures wrongful decline, the harm in ER6 |
| **False positive rate gap** (approval rate among those who would *not* repay) | Are risky customers approved at similar rates? | Completes equalised odds. Tests whether one group is let through more easily |
| **Predictive parity** (repayment rate among approved) | Is an approval equally reliable for every group? | Shows the conflict between definitions |

## 4. Results

Three model variants, all set to approve about 62% overall so they are comparable. Test set: 3,200 customers.

| Variant | What it is |
|---|---|
| **V0 baseline** | All features, trained on past decisions |
| **V1 proxies removed** | Drops basic phone and location changes, still trained on past decisions |
| **V2 outcome labels** | All features, trained on actual repayment outcomes |

| Comparison | Variant | Impact ratio | Equal opportunity gap | FPR gap | Predictive parity gap |
|---|---|---|---|---|---|
| Rural vs urban | V0 | **0.82** | **−12.3 pp** | −8.9 pp | +0.6 pp |
| Rural vs urban | V1 | 0.88 | −8.9 pp | −4.2 pp | −0.7 pp |
| Rural vs urban | V2 | 0.99 | −1.2 pp | +2.5 pp | −2.0 pp |
| Rural women vs urban men | V0 | 0.81 | −12.6 pp | −12.7 pp | +3.4 pp |
| Female vs male | V0 | 1.00 | −0.2 pp | −1.7 pp | +1.5 pp |

*Bootstrap 95% intervals for the baseline rural vs urban comparison: impact ratio 0.77 to 0.87; equal opportunity gap −16.4 to −8.5 pp.*

**Findings**

1. **The baseline disadvantages rural customers who would repay.** Their approval rate is about 12 points lower, and the interval excludes zero. This is the clearest result.
2. **The impact ratio alone understates it.** At 0.82 it sits just above the 0.8 rule of thumb, and its interval crosses 0.8. Equal opportunity shows the harm more clearly.
3. **The definitions disagree.** Predictive parity is almost perfect (+0.6 pp) while equal opportunity fails badly. A team checking only precision would pass the model.
4. **There is no evidence of a gender gap** in this data, even though women have thinner files. Absence of a gap is also a result and should be reported.
5. **Rural women vs urban men** looks no worse than rural vs urban on equal opportunity (−12.6 vs −12.3 pp, a 0.3 pp difference well inside the ±4 pp bootstrap interval), so that gap is not shown to be wider. The intersection is clearly worse only on the false positive rate gap (−12.7 vs −8.9 pp). Intersectional groups still need their own check, because a single-attribute test can hide a gap that only appears in a subgroup.
6. **Removing proxies helps only partly** (V1): the label bias still enters through history length. **Fixing the labels** (V2) closes most of the gap. This points to training data as the root cause, not just features.

## 5. Explainability and decision review

**Global.** Permutation importance and coefficients (`evidence/explainability_importance.csv`) show income stability dominates, as it should. The basic-phone proxy ranks above history length and has a **negative** coefficient, so it is being used to penalise customers, though it has no link to true repayment here.

**Local decision review.** 262 rural customers who would have repaid were wrongly declined by the baseline. A counterfactual check changes only `device_basic` to 0 for each one: **48% would have been approved**. A reviewer's sheet for ten of them (`evidence/decision_review_sheet.csv`) lists the top negative driver and whether the decision flips. This is a practical review step: if changing a proxy alone flips the decision, the decision should be escalated, not confirmed.

## 6. Recommended controls

| Finding | Control | Links to |
|---|---|---|
| Rural gap in wrongful declines | Make **equal opportunity gap ≤ a stated threshold** (for example 5 pp, to be set by the AI Governance Committee) a go-live gate, reported with confidence intervals | ER1 |
| Proxy reliance | Proxy-risk review of every feature before release. Block device type and location-change features from M3 | ER2 |
| Biased labels | Replace past-decision labels with outcome labels. Run a **controlled approval sample** to get outcomes for customers who would otherwise be declined | ER1, ER6 |
| Metrics disagree | Report several measures, never one. Include intersectional groups | ER1 |
| Wrongful declines persist | Counterfactual flag in the reviewer screen. Human reviewers must see the main drivers and can override | ER4, ER5 |
| Drift after launch | Monthly group-level monitoring with the same measures | NIST MEASURE, MANAGE |

## 7. Limitations

- Synthetic data with planted bias: it shows the method, not real-world prevalence.
- Only M3 was tested. M1 (identity verification) and M2 (fraud detection) were not, so group-level error rates for them must be measured on pilot data before launch.
- Two group attributes only. A real assessment would also consider ethnicity, language, disability and age, subject to the NDPA's rules on sensitive data.
- A simple logistic model keeps explanations exact. More complex models would need tools such as SHAP and may behave differently.
- Group-specific decision thresholds could also reduce gaps but risk unlawful differential treatment. They are not recommended without legal advice.
