import os
from datetime import datetime, timezone
from typing import Dict, Iterable

from sqlalchemy import create_engine, text


def _pg_url() -> str:
    host = os.getenv("PG_HOST", "localhost")
    port = os.getenv("PG_PORT", "5432")
    user = os.getenv("PG_USER", "quickfin")
    pwd  = os.getenv("PG_PASSWORD", "secret")
    db   = os.getenv("PG_DATABASE", "quickfin")
    return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"


def ensure_table() -> None:
    engine = create_engine(_pg_url(), future=True)
    ddl = """
    create table if not exists raw_finviz (
        ticker text not null,
        metric text not null,
        value  text,
        _loaded_at timestamptz not null
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))


def write_raw_to_postgres(ticker: str, metrics: Dict[str, str]) -> int:
    ensure_table()
    engine = create_engine(_pg_url(), future=True)
    rows: Iterable[dict] = (
        {
            "ticker": ticker.upper(),
            "metric": k,
            "value": v,
            "_loaded_at": datetime.now(timezone.utc),
        }
        for k, v in metrics.items()
    )
    sql = text("""
        insert into raw_finviz (ticker, metric, value, _loaded_at)
        values (:ticker, :metric, :value, :_loaded_at)
    """)
    count = 0
    with engine.begin() as conn:
        for r in rows:
            conn.execute(sql, r)
            count += 1
    return count
