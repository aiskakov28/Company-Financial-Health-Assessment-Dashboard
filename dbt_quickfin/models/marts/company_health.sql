with by_cat as (
  select
    ticker,
    category,
    avg(score) as category_score
  from {{ ref('stg_finviz_raw') }}
  group by 1,2
),
pivoted as (
  select
    ticker,
    max(case when category='Valuation' then category_score end) as valuation_score,
    max(case when category='Liquidity' then category_score end) as liquidity_score,
    max(case when category='Solvency' then category_score end) as solvency_score,
    max(case when category='Profitability' then category_score end) as profitability_score,
    max(case when category='Dividend' then category_score end) as dividend_score,
    max(case when category='Growth' then category_score end) as growth_score,
    max(case when category='Ownership' then category_score end) as ownership_score
  from by_cat
  group by 1
)
select
  p.*,
  round(avg(v) over (partition by ticker), 2) as overall_score
from pivoted p,
lateral (values
  (valuation_score),(liquidity_score),(solvency_score),
  (profitability_score),(dividend_score),(growth_score),(ownership_score)
) as t(v)
