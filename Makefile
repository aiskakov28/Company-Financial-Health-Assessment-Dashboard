.PHONY: dev test e2e dbt seed

dev:
	python -m app.main

test:
	pytest -q

e2e:
	npx playwright test

dbt:
	cd dbt_quickfin && dbt build

seed:
	python scripts/seed_demo_data.py
