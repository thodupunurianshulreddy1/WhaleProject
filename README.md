# Whale Wallet Tracking & Crypto Market Impact Analysis

## Project Overview

This project aims to analyze the impact of large cryptocurrency transactions, commonly called **whale transactions**, on cryptocurrency market behavior and volatility.

The objective is to build a complete Big Data pipeline capable of:
- collecting cryptocurrency market data,
- collecting whale wallet transaction data,
- storing the raw data inside a Data Lake architecture,
- transforming and combining the datasets,
- generating analytical indicators,
- exposing the final results through Elasticsearch and Kibana dashboards.

The project follows a modern Data Engineering workflow using APIs, Apache Spark, Airflow, Elasticsearch, and Kibana.

---

# Project Objective

Large cryptocurrency holders, known as whales, can significantly influence market behavior when transferring large amounts of crypto assets.

This project aims to:
- detect large blockchain transactions,
- analyze market reactions after whale movements,
- study possible correlations between whale activity and price volatility,
- visualize the results through dashboards.

Examples of analysis:
- price evolution after large BTC transfers,
- exchange inflow/outflow monitoring,
- abnormal whale activity detection,
- most active cryptocurrencies among whales.

---

# Data Sources

## 1. CoinGecko API

CoinGecko provides cryptocurrency market information.

Collected data includes:
- cryptocurrency name,
- symbol,
- current price,
- market capitalization,
- trading volume,
- price variation.

Example API:

```text
https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd
```

---

## 2. Whale Transaction API

A blockchain transaction API such as Whale Alert or Etherscan is used to collect large cryptocurrency transfers.

Collected data may include:
- blockchain,
- amount transferred,
- amount in USD,
- sender wallet,
- receiver wallet,
- timestamp,
- transaction hash.

---

# Global Architecture

The pipeline works as follows:

```text
CoinGecko API
        │
        ▼
Raw JSON Storage
        │
        ▼
Spark Formatting
        │
        ▼
Formatted Parquet
        │
        ▼

Whale Transaction API
        │
        ▼
Raw JSON Storage
        │
        ▼
Spark Formatting
        │
        ▼
Formatted Parquet
        │
        ▼

Spark Combination
        │
        ▼
Usage Dataset
        │
        ▼
Elasticsearch
        │
        ▼
Kibana Dashboard
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| REST APIs | Data collection |
| Apache Spark / PySpark | Data transformation and processing |
| Apache Airflow | Task orchestration |
| JSON | Raw data format |
| Parquet | Analytical data format |
| Elasticsearch | Final data indexing |
| Kibana | Dashboard visualization |
| Git / GitHub | Version control and collaboration |

---

# Git Project Architecture

```text
WhaleWalletTracking/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── dags/
│   └── whale_pipeline_dag.py
│
├── src/
│   ├── ingestion/
│   │   ├── fetch_coingecko.py
│   │   └── fetch_whale_transactions.py
│   │
│   ├── formatting/
│   │   ├── format_coingecko.py
│   │   └── format_whale_transactions.py
│   │
│   ├── combination/
│   │   └── combine_market_whales.py
│   │
│   └── indexing/
│       └── index_to_elasticsearch.py
│
├── datalake/
│   ├── raw/
│   ├── formatted/
│   └── usage/
│
├── notebooks/
│   └── exploration.ipynb
│
└── docs/
    ├── architecture.png
    └── report.pdf
```

---

# Data Lake Structure

The Data Lake follows a layered architecture:

## Raw Layer

Stores original API responses.

Example:

```text
datalake/raw/coingecko/markets/20260518/markets.json
datalake/raw/whale_alert/transactions/20260518/transactions.json
```

---

## Formatted Layer

Stores cleaned and normalized data in Parquet format.

Example:

```text
datalake/formatted/coingecko/markets/20260518/markets.parquet
```

---

## Usage Layer

Stores the final analytical datasets.

Example:

```text
datalake/usage/whale_analysis/market_impact/20260518/result.parquet
```

---

# Pipeline Steps

1. Extract cryptocurrency market data from CoinGecko.
2. Extract whale transaction data from Whale Alert or Etherscan.
3. Store raw API responses inside the Data Lake.
4. Use Apache Spark to clean and normalize data.
5. Convert formatted data into Parquet format.
6. Combine whale transactions with market prices.
7. Generate analytical indicators.
8. Index final datasets into Elasticsearch.
9. Visualize results through Kibana dashboards.

---

# Expected Dashboard

The Kibana dashboard may include:
- number of whale transactions per day,
- total whale transaction volume,
- biggest whale transfers,
- top cryptocurrencies moved by whales,
- BTC price evolution after whale transactions,
- exchange inflow and outflow activity,
- abnormal whale movement alerts.

---

# Final Objective

The final objective of this project is to build a reusable Big Data pipeline capable of detecting whale activity and analyzing its potential impact on cryptocurrency market volatility and market behavior.