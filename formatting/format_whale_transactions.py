import os
import json
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("FormatEtherscanTransactions").getOrCreate()

ADDRESSES = [
    "0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe",
    "0x50327c6c5a14dcade707abad2e27eb517df87ab5",
    "0xba2ae424d960c26247dd6c32edc70b295c744c43",
    "0xdac17f958d2ee523a2206206994597c13d831ec7"
]

RAW_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project"
FORMATTED_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project\datalake\_formatted"
TEMP_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project\datalake\temp"

os.makedirs(TEMP_BASE, exist_ok=True)

for address in ADDRESSES:
    input_path = os.path.join(RAW_BASE, f"{address}.json")
    temp_path = os.path.join(TEMP_BASE, f"{address}_clean.json")
    output_path = os.path.join(FORMATTED_BASE, address)

    print(f"Processing address: {address}")

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    records = raw_data.get("result", [])

    if not records:
        print(f"No transactions found for {address}")
        continue

    with open(temp_path, "w", encoding="utf-8") as f:
        for row in records:
            f.write(json.dumps(row) + "\n")

    df = spark.read.json(temp_path)
    df.write.mode("overwrite").parquet(output_path)

    print(f"Parquet created: {output_path}")

spark.stop()