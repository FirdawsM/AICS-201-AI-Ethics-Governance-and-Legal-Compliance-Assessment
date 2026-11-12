# 03. Task 1: Ethical Risk Identification (20 marks)

*Ratings here are preliminary; formal likelihood and impact scoring and owners are set in the Task 2 risk register.*

**Method.** Risks were identified by walking each module (M1 identity verification, M2 fraud detection, M3 risk assessment; see `01_scope_and_assumptions.md`) through the AI lifecycle and testing it against two sources: NIST SP 1270's three bias categories (systemic, statistical/computational, human) and the UNESCO Recommendation on the Ethics of AI (2021) values and principles. UNESCO is **non-binding** (it asks Member States to apply it "on a voluntary basis", para. 2), so it is used here as an ethical benchmark, not as law. Legal obligations are assessed separately in Task 3.

Where this document says a harm is *plausible*, it has not been demonstrated for this system: it is a hypothesis to be tested pre-deployment (Task 4 shows the method).

## Summary

| ID | Risk | Required theme | Modules | Prelim. priority |
|---|---|---|---|---|
| ER1 | Biased outcomes from unrepresentative or historically skewed data | Algorithmic bias | M1, M2, M3 | High |
| ER2 | Proxy variables recreate discrimination | Fairness | M2, M3 | High |
| ER3 | Excessive collection, retention and reuse of biometric and financial data | Privacy | M1, M2, M3 | High |
| ER4 | Customers cannot understand or contest decisions | Transparency | M1, M2, M3 | High |
| ER5 | Human review becomes a rubber stamp (automation bias) | Human oversight | M1, M2, M3 | High |
| ER6 | Disproportionate harm from false positives, with no effective remedy | Fairness / accountability | M1, M2 | High |

---

## ER1. Biased outcomes from unrepresentative or historically skewed data

**Cause.** Training data may under-represent some groups or encode past exclusion. SP 1270 describes *systemic* bias as present "in the datasets used in AI, and the institutional norms, practices, and processes across the AI lifecycle" (PDF p.15), and *statistical/computational* bias as arising when "the sample is not representative of the population" and algorithms "cannot extrapolate beyond those data" (PDF p.18). For a platform built for African markets, plausible gaps include customers without formal documents, thin credit histories, and regions with little data. UNESCO flags "regions where the data are scarce" (para. 66) and calls for training data that reflect populations (para. 67).

**Affected stakeholders.** Customers from under-represented groups (identity rejections, higher risk scores); SecureFinance (regulatory and reputational exposure); the wider public (exclusion from financial services).

**Likely consequences.** Systematically higher rejection or flag rates for some groups; unequal access to accounts and products; loss of trust.

**Proportionate safeguards.**
- Document training data provenance and coverage by group; test for performance differences *before* launch and monitor after (Task 4).
- Require acceptance thresholds for group-level error gaps as a go-live gate.
- Add a non-automated onboarding route for people the model handles poorly.

*Sources:* SP 1270 PDF pp.15, 18; UNESCO paras 28-29, 66-67.

---

## ER2. Proxy variables recreate discrimination

**Cause.** Even without using protected attributes, features such as location, device type, network provider, language or name patterns can act as proxies for them. SP 1270 explains that teams use proxies for concepts that cannot be measured directly, "which can create many risks" (PDF p.36), and lists "using proxy variables because they are easier to measure" as a statistical bias; it also notes that some observational fairness measures can increase discrimination depending on how protected attributes relate to the data (PDF p.40). Excluding protected attributes ("fairness through unawareness") is therefore not enough.

**Affected stakeholders.** Customers in particular regions, on lower-cost devices, or with atypical names or languages; SecureFinance.

**Likely consequences.** Indirect discrimination that is hard to see in aggregate accuracy figures; groups flagged as "risky" because of where or how they transact.

**Proportionate safeguards.**
- Feature review with a proxy-risk assessment before each model release; remove or constrain features with high proxy power.
- Test outcomes by group using several fairness measures, not one (Task 4).
- Keep protected attributes available *for auditing only*, under strict access control.

*Sources:* SP 1270 PDF pp.36, 40; UNESCO paras 28-29.

---

## ER3. Excessive collection, retention and reuse of biometric and financial data

**Cause.** M1 processes facial images and identity documents; M2 and M3 build detailed behavioural profiles. Without limits, data collected for verification can be kept too long, reused for new purposes, or exposed in a breach. UNESCO states that privacy "must be respected, protected and promoted throughout the life cycle" (para. 32), calls for privacy impact assessments for algorithmic systems (para. 34), and lists biometric data among data needing "full security" because disclosure "may cause exceptional damage" (para. 74). It also expects data subject rights, including access and erasure (para. 73).

**Affected stakeholders.** All customers; employees with data access; SecureFinance (breach liability).

**Likely consequences.** Identity theft and fraud if biometric data leaks (biometrics cannot be reissued like a password); loss of autonomy through function creep; regulatory action (see Task 3).

**Proportionate safeguards.**
- Data minimisation and fixed retention limits, with biometric templates stored separately from identity data and encrypted.
- Purpose limitation: no reuse of verification data for marketing or scoring without a separate lawful basis.
- A data protection impact assessment before launch; role-based access and audit logs.

*Sources:* UNESCO paras 32-34, 73-74. Binding duties under the Nigeria Data Protection Act 2023 to be added in Task 3.

---

## ER4. Customers cannot understand or contest decisions

**Cause.** Complex models can produce a flag or rejection with no usable reason. UNESCO says people should be told when a decision is informed by AI, should be able to request explanatory information, and should "have the option of making submissions to a designated staff member" able to review and correct the decision (para. 38); where impact is not "temporary, easily reversible or otherwise low risk", a "meaningful explanation" should accompany the decision (para. 40). A lack of transparency "could also undermine the possibility of effectively challenging decisions" (para. 37).

**Affected stakeholders.** Customers whose accounts are blocked, rejected or restricted; front-line staff who must explain outcomes; auditors.

**Likely consequences.** Customers cannot correct errors; staff cannot detect bias; the company cannot show its decisions were justified.

**Proportionate safeguards.**
- Reason codes for every adverse decision, in plain language, plus an explainability method suitable for reviewers (Task 4).
- Notice that AI is used, and a documented appeal route with a named reviewer and response time.
- Decision logs that allow each outcome to be reconstructed.

*Sources:* UNESCO paras 37-40, 43.

---

## ER5. Human review becomes a rubber stamp (automation bias)

**Cause.** The design says staff review recommendations, but heavy alert volumes, time targets and trust in the score can lead reviewers to accept the model's output by default. SP 1270 lists *automation bias* among the biases that arise in how people use automated output (PDF p.18 and its Fig. 5). UNESCO says ethical and legal responsibility must always be attributable to persons, and that an AI system "can never replace ultimate human responsibility and accountability" (paras 35-36); it also asks that effects of AI recommendations on "decision-making autonomy" be investigated (para. 51).

**Affected stakeholders.** Customers (errors pass unchallenged); reviewers (blamed for outcomes they could not realistically change); SecureFinance.

**Likely consequences.** Oversight exists on paper only; model errors and biases propagate into final decisions; accountability is unclear.

**Proportionate safeguards.**
- Track reviewer override rates and time-per-case; investigate rates near zero as a warning sign.
- Reviewer training on automation bias, with authority and time to override, and no penalty for disagreeing with the model.
- Escalation rule: decisions with severe or hard-to-reverse effects (e.g. account closure) require a documented human determination, consistent with UNESCO para. 26.

*Sources:* SP 1270 PDF p.18, Fig. 5; UNESCO paras 26, 35-36, 51.

---

## ER6. Disproportionate harm from false positives, with no effective remedy

**Cause.** Fraud controls are tuned to avoid missed fraud, which raises false positives: legitimate customers are blocked or frozen. For people who depend on a single account or mobile-money access, even short freezes cause real harm. UNESCO's proportionality principle says AI processes should not exceed "what is necessary to achieve legitimate aims" (para. 25), and that "effective remedy should be available against discrimination and biased algorithmic determination" (para. 29).

**Affected stakeholders.** Legitimate customers (especially low-income and unbanked); small businesses relying on the account; SecureFinance (complaints, churn).

**Likely consequences.** Loss of access to money, missed payments, financial exclusion; harm concentrated on groups already flagged more often (links to ER1-ER2).

**Proportionate safeguards.**
- Graduated responses (step-up verification, temporary limits) before freezes; freezes only on high-confidence or human-confirmed cases.
- A service-level target for resolving disputes, with fast-track handling for essential-access cases.
- Report false-positive rates by group as a standing governance metric.

*Sources:* UNESCO paras 25-26, 28-29.

---

## Cross-cutting note

The six risks interact: unrepresentative data (ER1) and proxies (ER2) raise false positives for some groups (ER6); weak explanation (ER4) and rubber-stamp review (ER5) stop those errors from being caught. The controls are therefore designed as a package, and Task 2 maps them to NIST AI RMF functions with owners and monitoring.
