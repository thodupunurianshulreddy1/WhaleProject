import pandas as pd
from pathlib import Path

# List of addresses / filenames (without .json)
addresses = [
    "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
    "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe",
    "0x50327c6c5a14dcade707abad2e27eb517df87ab5",
    "0xba2ae424d960c26247dd6c32edc70b295c744c43",
    "markets_20260518_200539"
]

# Base folders
input_folder = Path(r"C:\Users\Famille\WhaleProject\datalake\raw")
output_folder = Path(r"C:\Users\Famille\WhaleProject\datalake\formatted")

# Create output folder if needed
output_folder.mkdir(parents=True, exist_ok=True)

# Loop through all files
for address in addresses:

    # Build full input/output paths
    input_json_path = input_folder / f"{address}.json"
    output_parquet_path = output_folder / f"{address}.parquet"

    try:
        # Read JSON
        df = pd.read_json(input_json_path)

        # If your files are JSONL instead, use this instead:
        # df = pd.read_json(input_json_path, lines=True)

        # Save parquet
        df.to_parquet(output_parquet_path, engine="pyarrow", index=False)

        print(f"SUCCESS: {input_json_path.name} -> {output_parquet_path.name}")

    except Exception as e:
        print(f"ERROR processing {input_json_path.name}: {e}")