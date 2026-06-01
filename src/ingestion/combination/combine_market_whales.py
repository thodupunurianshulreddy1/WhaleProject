import os
import pandas as pd

FORMATTED_BASE = r"C:\Users\Famille\WhaleProject\datalake\formatted"
USAGE_BASE = r"C:\Users\Famille\WhaleProject\datalake\usage"

ADDRESS_TO_COIN = {
    "0x2170ed0880ac9a755fd29b2688956bd959f933f8": "ethereum",
    "0xdac17f958d2ee523a2206206994597c13d831ec7": "tether",
    "0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe": "xrp",
    "0x50327c6c5a14dcade707abad2e27eb517df87ab5": "tron",
    "0xba2ae424d960c26247dd6c32edc70b295c744c43": "dogecoin"
}

all_transactions = []

for address, coin_id in ADDRESS_TO_COIN.items():
    path = os.path.join(FORMATTED_BASE, f"{address}.parquet")

    if not os.path.exists(path):
        print(f"Missing file: {path}")
        continue

    print(f"Reading: {path}")

    df = pd.read_parquet(path)
    df["contract_address"] = address
    df["coin_id"] = coin_id

    all_transactions.append(df)

if not all_transactions:
    raise ValueError("No transaction parquet files were found.")

transactions_df = pd.concat(all_transactions, ignore_index=True)

# Your markets file
markets_path = os.path.join(
    FORMATTED_BASE,
    "markets_20260518_200539.parquet"
)

if not os.path.exists(markets_path):
    raise FileNotFoundError(f"Missing markets file: {markets_path}")

markets_df = pd.read_parquet(markets_path)

markets_clean = markets_df[
    [
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "total_volume",
        "price_change_percentage_24h"
    ]
].rename(columns={"id": "coin_id"})

combined_df = transactions_df.merge(
    markets_clean,
    on="coin_id",
    how="left"
)

os.makedirs(USAGE_BASE, exist_ok=True)

output_file = os.path.join(USAGE_BASE, "market_impact_combined.parquet")
combined_df.to_parquet(output_file, index=False)

print(f"Combined dataset created: {output_file}")
print(combined_df.head())