import requests
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
# Get your free key at whale-alert.io
API_KEY = "CG-xRS754Yq1yxUxWc8QCgDaDF4" 
BASE_DIR = os.path.expanduser("~/Desktop/WhaleProject/lake/bronze")
# We track transactions over $1,000,000 USD
URL = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1"

def run_ingestion():
    print(f"[{datetime.now()}] Starting sonar scan for whales...")
    
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        
        if 'transactions' in data and data['transactions']:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whale_tx_{timestamp}.json"
            filepath = os.path.join(BASE_DIR, filename)
            
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            
            print(f"✅ Success! Captured {len(data['transactions'])} whales.")
            print(f"Saved to: lake/bronze/{filename}")
        else:
            print("🌊 The ocean is quiet. No large transactions found right now.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    os.makedirs(BASE_DIR, exist_ok=True)
    run_ingestion()
