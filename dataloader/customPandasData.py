import backtrader as bt
import pandas as pd

class CustomPandasData(bt.feeds.PandasData):
    lines = ('price_return','open_interest', 'addresses_count_active')  # Add additional columns if needed

    # Define the parameters to map your dataframe columns to Backtrader's default columns
    # Depends on the endpoints called, edit as see fit
    params = (
        ('datetime', None),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
        ('price_return', -1),
        ('open_interest', -1),
        ('addresses_count_active', -1),
    )

    def __init__(self):
        super().__init__()
