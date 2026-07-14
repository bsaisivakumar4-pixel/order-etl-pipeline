"""
Orchestration: runs Extract -> Transform -> Load in order.

This is a tiny, manual version of what Airflow (or your old JCL
job stream) does at scale: define the steps, define the order,
run them, report success/failure.
"""

import time
from extract import extract
from transform import transform
from load import load


def run_pipeline():
    start = time.time()
    print("=" * 60)
    print("Starting order ETL pipeline")
    print("=" * 60)

    raw_df = extract()
    clean_df = transform(raw_df)
    load(clean_df)

    elapsed = time.time() - start
    print("=" * 60)
    print(f"Pipeline finished in {elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
