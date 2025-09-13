# 📊 QuickFin — Company Financial Health Dashboard

Exec-ready KPIs, anomaly detection, and cash-flow trends in one place.  
Streamlines financial health analysis for public companies with a modern **Dash + dbt + AWS** stack.

---

## ⚠️ Disclaimer
This project is for **educational purposes only**.  
It is **not** intended for commercial use or financial advice. Do **not** rely on this tool for investment decisions.

---

> **One-stop toolkit** for analyzing, visualizing, and tracking a company’s financial health using Python, dbt, and modern workflows.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![dbt](https://img.shields.io/badge/dbt-Analytics-orange?logo=dbt)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://github.com/aiskakov28/Company-Financial-Health-Assessment-Dashboard/actions/workflows/playwright.yml/badge.svg)

---

### 🚀 Overview

The **Financial Health Assessment Dashboard** automates financial data collection, applies quantitative analysis, and generates actionable insights.  
It’s built for **data scientists, analysts, and finance teams** who need quick and reliable evaluation of company performance.

Key highlights:
- ✅ Automated data collection from Finviz and loaders  
- ✅ Financial metric analysis with curated benchmarks  
- ✅ dbt transformations for clean analytics  
- ✅ Terraform & Lambdas for infrastructure and orchestration  
- ✅ E2E testing with Playwright to ensure reliability  

---

### 🛠 Tech Stack

| Layer            | Tools & Frameworks                                    |
|------------------|-------------------------------------------------------|
| **Core**         | Python, Pandas, NumPy                                 |
| **Analytics**    | dbt, SQL, curated benchmarks                          |
| **Infra**        | Terraform, AWS Lambda                                 |
| **Testing**      | Playwright (E2E), Pytest                              |
| **Packaging**    | Poetry (`pyproject.toml`)                             |
| **Dev Tools**    | Makefile, GitHub Actions (CI), pnpm for e2e tests     |

---

### 📂 Project Structure

```bash
Assessment_Tool/
├── app/                 # Core app (UI/assets/main.py)
├── collectors/          # Data collection (e.g., finviz loader)
├── core/                # Financial metric calculations
├── dbt_quickfin/        # dbt models, staging & marts
├── infra/               # IaC (terraform + github workflows)
├── lambdas/             # AWS Lambda functions
├── scripts/             # Utilities (refresh, seeding)
├── tests/               # Pytest + Playwright e2e
└── README.md
```

### ⚡ Quickstart
**Clone the repo:**
```bash
git clone https://github.com/aiskakov28/Company-Financial-Health-Assessment-Dashboard.git
cd Company-Financial-Health-Assessment-Dashboard/Assessment_Tool
```
**Install dependencies:**
````
# Using Poetry
poetry install
````

**Run the app:**
```
poetry run python app/main.py
```
### 🧪 Testing
**Unit Tests:**
````
pytest tests/test_core.py
````

**E2E Tests (Playwright):**
````
cd tests/e2e
pnpm install
pnpm exec playwright install
pnpm exec playwright test
````

### 🔄 Continuous Integration
**This repo uses GitHub Actions to:**
* Run linting + tests 
* Build dbt models 
* Execute Playwright e2e checks 
* Upload reports as artifacts 
* Workflow: .github/workflows/playwright.yml

### 📈 Example Workflow
* Collect raw data from Finviz 
* Transform with dbt staging models 
* Enrich with financial metric benchmarks 
* Analyze & visualize company health in the dashboard 
* Automate refreshes with Lambda + Terraform

### 🤝 Contributing
**Contributions are welcome!**
* Fork the repo 
* Create a feature branch:
```
git checkout -b feat/my-feature
```
* Commit changes and push:
````
git push origin feat/my-feature
````
* Open a PR 🚀

### 📜 License
Distributed under the **MIT License**. See LICENSE for more info.
