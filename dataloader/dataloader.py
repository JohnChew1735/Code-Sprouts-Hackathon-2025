import pandas as pd

class DataLoader:
    def __init__(self, file1, file2, file3, return_col='close', return_shift=1):
        
        self.return_col = return_col
        self.return_shift = return_shift

        # Load and preprocess datasets
        self.file1_data = self._load_csv(file1, time_col='start_time', unit='ms')
        self.file2_data = self._load_csv(file2, time_col='start_time', unit='ms')
        self.file3_data = self._load_csv(file3, time_col='datetime')

        # Merge all into one DataFrame
        self.merged_data = self._merge_data()

    def _load_csv(self, file_path, time_col, unit=None):
        df = pd.read_csv(file_path)
        if unit:
            df[time_col] = pd.to_datetime(df[time_col], unit=unit)
        else:
            df[time_col] = pd.to_datetime(df[time_col])
        df.set_index(time_col, inplace=True)
        return df

    def _merge_data(self):
        # Merge file 1 and file 2
        merged = self.file1_data.merge(
            self.file2_data[['open_interest']],
            left_index=True,
            right_index=True,
            how='inner'
        )

        # Merge file 1 and file 2 with file 3
        address_cols = [col for col in self.file3_data.columns if 'address' in col or 'count' in col]
        merged = merged.merge(
            self.file3_data[address_cols],
            left_index=True,
            right_index=True,
            how='inner'
        )

        # Calculate return 
        merged['price_return'] = merged[self.return_col].pct_change(periods=self.return_shift).shift(-self.return_shift)

        # Drop NaNs
        merged = merged.dropna()

        return merged

    def get_data(self):
        return self.merged_data
