"""
EXTRACT stage.

Job: pull raw data from a source (here, a CSV file) into memory,
with zero business logic applied. In a real pipeline this stage
might instead call an API, query a source database, or read from
cloud storage (S3/GCS) -- the shape of this function stays the same.

Mainframe parallel: this is your input JCL step (DD statement
pointing at a dataset) -- just getting the raw records loaded.
"""

import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw/online_retail.csv")


def extract() -> pd.DataFrame:
    """Read the raw retail CSV and return it as a DataFrame, unmodified."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Could not find {RAW_DATA_PATH}. "
            "Download the dataset (see README.md step 1) and place it there."
        )

    df = pd.read_csv(
        RAW_DATA_PATH,
        encoding="ISO-8859-1",   # this dataset has non-UTF8 characters in Description
        dtype={"CustomerID": "string", "InvoiceNo": "string", "StockCode": "string"},
    )

    print(f"[extract] Loaded {len(df):,} raw rows from {RAW_DATA_PATH}")
    return df


if __name__ == "__main__":
    df = extract()
    print(df.head())
    print(df.dtypes)
