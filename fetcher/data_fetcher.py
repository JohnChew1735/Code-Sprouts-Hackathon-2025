# fetcher/data_fetcher.py
from src.openInterest import fetch_open_interest
from src.addressesCount import fetch_addresses_count
from src.priceOhlcv import fetch_price_ohlcv

class DataFetcher:
    def __init__(self, price_config, open_interest_config, addresses_count_config, path1, path2, path3):
        self.price_config = price_config
        self.open_interest_config = open_interest_config
        self.addresses_count_config = addresses_count_config
        self.path1 = path1
        self.path2 = path2
        self.path3 = path3

    def fetch_all(self):
        df1 = fetch_price_ohlcv(**self.price_config, save_path=self.path1)
        df2 = fetch_open_interest(**self.open_interest_config, save_path=self.path2)
        df3 = fetch_addresses_count(**self.addresses_count_config, save_path=self.path3)

        if df1 is not None and df2 is not None and df3 is not None:
            print("✅ Datasets fetched and saved successfully.")
            return self.path1, self.path2, self.path3
        else:
            raise RuntimeError("❌ Failed to fetch all datasets.")
