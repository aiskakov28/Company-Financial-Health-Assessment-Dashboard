with latest as (
  select
    ticker,
    metric,
    value,
    _loaded_at,
    row_number() over (partition by ticker, metric order by _loaded_at desc) as rn
  from raw_finviz
),
clean as (
  select
    l.ticker,
    l.metric,
    trim(replace(replace(l.value,'(',''),')','')) as raw_value
  from latest l
  where l.rn = 1
),
parsed as (
  select
    c.ticker,
    c.metric,
    c.raw_value,
    case
      when c.raw_value ~ '^\s*-?\d+(\.\d+)?\s*%$'
        then replace(c.raw_value,'%','')::float
      when lower(c.raw_value) like '%b'
        then replace(lower(c.raw_value),'b','')::float * 1e9
      when lower(c.raw_value) like '%m'
        then replace(lower(c.raw_value),'m','')::float * 1e6
      when lower(c.raw_value) like '%k'
        then replace(lower(c.raw_value),'k','')::float * 1e3
      when c.raw_value ~ '^\s*-?\d+(\.\d+)?$'
        then c.raw_value::float
      else null::float
    end as num_value
  from clean c
),
joined as (
  select
    p.ticker,
    mb.category,
    mb.direction,
    p.metric,
    p.raw_value,
    p.num_value
  from parsed p
  join {{ ref('metric_benchmarks') }} mb
    on p.metric = mb.metric
),
scored as (
  select
    ticker,
    category,
    metric,
    raw_value,
    num_value,
    case
      when num_value is null then null
      when direction = 'higher_is_better' then least(100.0, greatest(0.0, num_value))
      else case when num_value <= 0 then 100.0 else round(100.0/(1.0+num_value), 2) end
    end as score
  from joined
)
select * from scored
