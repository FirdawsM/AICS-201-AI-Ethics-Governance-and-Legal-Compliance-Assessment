# 05. Task 3: Legal and Regulatory Compliance

*Section 6 states exactly what was and was not checked. Binding law is separated from non-binding principles throughout. This is analysis, not legal advice.*

## 1. Binding law and non-binding principles

| Instrument | Status | When it affects SecureFinance Africa |
|---|---|---|
| **Nigeria Data Protection Act 2023 (NDPA)** | **Binding (Nigeria)** | From Phase 1. Under s.2(2) it applies where the controller is operating in Nigeria, where processing occurs in Nigeria, or where a non-Nigerian controller processes data of people in Nigeria. Assumption A1 (Nigerian controller, Nigerian customers) meets s.2(2)(a) and (b). |
| **NDPA General Application and Implementation Directive 2025 (GAID)** | **Binding regulatory directive, subordinate to the Act** | From Phase 1. Issued by the NDPC under NDPA ss.1(a), 6(c), 61 and 62; if it conflicts with the Act, the Act prevails (GAID Art. 3(2)). It adds the detailed duties that matter most here (DPIA filing, AI and disparate-outcome assessment, consent for solely automated decisions). Its exact legal force relative to the Act is a question for Nigerian counsel; it is treated as binding here because the Commission applies it in audits. |
| **EU AI Act, Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744** | **Binding (EU)** | Not in Phase 1. In Phase 2 only if Art. 2(1) is triggered: SecureFinance places the system on the EU market or puts it into service there (Art. 2(1)(a)), or, as a provider or deployer in a third country, its output is used in the Union (Art. 2(1)(c)). No EU establishment is needed. |
| **UNESCO Recommendation on the Ethics of AI (2021)** | Non-binding | Never directly. Member States are asked to apply it "on a voluntary basis" (para. 2). Used as an ethical benchmark. |
| **OECD AI Principles (OECD/LEGAL/0449, revised 3 May 2024)** | Non-binding | Never directly. A Council Recommendation, not enforceable. Used as an ethical benchmark. |

GDPR and Nigerian financial-sector rules are acknowledged as likely to apply in Phase 2 and Phase 1 respectively, but are outside the approved resource set (see `01_scope_and_assumptions.md`).

## 2. NDPA and GAID: what applies, by module

| Provision | Requirement | Effect on the platform |
|---|---|---|
| NDPA s.24; GAID Arts. 41(5), 41(8), 42(5), 52 | Fair, accurate processing and a duty of care (s.24(3)). The GAID prohibits discrimination in data processing, calls for safeguards against algorithms that produce prejudiced outcomes, and treats an outcome that departs adversely from what was expected as a "disparate outcome" for which liability can follow. It describes a task that could cause one as unlawful. | Fairness testing (Task 4) is a Nigerian compliance activity, not only an ethical one. A DPIA must include disparate-impact analysis (Art. 42(5)(e)). |
| s.25–26; GAID Art. 17(7)(c) | Lawful basis. Legitimate interest fails if it overrides data subjects' rights or they would not reasonably expect it (s.25(2)). Consent is not free if a service is made conditional on unnecessary consent (s.26(2)); refusing consent must not harm the person. | Behavioural and device data for M2/M3 cannot be bundled into onboarding consent. |
| s.27(1)(g); GAID Art. 27 | Tell people about automated decision-making and profiling, its consequences, and their right to object and challenge. | Privacy notice must describe M1–M3 in plain language. |
| **s.28; GAID Art. 28** | DPIA before high-risk processing; consult the Commission if high residual risk (s.28(2)). GAID Art. 28(3) makes the DPIA **mandatory and filed with the Commission** for, among other cases: profiling or scoring, automated decisions with significant effects, sensitive data, and financial services processed through digital devices. It must be vetted and signed by a certified DPO and completed before processing starts (Art. 28(4), (9), (12)). Failure can lead to restrictions on platforms (Art. 28(6)). | **All three modules trigger a filed DPIA**; the financial-services limb alone covers the platform. This is a Phase 1 launch gate. For AI, Art. 43(4) adds assessment of disparate outcomes and data-subject vulnerability, controlled testing, re-testing, and continuous monitoring. |
| s.30, s.65; GAID Art. 18(1)(b) | Biometric data is sensitive personal data. The s.65 definition covers data that "allow or confirm" unique identification, so one-to-one verification is inside it. The s.30(1) grounds include no contract or legitimate-interest basis, and GAID Art. 18(1)(b) requires consent for sensitive data. | M1 needs consent under s.30(1)(a); no other listed ground obviously fits. Note the contrast with the EU, where one-to-one verification is likely outside Annex III but is still sensitive data here. |
| **s.37, s.65; GAID Arts. 18(1)(f), 43(2)(a)** | A right not to be subject to a decision based solely on automated processing with legal or similar significant effects. Exceptions: contract necessity, written law, or consent (s.37(2)). Safeguards: human intervention, express a view, contest (s.37(3)). The Act defines automated decision-making as "without any human involvement" (s.65). GAID Art. 18(1)(f) requires consent before such a decision. | Real staff review of M1–M3 keeps decisions outside s.37. On a literal reading of s.65 even a nominal review might do so, but a regulator is likely to ask whether the involvement is genuine (interpretation, to confirm with counsel). Rubber-stamping (ER5) therefore risks both the law and the design intent. |
| s.39–40; GAID Arts. 7(p)–(q), 33 | Security measures. Notify the Commission within 72 hours of a breach likely to risk individuals' rights; tell data subjects immediately where risk is high. GAID Art. 33(2) treats exposure to fraud or identity theft as high risk. | A breach of the biometric store (RR08) is a high-risk breach on that definition. |
| s.41–43; GAID Art. 45 | Cross-border transfers need adequacy or a listed basis, and the basis must be recorded (s.41(2)). | Hosting or model training outside Nigeria; Phase 2 EU data flows. |
| s.32, s.44; GAID Arts. 7–11 | Controllers "of major importance" must appoint a DPO, register, and (at the Ultra-High and Extra-High levels) file an annual compliance audit return by 31 March through a licensed compliance organisation. Art. 8(3) lists the factors: sensitivity, financial assets entrusted, reliance on cloud, cross-border flows, automation, number of data subjects. | SecureFinance very likely qualifies on those factors. The tier thresholds are in GAID Schedule 7, which has not been read; secondary sources disagree on the numbers, so none are stated. |
| GAID Arts. 21(2), 49(3) | Absent a legal retention period, storage lapses six months after the purpose is met; data from a contract that never happened is destroyed within six months unless needed for legal claims. | Retention schedule for biometrics and for rejected applicants (ER3). |
| s.48(4) | Penalty up to the greater of ₦10m and 2% of the preceding year's annual gross revenue (major-importance controllers). Civil damages (s.51). | Exposure if the above fail. |

## 3. EU AI Act: Phase 2 classification

Classification depends on what each module does, so the conclusion is conditional.

| Module | Likely classification | Reason and condition |
|---|---|---|
| **M1 identity verification** | Probably **not** Annex III high-risk | Annex III point 1(a) excludes biometric verification whose sole purpose is to confirm a person is who they claim to be. Becomes a different question if M1 performs one-to-many identification against a database. |
| **M2 fraud detection** | Probably **not** high-risk under point 5(b) | Point 5(b) excludes AI used to detect financial fraud. |
| **M3 risk assessment** | **High-risk** if it evaluates creditworthiness or sets a credit score of natural persons | Annex III point 5(b). M3 sets limits, eligibility and pricing, which resembles creditworthiness assessment. If it only scored fraud or AML risk, the exclusion would apply. The scope document must say which. |

**Timing.** Regulation (EU) 2026/1744 was published on 24 July 2026 and entered into force on 27 July 2026. It moved the Chapter III, Sections 1 to 3 obligations for Annex III systems to **2 December 2027** (Art. 113(3)(c)(i), as amended). Two points follow:

- Under Art. 111(2) as amended, a high-risk system already on the market before that date becomes subject to the rules only if its design is significantly changed afterwards. Do not rely on this: "significant change" is not defined in the sources read, and the fairness remediation recommended in Task 4 (retraining on outcome labels, removing proxy features) is itself a design change. Treat 2 December 2027 as the design target.
- The Art. 5 prohibitions already apply. Art. 5(1)(c) bans scoring that leads to detrimental treatment in social contexts unrelated to where the data came from, or treatment that is unjustified or disproportionate to the behaviour, and it applies to private firms. Commission guidance, as summarised by law-firm sources (secondary), says credit scoring on relevant financial data is not itself caught. The risk for SecureFinance is reusing M2/M3 behavioural scores to penalise customers in unrelated contexts. UNESCO para. 26 states the same expectation as an ethical norm.

**If M3 is high-risk**, under A1 SecureFinance is both provider and deployer, so both sets of duties apply:

- Provider, Arts. 9 to 16:
  - Art. 9: a risk management system maintained across the lifecycle, with testing against metrics and probabilistic thresholds defined in advance. This is the legal hook for the pass/fail fairness threshold recommended in Task 4.
  - Art. 10: data governance covering examination and mitigation of bias (Art. 10(2)(f)–(g)) and data that is relevant, sufficiently representative and suited to the setting of use (Art. 10(3)–(4)). Art. 10(5) lets providers process special-category data for bias detection only where strictly necessary and under strict conditions.
  - Arts. 11–13: technical documentation, automatic logging, and instructions that let deployers interpret the output. Art. 15: accuracy, robustness and cybersecurity, including resilience to data poisoning and feedback loops. Art. 16: the provider's general obligations.
- Deployer, Art. 26: human oversight assigned to people with the competence, training and authority to act (Art. 26(2)); automatically generated logs kept for at least six months (Art. 26(6)), which a financial institution can meet through its internal governance arrangements under financial services law; affected people informed that a high-risk system is used. Plus a **fundamental rights impact assessment under Art. 27**, which applies to deployers of point 5(b) systems whether public or private; where a DPIA already covers some of its content, the FRIA complements it. The NDPA/GAID DPIA in section 2 is therefore reusable input.
- Art. 14(4)(b) requires oversight measures that keep the reviewer aware of the tendency to over-rely on the output (automation bias). This is the legal counterpart of ER5 and RR05.

## 4. Soft law as a benchmark

Binding law sets the floor. UNESCO and the OECD Principles are used to judge whether the design goes beyond it, and they create no legal duty.

| Theme | UNESCO | OECD (2024) |
|---|---|---|
| Fairness and non-discrimination | paras 28–29 (para 28 also asks for equity between rural and urban areas, the gap tested in Task 4; para 29 asks for effective remedy) | 1.2: rule of law, human rights and democratic values, including fairness and privacy |
| Privacy | paras 32–34; para 74 (biometric data needs full security) | 1.2 |
| Human oversight | paras 35–36; para 26 (final human determination where effects are irreversible or hard to reverse) | 1.2(b): capacity for human agency and oversight |
| Transparency and explainability | paras 37–40 | 1.3, including information that lets those adversely affected challenge an output (the soft-law counterpart of NDPA s.37(3)) |
| Robustness and security | para 27 (safety and security) | 1.4: robustness, security and safety, including mechanisms to override, repair or decommission a system that causes undue harm |
| Accountability, traceability, risk management | paras 42–43 | 1.5 (the 2024 revision moved traceability and risk management here from 1.4) |

## 5. Assumptions and limitations

- Jurisdiction: Phase 1 Nigeria only; Phase 2 EU only if Art. 2(1) is triggered, as assumed in A1 and the deployment scenario.
- Data subjects: Nigerian residents in Phase 1; people located in the EU in Phase 2.
- System use: the platform recommends and staff review; the s.37 and Art. 14 analysis depends on that review being meaningful.
- SecureFinance is assumed to be a controller of major importance. Tier and fees are not assessed.
- Whether Nigeria has adhered to the OECD Recommendation is not confirmed; it makes no difference to the analysis since it is non-binding either way.

## 6. Limitations and verification

**Checked against the text itself**

- NDPA: the certified Bill copy was read in full. Sections 2, 24–30, 32, 37, 39–44, 48 and 65 are cited as above, and the numbering matches several independent law-firm commentaries.
- GAID 2025: main text (Arts. 1–52) read on the NDPC site. Cited: Arts. 3, 7–11, 17–18, 21, 27–28, 33, 41–43, 45, 49, 52.
- UNESCO Recommendation: full text read. All paragraph numbers cited here and in Task 1 match. Para. 27 is the safety and security paragraph.
- OECD Recommendation (OECD/LEGAL/0449, as amended 3 May 2024): headings and content of Principles 1.3, 1.4 and 1.5 confirmed against the OECD's own background text and a full-text copy; the 2024 move of traceability and risk management from 1.4 to 1.5 is confirmed by the OECD's own summary of the revision. Principle 1.2(b) confirmed earlier.
- EU AI Act, article text read: Art. 9 (lifecycle risk management; testing against pre-defined metrics and thresholds), Art. 10 (paras 2–5 as cited), Art. 26 (paras 2 and 6, and the financial-institution rule on logs), Art. 27 scope, Art. 5(1)(c), Art. 14(4)(b), Art. 111(2) as at 27 July 2026. Annex III points 1(a) and 5(b) and Art. 2(1)(c) were verified in an earlier session.
- EU AI Act, confirmed from summaries only: Arts. 11, 12, 13, 15 and 16 are described at the level of what each article requires, taken from academic and regulator summaries, not from the article text. Paragraph numbers are not cited for them.
- The Omnibus dates are confirmed by several law-firm summaries and a reproduction of the Commission's timeline. Some websites still show 2 August 2026 as the application date; those pages predate the amendment.

**Not verified**

- Annex III points 1(a) and 5(b) and Art. 2(1)(c) were verified in an earlier pass and not re-read; Arts. 11–13, 15 and 16 are cited without paragraph numbers.
- GAID: Schedules 4 to 7 and 10 not read; the effective date is unconfirmed (the file is dated 20 March 2025, secondary sources say September 2025).
- Meaning of "significant change" in Art. 111(2), and the legal force of the GAID: both are points for counsel.
- NDPA: the NDPC's gazetted copy has not been retrieved (the text read is a certified Bill copy hosted by a third party).
