# 01. Scope and Assumptions

## 1. System under assessment

**SecureFinance Africa** is developing an AI-powered platform with three functions:

| Module | What it does | Output | Customer-facing effect |
|---|---|---|---|
| **M1. Identity verification** | Matches a customer's identity document and live selfie, checks the details against identity databases | Match score and pass/fail recommendation | Onboarding approved, delayed or rejected |
| **M2. Fraud detection** | Scores transactions and account behaviour for anomalies | Alert and risk flag | Transaction blocked, account frozen or escalated |
| **M3. Automated financial risk assessment** | Combines profile, behaviour and transaction history into a customer risk score | Risk tier and recommended limits or terms | Account limits, product eligibility, pricing |

**Decision model:** the system *recommends*; staff are expected to review. We assess whether that human oversight is meaningful in practice, because automation bias can turn a recommendation into a decision (see the oversight risks in Task 1).

**Data processed:** identity attributes, biometric images, device and location data, transaction records, derived risk scores.

## 2. Deployment scenario

| Phase | Scope | Assumption |
|---|---|---|
| **Phase 1: Launch** | Nigeria | SecureFinance Africa is established in Nigeria and is the data controller; customers are Nigerian residents |
| **Phase 2: Expansion** | EU market | The platform is offered to or its outputs are used in relation to **people located in the EU** |

Assessing both phases lets Task 3 show *when* each legal instrument applies, rather than assuming it always does.

## 3. Key assumptions

| ID | Assumption | Why it matters |
|---|---|---|
| A1 | The company is the data **controller** and also the **provider** of the AI system (it builds it) and its own **deployer** | Determines duties under the Nigeria Data Protection Act 2023 and the EU AI Act |
| A2 | **Decision:** M3 is treated as evaluating creditworthiness (it sets account limits, product eligibility and pricing for natural persons), so it is assessed as **Annex III point 5(b) high-risk** in Phase 2. This is the conservative reading; if SecureFinance limited M3 to fraud or AML risk scoring, the point 5(b) exclusion would apply. M1 (one-to-one biometric verification) and M2 (fraud detection) are likely excluded from Annex III high-risk, subject to design | EU AI Act Annex III points 1(a) and 5(b), checked in Task 3 (`05_task3_legal_compliance.md`) |
| A3 | Customers include people with thin credit files and people without formal documents | Raises exclusion and bias risk for M1 and M3 |
| A4 | No real data is used anywhere in this assessment | Required by the assessment brief |
| A5 | The assessment is pre-deployment, so risks are *proposed* and controls are *recommended* | Risk register uses "proposed control" |

## 4. Out of scope

- Live system testing or any third-party service (brief, section 5).
- Sector-specific financial regulation (e.g. central bank rules) and GDPR as separate instruments. These are acknowledged as relevant but are not covered by the approved resource set, so they are flagged as limitations rather than analysed.

## 5. Limitations

- Likelihood and impact ratings are analytical judgements.
- Legal conclusions are limited to what the approved sources support, and this is not legal advice.
- The fairness dataset is synthetic and shows the method; it does not prove how a real system would behave.
