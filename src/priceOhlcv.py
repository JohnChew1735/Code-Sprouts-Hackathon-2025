import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["API_KEY"]
BASE_URL = 'https://api.datasource.cybotrade.rs/cryptoquant/eth/market-data/price-ohlcv'

def fetch_price_ohlcv(limit, start_time, exchange, window, save_path='src_folder/priceOhlcv.csv'):
    headers = {'X-API-Key': API_KEY}
    params = {
        "limit": str(limit),
        "start_time": str(start_time),
        "exchange": exchange,
        "window": window
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        print("Request Successful!")
        data = response.json()

        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif 'data' in data and isinstance(data['data'], list):
            df = pd.DataFrame(data['data'])
        else:
            print("Unexpected data structure:", data)
            return None

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)
        print(f"Data saved to {save_path}")
        return df

    else:
        print(f"Error: Received status code {response.status_code}")
        try:
            print("Details:", response.json())
        except ValueError:
            print("Raw response:", response.text)
        return None
