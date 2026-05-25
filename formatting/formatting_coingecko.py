import os
import json
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("FormatCoinGeckoMarket").getOrCreate()

RAW_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project"
FORMATTED_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project\datalake_\formatted\coingecko"
TEMP_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project\datalake\temp"

MARKET_FILE = "markets_20260518_200539"

os.makedirs(TEMP_BASE, exist_ok=True)

input_path = os.path.join(RAW_BASE, f"{MARKET_FILE}.json")
temp_path = os.path.join(TEMP_BASE, f"{MARKET_FILE}_clean.json")
output_path = os.path.join(FORMATTED_BASE, "markets")

with open(input_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

with open(temp_path, "w", encoding="utf-8") as f:
    for row in raw_data:
        f.write(json.dumps(row) + "\n")

df = spark.read.json(temp_path)
df.write.mode("overwrite").parquet(output_path)

print(f"CoinGecko market parquet created: {output_path}")

spark.stop()