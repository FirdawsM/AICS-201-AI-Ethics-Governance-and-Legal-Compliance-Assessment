# 04. Task 2: AI Governance and Risk Management (25 marks)

*The risk register is in `risk_register/risk_register.csv` (12 risks). Owners are roles within the organisation. Timelines and thresholds marked "proposed" are design recommendations, not requirements taken from a source.*

## 1. Approach

SecureFinance Africa adopts the **NIST AI Risk Management Framework 1.0 (AI RMF)** as its governance backbone. The AI RMF is **voluntary** ("use-case agnostic", NIST AI 100-1), so adopting it is a management decision, not a legal duty. Legal obligations are assessed separately (Task 3), and the framework is used to organise how the company meets and evidences them.

The AI RMF Core has four functions. **Govern** is cross-cutting and applies throughout; **Map, Measure and Manage** operate on each system. The sections below apply each function to the platform's three modules: identity verification (M1), fraud detection (M2) and risk assessment (M3).

The framework's trustworthiness characteristics (valid and reliable; safe; secure and resilient; accountable and transparent; explainable and interpretable; privacy-enhanced; fair with harmful bias managed) are used as the checklist for what "good" looks like at each go-live gate.

## 2. GOVERN: responsibilities and structure

AI RMF GOVERN 2.1 requires roles, responsibilities and lines of communication to be "documented and clear", and GOVERN 2.3 requires executive leadership to take responsibility for AI risk decisions.

| Role | Responsibility |
|---|---|
| **Board / Executive Sponsor (CEO)** | Owns AI risk appetite; accepts residual High risks; final go/no-go (GOVERN 2.3) |
| **AI Governance Committee** (CRO chair; Legal, DPO, CISO, Data Science, Customer Ops) | Approves policy, reviews the risk register monthly, signs off go-live gates and model changes |
| **Independent AI Ethics & Compliance Analyst** | Pre-deployment and periodic assessment; reports to the Committee, independent of the build team. UNESCO para. 58 encourages an independent AI Ethics Officer or similar mechanism |
| **Model owners** (Head of Data Science) | Data, model quality, fairness testing, documentation |
| **Data Protection Officer** | Privacy impact assessment, data subject rights, retention |
| **CISO** | Security of platform, biometric store and models |
| **Head of Customer Operations / Fraud Operations Manager** | Human review quality, appeals, customer remedy |
| **Head of Legal & Compliance** | Legal applicability register per market; regulator engagement |

**Policies required before launch (GOVERN 1.x):** AI risk policy and risk tolerance (GOVERN 1.3, MAP 1.5); an AI system inventory including third-party components (GOVERN 1.6, GOVERN 6.1); monitoring and review schedule (GOVERN 1.5); channels for feedback from affected people (GOVERN 5.1).

## 3. MAP: context and risk identification

MAP 1.1 asks that intended purposes, deployment settings and context-specific laws and norms be understood and documented. Activities:

1. **System and context description** (`01_scope_and_assumptions.md`): purposes, modules, users, affected groups, jurisdictions.
2. **Impact mapping** for each module (MAP 5.1: likelihood and magnitude of impacts), including affected groups and the harms in Task 1 (ER1-ER6).
3. **Component and third-party mapping** (MAP 4.1): identity databases, cloud services, pre-trained components.
4. **Human oversight design** (MAP 3.5): where reviewers sit, what they can override, what training they need (MAP 3.4).
5. **Risk tolerance** (MAP 1.5): see the scoring method in section 7.

Output: the risk register. Risks were identified by combining the Task 1 ethical risks with governance, security, third-party, drift, legal and capability risks.

## 4. MEASURE: risk measurement

MEASURE 1.1 requires metrics to be selected "starting with the most significant AI risks". Proposed measures:

| Risk area | Measure | Reference |
|---|---|---|
| Fairness | Selection rate, false positive rate and true positive rate by group; gaps and ratios (method and demonstration in Task 4) | MEASURE 2.11 |
| Validity and reliability | Precision, recall and error rates; documented limits on generalisation beyond the test conditions | MEASURE 2.5 |
| Explainability | Share of adverse decisions with a valid reason code; reviewer comprehension spot-checks | MEASURE 2.9 |
| Privacy | DPIA completed; records of data minimisation and retention checks | MEASURE 2.10 |
| Security and resilience | Penetration and spoofing test results | MEASURE 2.7 |
| Oversight quality | Override rate, time per review, appeal outcomes | MAP 3.5, MANAGE 4.1 |
| Customer feedback | Complaint and appeal volumes and outcomes | MEASURE 3.3 |

**Thresholds (proposed):** acceptable group gaps are set by the Committee before testing and recorded; Task 4 shows how to calculate the measures and discusses candidate thresholds. Independent assessors who did not build the model should review the results (cf. MEASURE 1.3).

## 5. MANAGE: mitigation, monitoring and decisions

- **Go/no-go (MANAGE 1.1):** a documented decision on whether the system meets its objectives and whether deployment should proceed.
- **Prioritised treatment (MANAGE 1.2-1.3):** the register ranks risks by score; Critical risks must have a planned response before launch.
- **Residual risk (MANAGE 1.4):** negative residual risks are documented and accepted by the right level (Medium: Committee; High: Board).
- **Switch-off (MANAGE 2.4):** an owner and procedure exist to "supersede, disengage, or deactivate" the system if its outcomes are inconsistent with intended use.
- **Post-deployment monitoring (MANAGE 4.1):** plan covers user input, appeals and override, incident response and recovery.

**Monitoring cadence (proposed):**

| Frequency | Activity | Owner |
|---|---|---|
| Daily | Alert volumes, false-positive queue, blocked-account backlog | Fraud Operations Manager |
| Weekly | Override rates, appeal turnaround, drift indicators | Head of Customer Ops; Head of Data Science |
| Monthly | Group-level fairness metrics; risk register review | AI Governance Committee |
| Quarterly | Independent assessment; third-party review; training refresh | Independent Analyst; Vendor Risk Manager |
| On every model change | Full fairness, privacy and security re-test before release | Head of Data Science; DPO; CISO |

## 6. Human oversight and incident escalation

**Oversight levels (proposed).**

| Decision type | Human role |
|---|---|
| Low-risk, easily reversible (e.g. routine transaction cleared) | Automated; sampled for quality |
| Adverse and reversible (e.g. step-up verification, temporary limit) | Reviewer can see the reason code and override |
| Severe or hard to reverse (e.g. account closure, sustained freeze, rejection of onboarding) | Documented human determination required before action (consistent with UNESCO para. 26) |

**Incident escalation (proposed).** An AI incident is any event where the system causes or is likely to cause harm, a breach, a material fairness failure, or an outage of decisions.

| Severity | Examples | Notify | Target |
|---|---|---|---|
| S1 Critical | Data breach of biometrics; systematic wrongful freezes; evidence of discriminatory outcomes at scale | CRO, CEO, DPO, Legal immediately; consider suspension (MANAGE 2.4) | Containment started within hours |
| S2 High | Fairness metric breaches threshold; significant model failure | CRO, Committee chair, model owner | Same business day |
| S3 Medium | Localised errors, rising complaints | Model owner, Customer Ops | Within days |
| S4 Low | Minor defects | Logged and tracked | Next review cycle |

Incidents and errors are communicated to relevant parties, "including affected communities" (MANAGE 4.3), and tracked to recovery. Under the Nigeria Data Protection Act a breach likely to risk individuals' rights must be notified to the regulator within 72 hours (see Task 3), so the S1 runbook starts that clock.

## 7. Risk scoring method

- **Likelihood** (1 rare to 5 almost certain) × **Impact** (1 minimal to 5 severe) = score out of 25.
- **Bands:** Low 1-4; Medium 5-9; High 10-14; Critical 15-25.
- **Inherent** score is before proposed controls; **residual** score is after proposed controls are in place and working. All controls are *proposed*, because the assessment is pre-deployment.
- Likelihood and impact values are analytical judgements, to be revisited with real data.

## 8. Register summary (12 risks)

| Band | Inherent | Residual |
|---|---|---|
| Critical | 7 | 0 |
| High | 3 | 0 |
| Medium | 2 | 11 |
| Low | 0 | 1 |

The fall from 7 Critical risks to none is a *planned* result. It holds only if every proposed control is built and works as intended, and none exists yet, so the residual column is a target to verify at each launch gate, not a measured outcome. Residual scores remain **Medium** for most risks, which means continued monitoring and not "solved". RR05 (automation bias) and RR06 (false-positive harm) are the highest residual risks (score 9) because they depend on human behaviour and customer circumstances that controls reduce but cannot remove.

## 9. Launch gates (input to the Task 5 recommendation)

1. Group-level fairness testing completed and within thresholds the Committee set beforehand (Task 4).
2. DPIA completed and approved by the DPO.
3. Reason codes, appeals route and human determination rules operating in a pilot.
4. Penetration and anti-spoofing tests passed; incident runbook rehearsed.
5. Legal applicability review signed off for each launch market.
6. Reviewer training completed and competence checked.
7. Switch-off procedure tested.

## Sources

NIST AI 100-1: trustworthiness characteristics (PDF p.4); GOVERN 1.1-1.5 and 2.1, 2.3 (PDF pp.27-28); GOVERN 5.1, 6.1 (PDF p.29); MAP 1.1, 1.5 (PDF p.31); MAP 3.5, 4.1, 5.1 (PDF p.32); MEASURE 1.1-1.3, 2.5-2.11, 3.1, 3.3, 4.1 (PDF pp.34-36); MANAGE 1.1-1.4, 2.4, 4.1, 4.3 (PDF pp.37-38). UNESCO Recommendation paras 26, 58.
