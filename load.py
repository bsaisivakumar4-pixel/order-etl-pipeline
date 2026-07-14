"""
LOAD stage.

Job: write the cleaned data somewhere durable and queryable.
Here that's a SQLite file -- a real SQL database, just stored
as a single local file instead of a client-server system. Same
SQL you'd use against Postgres or Snowflake.

Mainframe parallel: this is your output DD statement writing to
the master file / DB2 table at the end of the batch job.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("warehouse.db")


def load(df: pd.DataFrame, table_name: str = "orders") -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        # if_exists="replace" makes this pipeline safely re-runnable --
        # running it twice won't duplicate data. Real pipelines usually
        # do something smarter (incremental/upsert loads), but full
        # replace is the right starting point to understand first.
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.commit()

        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"[load] Wrote {row_count:,} rows into '{table_name}' table in {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    from extract import extract
    from transform import transform

    raw_df = extract()
    clean_df = transform(raw_df)
    load(clean_df)
