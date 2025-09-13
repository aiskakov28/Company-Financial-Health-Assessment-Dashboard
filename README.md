# 📊 QuickFin — Company Financial Health Dashboard

Exec-ready KPIs, anomaly detection, and cash-flow trends in one place.  
Streamlines financial health analysis for public companies with a modern **Dash + dbt + AWS** stack.

---

## ⚠️ Disclaimer
This project is for **educational purposes only**.  
It is **not** intended for commercial use or financial advice. Do **not** rely on this tool for investment decisions.

---

## 💹 Overview
QuickFin is an interactive dashboard that:
- Fetches **real-time financial data** from Finviz
- Runs **dbt transformations** into curated marts
- Provides **visualizations** (radar, bar, time-series)
- Supports **scheduled refresh** via AWS Lambda + CloudWatch

---

## 🎯 Features
- Real-time company analysis by ticker symbol  
- Radar + bar charts for category health  
- Detailed metric breakdowns on click  
- Outlier detection and trend insights  
- Auto-refresh pipelines with dbt + Lambda  

---

## 🛠 Tech Stack
- **Python**, **Pandas**, **NumPy**
- **Dash + Plotly** for UI & charts
- **BeautifulSoup** for scraping
- **PostgreSQL** for storage
- **dbt** for curated marts
- **AWS Lambda + CloudWatch** for refresh
- **Playwright + Pytest** for testing
- **Terraform** for infra as code

---

## 📂 Project Structure
```text
app/              Dash web app
collectors/       Data ingestion (scrapers, loaders)
core/             Domain logic (metrics, scoring)
dbt_quickfin/     dbt project (staging + marts + seeds)
infra/            CI + Terraform + GitHub Actions
lambdas/          AWS Lambda functions
scripts/          Local utilities (refresh, seed data)
tests/            Unit + E2E tests
