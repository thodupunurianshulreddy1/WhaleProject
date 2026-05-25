import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col

spark = SparkSession.builder \
    .appName("CombineMarketWhales") \
    .getOrCreate()

FORMATTED_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project\datalake\formatted"
USAGE_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project\datalake\usage\whale_analysis\market_impact"

ADDRESS_TO_COIN = {
    "0x2170ed0880ac9a755fd29b2688956bd959f933f8": "ethereum",
    "0xdac17f958d2ee523a2206206994597c13d831ec7": "tether",
    "0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe": "xrp",
    "0x50327c6c5a14dcade707abad2e27eb517df87ab5": "tron",
    "0xba2ae424d960c26247dd6c32edc70b295c744c43": "dogecoin"
}

all_transactions = None

for address, coin_id in ADDRESS_TO_COIN.items():
    path = os.path.join(FORMATTED_BASE, address)

    df = spark.read.parquet(path) \
        .withColumn("contract_address", lit(address)) \
        .withColumn("coin_id", lit(coin_id))

    all_transactions = df if all_transactions is None else all_transactions.unionByName(df, allowMissingColumns=True)

markets_path = os.path.join(FORMATTED_BASE, "markets_20260518_200539")
markets_df = spark.read.parquet(markets_path)

markets_clean = markets_df.select(
    col("id").alias("coin_id"),
    col("symbol"),
    col("name"),
    col("current_price"),
    col("market_cap"),
    col("total_volume"),
    col("price_change_percentage_24h")
)

combined_df = all_transactions.join(markets_clean, on="coin_id", how="left")

combined_df.show(10, truncate=False)

combined_df.write.mode("overwrite").parquet(USAGE_BASE)

print(f"Combined usage dataset created at: {USAGE_BASE}")

spark.stop()