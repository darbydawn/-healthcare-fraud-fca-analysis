# Healthcare Fraud in America: FCA Settlement Analysis

**Dawn Krysa, PA-C, MSHIIM, CHDA**  
April 2026 | Portfolio Project

---

## Project Overview

A multi-phase fraud detection project using Python, SQL, and Tableau against publicly available federal datasets — T-MSIS Medicaid claims, CMS Medicare utilization, DOJ False Claims Act settlements, and the OIG LEIE exclusion list.

This project applies statistical anomaly detection and clinical judgment to surface fraud patterns that automated systems miss. Phase 1 alone identified two providers with mathematically impossible billing patterns totaling an estimated $123 million in Medicaid payments — neither named in the most recent DOJ national healthcare fraud takedown.

---

## Project Phases

| Phase | Topic | Tools | Status |
|---|---|---|---|
| 1 | Medicaid Provider Spending Anomaly Detection | Python, pandas, scikit-learn | ✅ Complete |
| 2 | Medicare Provider Utilization Analysis | Python, SQL | 🔄 In Progress |
| 3 | DOJ FCA Settlement Cross-Reference | SQL | 🔄 Planned |
| 4 | OIG Exclusion List Matching | SQL | 🔄 Planned |
| 5 | Tableau Dashboard | Tableau | 🔄 Planned |

---

## Phase 1 — Medicaid Provider Spending Anomaly Detection

**Data Source:** CMS T-MSIS Medicaid Provider Spending by HCPCS, released February 2026 by HHS/DOGE. Largest Medicaid claims dataset ever made publicly available. Coverage: January 2018 – December 2024, all 50 states and territories.

**Key Results:**
- 1,109 flagged billing records across 194 unique providers
- 2 providers identified with mathematically impossible LPN billing volumes
- Combined estimated Medicaid exposure: ~$123 million (sample only)
- Both cases submitted to HHS OIG for investigation

**Files:**
- `phase1/medicaid_fraud.py` — Full Python script
- `phase1/phase1_flagged_records.csv` — All 1,109 flagged records
- `phase1/phase1_provider_summary.csv` — 194 providers with composite risk scores
- `phase1/README.md` — Full methodology documentation

---

## About This Project

This analysis was produced as part of a healthcare analytics portfolio using publicly available federal data. All work was performed using Python for data processing and statistical outlier detection. No patient-level data was accessed — all analysis is based on aggregated, de-identified provider billing data.

The author brings 14 years of clinical experience as a PA-C combined with a Master of Science in Health Informatics and Information Management (MSHIIM) and Certified Health Data Analyst (CHDA) credential. Clinical judgment was applied alongside statistical methods to distinguish legitimately expensive billing from clinically impossible patterns.

---

## Tools & Data Sources

| Tool | Purpose |
|---|---|
| Python (pandas, scikit-learn) | Data processing, outlier detection, risk scoring |
| SQL | Data querying and cross-referencing (Phases 2–4) |
| Tableau | Dashboard visualization (Phase 5) |
| T-MSIS / HHS Open Data | Medicaid claims (Phase 1) |
| CMS Medicare Utilization | Medicare provider data (Phase 2) |
| DOJ FCA Settlements | Settlement cross-reference (Phase 3) |
| OIG LEIE | Exclusion list matching (Phase 4) |
