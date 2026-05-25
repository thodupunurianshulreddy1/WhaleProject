import requests
import json
import os
from datetime import datetime

API_KEY = "YOUR_ETHERSCAN_API_KEY"

ADDRESSES = [
    "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
    "0x28C6c06298d514Db089934071355E5743bf21d60",
    "0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549",
    "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",
    "0xF977814e90dA44bFA03b6295A0616a897441aceC"
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