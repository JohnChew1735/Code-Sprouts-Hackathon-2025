# pipeline/pipeline.py
from dataloader.dataloader import DataLoader
from backtest.backtester import Backtester
from model.random_forest_model import RandomForestModel

class Pipeline:
    def __init__(self, file1, file2, file3):
        self.data_loader = DataLoader(file1=file1, file2=file2, file3=file3)

    def run(self, window_years=2, step_months=6, forward_test_year=1):
        merged_data = self.data_loader.get_data()
        backtester = Backtester(data_loader=merged_data, rf_model_class=RandomForestModel)

        metrics_df, rolling_results = backtester.run_rolling_evaluation(
            window_years=window_years,
            step_months=step_months,
            forward_test_year=forward_test_year
        )

        metrics_df.to_csv('rolling_evaluation_results.csv', index=False)
        print("📊 Metrics saved to rolling_evaluation_results.csv")

        for i, result in enumerate(rolling_results):
            print(f"📈 Plotting result {i+1}/{len(rolling_results)}")
            backtester.plot_results(
                result["df"],
                result["buy_signals"],
                result["sell_signals"],
                result["equity_curve"]
            )
        print("✅ Rolling evaluation completed.")
