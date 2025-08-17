# Revenue Realities: Rethinking Win/Loss Classifications for the Interior FM Industry
*A Power BI analysis uncovering the gap between awarded designations and actual revenue outcomes.*

---

## 📊 Background and Overview

The internal reporting we initially leveraged relied on to model customer price sensitivity relied on binary win/loss designations as indicators of customer price acceptance. But after months of anecdotal observations suggesting a divergence between award status and actual revenue realization, I designed a dashboard to investigate the pattern at scale and to test my hypothesis that in order to effectively model customer price sensitivity we would need a different kind of dataset to model off of. 

This Power BI dashboard analyzes the divergence between **initial bid award designations** (Loss, Win [broken into Primary or Secondary designation]) and the **actual revenue realization** at the site level over the 12 months following the award, across ~155,000 sites and 32 national RFPs spanning back to 2021.

Despite clear win/loss labels during the bid process, the data revealed some striking insights:

> **Over 66% of awarded sites generated zero revenue, and over 25% of actual realized revenue came from sites dismissed as a loss during the bid process but that went on to receive work orders.**

This project surfaces those patterns visually and analytically, helping leadership understand the **true nature of revenue pull-through** in national interior trade facility service contracts.

---

## 🧠 Business Context

In B2B service contracting, clients often award national bids with award designations like:
- 🟦 **Primary** – You are the designated vendor
- 🟧 **Secondary** – You are the backup vendor
- ⬛ **Loss** – You were not awarded the work

However, these designations don't always align with reality — clients may continue using incumbent providers, or call other vendors for work throughout the season. Clients may also deny the award at the time of the RFP, and then call mid-season asking for coverage.

This dashboard helps answer:
- How often do Primary/Secondary awards actually convert into revenue?
- How often do Losses nonetheless convert into revenue?
- Is our binary win/loss target from the prior bids a reliable indicator of customer purchasing behavior?

---

## 🛠 Tools & Technologies

| Tool         | Purpose                                  |
|--------------|-------------------------------------------|
| **SQL**      | Data extraction, transformation, and logic (Snowflake) |
| **DAX**      | Custom measures for pull-through, zero-revenue logic |
| **Power BI** | Interactive data modeling and dashboarding |

---

## 🔍 Key Metrics Calculated

- **Sites Marked Won**: Count of sites marked Primary or Secondary
- **Sites Receiving Revenue**: Sites with ≥1 invoice post-award
- **Zero-Revenue Sites**: Sites marked won but with $0 realized
- **Total Pull-Through %**: % of won sites that generated revenue
- **Zero-Revenue %**: % of won sites that yielded no revenue
- **Win Pull-Through %**: % of revenue-active sites vs. all Primary sites

---

## 📈 Dashboard Highlights

### 1. **Overall Award Designation Breakdown**
Donut visual showing the share of all sites marked as Loss, Primary, or Secondary — **only ~35% were marked as “won”**, and just a fraction of those realized any revenue.

### 2. **Revenue Realities by Award Designation**
Stacked column chart showing revenue pull-through by designation — **even many Primary awards failed to materialize into revenue**, while a small number of Loss sites surprisingly did.

### 3. **Distribution of Revenue Realization**
Donut visual showing revenue-generating sites by award category. Here we see that **73% of revenue-generating sites were Primary**, but **26% came from Loss sites**, defying expectations.

---

## 🔎 Strategic Takeaways

- 🎯 **Designation ≠ Delivery**: Primary awards only generated revenue at **1 in 3 sites**.
- ⚠️ **Zero-Revenue Risk**: Over **66%** of all awarded sites never pulled through to work.
- 💡 **Loss Sites ≠ Lost Revenue**: A notable share of actual revenue came from sites that were not formally awarded in the RFP Process.

---

## 📁 Repository Contents

- 📸 Screenshots of anonymized dashboard views (Summary Page, Pull-Through Analysis)
- 🧾 Cleaned SQL query
- 🔣 DAX measures used for calculating pull-through and zero-revenue metrics