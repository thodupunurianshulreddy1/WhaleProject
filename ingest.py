import requests
import json
import os
from datetime import datetime

BASE_DIR = os.path.expanduser("~/Desktop/WhaleProject/datalake/raw/coingecko/markets")
URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1"

def run_ingestion():
    os.makedirs(BASE_DIR, exist_ok=True)

    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(BASE_DIR, f"markets_{timestamp}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Saved {len(data)} crypto market records to {filepath}")

if __name__ == "__main__":
    run_ingestion()
