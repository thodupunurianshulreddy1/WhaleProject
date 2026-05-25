import os
import json
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("WhaleWalletFormatting") \
    .getOrCreate()

JSON_FILES = [
    "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
    "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe",
    "0x50327c6c5a14dcade707abad2e27eb517df87ab5",
    "0xba2ae424d960c26247dd6c32edc70b295c744c43",
    "markets_20260518_200539"
]

RAW_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project"
FORMATTED_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project\datalake\formatted"
TEMP_BASE = r"C:\Users\Famille\Documents\ISEP\Big DATA\Project\datalake\temp"

os.makedirs(TEMP_BASE, exist_ok=True)

for json_file in JSON_FILES:
    print(f"\nProcessing file: {json_file}")

    input_path = os.path.join(RAW_BASE, f"{json_file}.json")
    temp_path = os.path.join(TEMP_BASE, f"{json_file}_clean.json")
    output_path = os.path.join(FORMATTED_BASE, json_file)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        if isinstance(raw_data, dict) and "result" in raw_data:
            records = raw_data["result"]
        elif isinstance(raw_data, list):
            records = raw_data
        else:
            records = []

        if not records:
            print(f"No records found for {json_file}")
            continue

        with open(temp_path, "w", encoding="utf-8") as f:
            for row in records:
                f.write(json.dumps(row) + "\n")

        df = spark.read.json(temp_path)

        df.printSchema()
        df.show(5, truncate=False)

        df.write.mode("overwrite").parquet(output_path)

        print(f"Parquet created: {output_path}")

    except Exception as e:
        print(f"Error processing {json_file}: {e}")

spark.stop()