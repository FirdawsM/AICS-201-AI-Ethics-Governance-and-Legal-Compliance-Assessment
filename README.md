# SecureFinance Africa: AI Ethics, Governance & Legal Compliance Assessment

ICDFA | AICS-201 | Assignment 01. Independent AI Ethics, Governance and Compliance Analyst assessment of a fintech AI platform.

> All data in this repository is **synthetic or fictional**. No real customer records, identifiers or confidential information are used.

## Repository layout

| Path | Contents |
|---|---|
| `docs/01_scope_and_assumptions.md` | System description, scope, jurisdiction and data-subject assumptions |
| `docs/02_source_log.md` | Every source used, its legal status (binding / non-binding) and where it is cited |
| `risk_register/risk_register.csv` | NIST AI RMF aligned AI risk register (Task 2) |
| `data/` | Synthetic dataset and data dictionary (Task 4) |
| `analysis/` | Reproducible fairness and explainability code (Task 4) |
| `evidence/` | Charts, tables and code outputs produced by the analysis |
| `evidence/screenshots/` | Screenshots of a clean-environment run (venv, install, data generation, fairness analysis). Also shown in Appendix E of the report |
| `report/` | Final assessment report, PDF (Task 5) |

## Reproducing the analysis

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python analysis/generate_data.py      # writes data/synthetic_customers.csv (seeded)
python analysis/fairness_analysis.py  # writes tables, charts and summary to evidence/
```

## Where each task lives

| Task | Location |
|---|---|
| 1. Ethical risk identification | `docs/03_task1_ethical_risks.md` |
| 2. AI governance and risk register | `docs/04_task2_governance.md`, `risk_register/risk_register.csv` |
| 3. Legal and regulatory compliance | `docs/05_task3_legal_compliance.md` |
| 4. Fairness and explainability | `docs/06_task4_fairness_explainability.md`, `analysis/`, `data/`, `evidence/` |
| 5. Final governance assessment report | `report/SecureFinance_AI_Assessment_Report.pdf` |

## References

1. Federal Republic of Nigeria. *Nigeria Data Protection Act 2023.* Nigeria Data Protection Commission, https://ndpc.gov.ng/ (text read from a certified Bill copy; the gazetted copy was not retrieved).
2. Nigeria Data Protection Commission. *NDPA General Application and Implementation Directive (GAID) 2025.* https://ndpc.gov.ng/
3. European Union. *Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act).* Official Journal L, 12 July 2024. https://ai-act-service-desk.ec.europa.eu/en/ai-act-explorer
4. European Union. *Regulation (EU) 2026/1744 (Digital Omnibus on AI),* in force 27 July 2026. European Commission announcement: https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force
5. UNESCO. *Recommendation on the Ethics of Artificial Intelligence,* adopted 23 November 2021. https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence
6. OECD. *Recommendation of the Council on Artificial Intelligence,* OECD/LEGAL/0449, as amended 3 May 2024. https://legalinstruments.oecd.org/public/doc/648/648.en.pdf
7. National Institute of Standards and Technology. *Artificial Intelligence Risk Management Framework (AI RMF 1.0),* NIST AI 100-1, January 2023. https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf
8. Schwartz, R., et al. *Towards a Standard for Identifying and Managing Bias in Artificial Intelligence,* NIST Special Publication 1270, March 2022.

The full list of sources, their legal status and where each is cited is in `docs/02_source_log.md`.
