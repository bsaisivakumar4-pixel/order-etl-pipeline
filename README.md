# Project: Order Data ETL Pipeline

Your first hands-on data engineering project. Goal: build a working Extract → Transform → Load pipeline end to end, using nothing but Python and SQLite. No cloud account, no signup required.

Estimated time: a weekend (4-8 hours depending on pace).

---

## 1. Get the dataset

We're using the **Online Retail II** dataset — real transaction data from a UK-based online retailer, covering Dec 2009 to Dec 2011. It's the most commonly used "starter" dataset in data engineering tutorials, so you'll also recognize it if you look up help online.

**Download it here (pick either source):**
- UCI Machine Learning Repository (original source): https://archive.ics.uci.edu/dataset/502/online+retail+ii
- Kaggle mirror (easier download, needs free Kaggle account): https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset

Download the CSV and save it as:
```
order-etl-project/data/raw/online_retail.csv
```

If you get the UCI version, it may come as an `.xlsx` with two sheets (2009-2010 and 2010-2011). Either export it to CSV yourself, or just use one sheet — one year of data is plenty for this project.

**Columns you'll be working with:**
| Column | Meaning |
|---|---|
| InvoiceNo | Transaction ID (starts with 'C' if it's a cancellation) |
| StockCode | Product ID |
| Description | Product name |
| Quantity | Units purchased |
| InvoiceDate | Date/time of transaction |
| UnitPrice | Price per unit (£) |
| CustomerID | Customer ID |
| Country | Customer's country |

---

## 2. Set up your environment

You need Python 3.9+ installed. Check with:
```bash
python3 --version
```

Create a virtual environment (keeps this project's packages separate from everything else on your machine):
```bash
cd order-etl-project
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
```

Install the packages:
```bash
pip install -r requirements.txt
```

---

## 3. Project structure

```
order-etl-project/
├── data/
│   ├── raw/              ← put the downloaded CSV here
│   └── processed/        ← cleaned output lands here
├── warehouse.db           ← SQLite database (created automatically)
├── extract.py
├── transform.py
├── load.py
├── run_pipeline.py         ← runs all three steps in order
├── queries.sql             ← example analytical queries
└── requirements.txt
```

This mirrors how real pipelines are structured: separate, single-purpose scripts for each stage, rather than one giant script doing everything. That separation is the whole point of "ETL" as a concept — each stage can be tested, rerun, and debugged independently.

---

## 4. Run it

```bash
python run_pipeline.py
```

This will:
1. **Extract** — read the raw CSV into memory
2. **Transform** — clean nulls, fix types, remove cancelled orders, add a `total_price` column
3. **Load** — write the cleaned data into `warehouse.db` (a real SQL database file)

Then explore the results:
```bash
sqlite3 warehouse.db
```
```sql
.tables
SELECT * FROM orders LIMIT 10;
```
Or just open `queries.sql` and run those queries directly.

---

## 5. What to look at afterward

Open each script and read the comments — they explain *why* each transformation exists, not just what it does. Once you're comfortable, try these extensions (roughly in order of difficulty):

1. Add logging so the pipeline prints how many rows it processed and how many were dropped/invalid — this is a real DE habit (data quality visibility).
2. Add a second table — e.g. a `customers` dimension table separate from the `orders` fact table. This is your first taste of dimensional modeling.
3. Swap SQLite for Postgres (free, run locally via Docker) — same code, different connection string. This is the natural next step toward "real" data warehouses.
4. Schedule it — install Apache Airflow locally and turn `run_pipeline.py` into a DAG that runs daily. This is where your JCL scheduling experience will click immediately — Airflow DAGs and JCL job steps are conceptually the same idea.

---

## 6. Useful references

- pandas documentation: https://pandas.pydata.org/docs/
- SQLite Python docs: https://docs.python.org/3/library/sqlite3.html
- UCI dataset description (data dictionary): https://archive.ics.uci.edu/dataset/502/online+retail+ii
- Airflow "Getting started" (for when you're ready for step 4 above): https://airflow.apache.org/docs/apache-airflow/stable/start.html
