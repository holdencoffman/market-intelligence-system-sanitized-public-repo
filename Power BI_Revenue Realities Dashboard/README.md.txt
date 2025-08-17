# Revenue Realities Dashboard (Power BI)
*A data-driven exploration of post-award revenue outcomes in national interior trade service bids*

---

## 📊 Overview

This Power BI dashboard analyzes the divergence between **initial bid award designations** (Loss, Primary, Secondary) and the **actual revenue realization** at the site level across ~155,000 sites and 32 national RFPs.

Despite clear win/loss labels during the bid process, the data revealed a striking insight:

> **Over 84% of awarded sites generated zero revenue**, including over 60% of those initially marked as "won".

This project surfaces those patterns visually and analytically, helping leadership understand the **true nature of revenue pull-through** in national interior trade facility service contracts.

---

## 🧠 Business Context

In B2B service contracting, clients often award national bids with award designations like:
- 🟦 **Primary** – You are the designated vendor
- 🟧 **Secondary** – You are the backup vendor
- ⬛ **Loss** – You were not awarded the work

However, these designations don't always align with reality — clients may continue using incumbent providers, or call other vendors for work throughout the season. This supports the 

This dashboard helps answer:
- How often do Primary awards actually convert into revenue?
- How much revenue is generated at Secondary vs. Loss-designated sites?
- What is the true post-award ROI of our bid strategy?

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
Stacked column chart showing revenue pull-through by designation — **even many Primary awards failed to materialize into revenue**, while a small number of Secondary and Loss sites surprisingly did.

### 3. **Distribution of Revenue Realization**
Donut visual showing revenue-generating sites by award category. Here we see that **73% of revenue-generating sites were Primary**, but **26% came from Loss sites**, defying expectations.

---

## 🔎 Strategic Takeaways

- 🎯 **Designation ≠ Delivery**: Primary awards only generated revenue at **1 in 3 sites**.
- ⚠️ **Zero-Revenue Risk**: Over **84%** of all awarded sites never pulled through to work.
- 💡 **Loss Sites ≠ Lost Revenue**: A notable share of actual revenue came from sites we were not awarded.

---

## 📁 Repository Contents

