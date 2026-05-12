# Healthcare Fraud in America: FCA Settlement Analysis

**Dawn Krysa, PA-C, MSHIIM, CHDA**  
May 2026 | Portfolio Project | [Full Interactive Report →](https://darbydawn.github.io/healthcare-fraud-fca-analysis/FCA_Portfolio_Report.html)

---

## Project Overview

A four-phase forensic data investigation into Medicare and Medicaid fraud using publicly available federal datasets — CMS T-MSIS Medicaid claims, CMS Medicare Provider Utilization data, DOJ False Claims Act enforcement records, and the HHS OIG List of Excluded Individuals and Entities (LEIE).

This project applies statistical outlier detection and clinical judgment to surface fraud patterns that automated systems miss. The combination of 14 years of clinical experience as a PA-C with intermediate SQL and Python skills produces a methodology that is both statistically valid and clinically literate — flagging patterns that are not just numerical outliers but medically impossible.

**4 OIG referrals submitted. 71% defendant confirmation rate via DOJ cross-reference.**

---

## Key Findings at a Glance

| Finding | Detail |
|---|---|
| Phase 1 flagged records | 1,109 across 194 providers |
| Estimated Phase 1 exposure | ~$123M (sample only) |
| Arizona cluster — 7 providers | $452M+ combined Medicare payments |
| DOJ confirmation rate | 71% (5 of 7 flagged providers subsequently charged) |
| OIG referrals submitted | 4 (2 Phase 1, 2 Phase 2/3) |
| LEIE records analyzed | 83,001 current exclusions |
| Mississippi abuse rate | 26.59 per 100K — 2.6x the #2 state |

---

## Project Phases

| Phase | Topic | Tools | Status |
|---|---|---|---|
| 1 | Medicaid Provider Spending Anomaly Detection | Python, pandas, scikit-learn | Complete |
| 2 | Medicare Provider Utilization Analysis | Python, SQLite | Complete |
| 3 | DOJ FCA Settlement Cross-Reference | Python, pandas | Complete |
| 4 | OIG LEIE National Exclusion Analysis | Python, pandas, Matplotlib | Complete |

---

## Phase 1 — Medicaid T-MSIS Anomaly Detection

**Data:** CMS T-MSIS Medicaid Provider Spending by HCPCS (released February 2026). Largest Medicaid claims dataset ever made publicly available. Coverage: January 2018 – December 2024, all 50 states.

**Method:** MinMaxScaler outlier detection on billing volume relative to real-world time and staffing constraints. Clinical judgment applied to distinguish expensive-but-plausible from mathematically impossible billing patterns.

**Results:**
- 1,109 flagged billing records across 194 unique providers
- 2 providers identified with mathematically impossible LPN billing volumes
- Combined estimated Medicaid exposure: ~$123M (sample only)
- Both submitted to HHS OIG as formal referrals

| Provider | NPI | Location | Anomaly |
|---|---|---|---|
| Quality One Care Home Health Inc. | 1528351285 | Silver Spring, MD | 7,201 billed LPN hours in a 672-hour month |
| Greater New York Home Care LLC | 1225205354 | Brooklyn, NY | 548 hours of LPN care per patient in a 31-day period |

**Files:** `medicaid_fraud.py` · `phase1_flagged_records.csv` · `phase1_provider_summary.csv`

---

## Phase 2 — Medicare Provider Utilization Analysis

**Data:** CMS Medicare Provider Utilization and Payment Data, 2023.

**Method:** SQLite queries aggregating Medicare paid amounts, patient counts, and spend-per-patient by NPI and specialty. Flagged providers billing amniotic allograft injections at 130–270x the national NP average spend per patient.

**Result:** A 7-provider cluster in Arizona with combined Medicare payments exceeding $452M. National NP average spend per patient is approximately $3,500. Cluster average: $722,000 per patient.

---

## Phase 3 — DOJ FCA Cross-Reference

**Data:** DOJ False Claims Act press releases and settlement database.

**Method:** NPI and provider name matching against DOJ enforcement records. Used to validate Phase 2 outlier methodology independently of enforcement outcomes.

**Result:** 5 of 7 independently flagged Arizona cluster providers appeared in subsequent 2024–2025 DOJ enforcement actions — a 71% confirmation rate achieved without prior knowledge of the investigation. The remaining 2 providers were submitted as OIG referrals in May 2026.

| Provider | NPI | Medicare Paid | Per Patient | Status |
|---|---|---|---|---|
| Ira Denny NP | 1255987475 | $135.8M | $653,093 | Charged — 2025 DOJ Takedown |
| Jorge Kinds NP | 1174182760 | $126.3M | $454,452 | Charged — 2025 DOJ Takedown |
| Carlos Ching NP | 1417543117 | $64.1M | $956,797 | Charged — 2024 DOJ Action |
| Bethany Jameson NP | 1225551484 | $50.2M | $784,040 | Charged — 2024 DOJ Action |
| Gina Palacios NP | 1275217952 | $27.0M | $730,791 | Charged — 2025 DOJ Takedown |
| Elisabeth Balken NP | 1992489728 | $23.3M | $776,182 | OIG Referred May 2026 |
| Arlene Bautista NP | 1285292334 | $16.9M | $702,096 | OIG Referred May 2026 |

---

## Phase 4 — OIG LEIE National Exclusion Analysis

**Data:** HHS OIG List of Excluded Individuals/Entities (LEIE), full current database — 83,001 records.

**Method:** Per-capita rate calculation by state using 2024 Census population estimates. Facility type classification using LEIE specialty codes. State ranking by patient abuse exclusions per 100,000 residents.

**The Mississippi Finding:**

Mississippi has **26.59 patient abuse exclusions per 100,000 residents** — the highest in the nation by a substantial margin. The #2 states (Louisiana and Delaware) are tied at 10.20. Mississippi accounts for **9.58% of all national patient abuse exclusions** while representing **0.87% of the US population.**

The abuse is concentrated in ICF/IID facilities — intermediate care facilities serving nonverbal and cognitively disabled adults. **83% of Mississippi ICF exclusions are specifically for patient abuse**, not billing fraud. These are patients who cannot call a hotline, cannot tell a family member, and are entirely dependent on the people paid to care for them.

During the COVID enforcement gap, national exclusions dropped 31% (2021, lowest in 15 years) before spiking 63% in 2022 as backlogged cases cleared. The abuse did not stop. The enforcement did.

**Additional findings:**
- Nurses and aides account for **41.6% of all LEIE exclusions** and **72.2% of all permissive felony exclusions** nationally
- The dominant exclusion type is **1128b4 (permissive felony, any crime)** at 39.9% of all exclusions
- 2024 saw the highest exclusion volume in recent years (3,134) driven by DOJ healthcare fraud takedown operations

---

## Tools and Data Sources

| Tool | Purpose |
|---|---|
| Python (pandas, scikit-learn) | Data processing, outlier detection, risk scoring |
| SQLite | Phase 2 Medicare utilization queries |
| Matplotlib | All data visualizations |
| CMS T-MSIS | Medicaid claims data (Phase 1) |
| CMS Medicare Provider Utilization | Medicare provider data (Phase 2) |
| DOJ FCA Database | Settlement cross-reference (Phase 3) |
| HHS OIG LEIE | National exclusion analysis (Phase 4) |

---

## About This Project

All analysis uses publicly available federal data. No patient-level data was accessed. All findings are based on aggregated, de-identified provider billing records and publicly filed enforcement actions.

The author brings 14 years of clinical experience as a PA-C combined with a Master of Science in Health Informatics and Information Management (MSHIIM) and Certified Health Data Analyst (CHDA) credential. Clinical judgment applied alongside statistical methods distinguishes legitimately expensive billing from clinically impossible patterns — a capability that purely algorithmic approaches miss.

**[View Full Interactive Report](./FCA_Portfolio_Report.html)**

---

*Dawn Krysa, PA-C, MSHIIM, CHDA · Darby, Montana · darbydawn7683@gmail.com*
