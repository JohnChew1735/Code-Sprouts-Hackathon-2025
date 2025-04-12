# main.py
from config import get_open_interest_config, get_addresses_count_config, get_price_config
from fetcher.data_fetcher import DataFetcher
from pipeline.pipeline import Pipeline

def main():
    path1 = 'src_folder/priceOhlcv.csv'
    path2 = 'src_folder/openInterest.csv'
    path3 = 'src_folder/addressesCount.csv'

    fetcher = DataFetcher(
        price_config=get_price_config(),
        open_interest_config=get_open_interest_config(),
        addresses_count_config=get_addresses_count_config(),
        path1=path1,
        path2=path2,
        path3=path3
    )

    try:
        file1, file2, file3 = fetcher.fetch_all()
        pipeline = Pipeline(file1, file2, file3)
        pipeline.run(window_years=2, step_months=6, forward_test_year=1)

    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    main()
