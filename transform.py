"""
TRANSFORM stage.

Job: clean, validate, and reshape the raw data into something
trustworthy and analysis-ready. This is where most of a data
engineer's actual thinking happens -- deciding what counts as
"bad data" and what to do about it.

Mainframe parallel: this is your validation/edit-check logic,
the part of a COBOL program that rejects or flags bad records
before they hit the master file.
"""

import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    original_count = len(df)

    # 1. Drop rows with no CustomerID -- we can't attribute these sales
    #    to anyone, so they're not useful for customer-level analysis.
    df = df.dropna(subset=["CustomerID"])

    # 2. Drop cancelled orders -- InvoiceNo starting with 'C' means cancellation.
    #    Keeping these would double-count / distort revenue figures.
    df = df[~df["InvoiceNo"].str.startswith("C", na=False)]

    # 3. Drop rows with non-positive quantity or price -- these are
    #    data entry errors or adjustments, not real sales.
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    # 4. Fix types -- InvoiceDate needs to be an actual datetime,
    #    not a string, or date-based queries won't work correctly.
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # 5. Remove exact duplicate rows -- can happen from source system re-sends.
    df = df.drop_duplicates()

    # 6. Derive a new column -- this is the kind of business logic
    #    a transform stage is FOR: computing something the source
    #    system doesn't give you directly.
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    # 7. Trim whitespace / normalize text fields -- source systems
    #    are notoriously inconsistent here.
    df["Description"] = df["Description"].str.strip()
    df["Country"] = df["Country"].str.strip()

    cleaned_count = len(df)
    dropped = original_count - cleaned_count
    print(
        f"[transform] {original_count:,} rows in -> {cleaned_count:,} rows out "
        f"({dropped:,} dropped, {dropped/original_count:.1%})"
    )

    return df


if __name__ == "__main__":
    from extract import extract

    raw_df = extract()
    clean_df = transform(raw_df)
    print(clean_df.head())
    print(clean_df.describe())
