import requests
import json
import os
from datetime import datetime

API_KEY = "KERIZSGWDRX7X98NVW9AAH79F7V7DFHTWW"

#different adresses of the smart contracts
ADDRESSES = [
    "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
    "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe",
    "0x50327c6c5a14dcade707abad2e27eb517df87ab5",
    "0xba2ae424d960c26247dd6c32edc70b295c744c43"
]

BASE_DIR = os.path.expanduser("~/Desktop/WhaleProject/datalake/raw/etherscan/transactions")

def fetch_transactions(address):
    url = (
        "https://api.etherscan.io/v2/api"
        "?chainid=1"
        "&module=account"
        "&action=txlist"
        f"&address={address}"
        "&startblock=0"
        "&endblock=99999999"
        "&page=1"
        "&offset=100"
        "&sort=desc"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_json(data, address):
    date = datetime.now().strftime("%Y%m%d")
    folder = os.path.join(BASE_DIR, date)
    os.makedirs(folder, exist_ok=True)

    filename = f"{address}.json"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Saved data for {address} to {filepath}")

def main():
    for address in ADDRESSES:
        print(f"Fetching transactions for {address}...")
        data = fetch_transactions(address)
        save_json(data, address)

if __name__ == "__main__":
    main()