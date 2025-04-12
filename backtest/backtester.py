import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt
import mplfinance as mpf
from dataloader.customPandasData import CustomPandasData
from strategy.randomForestStrategy import RandomForestStrategy

class Backtester:
    def __init__(self, data_loader, rf_model_class, initial_cash=10000, commission=0.0006):
        self.data_loader = data_loader
        self.rf_model_class = rf_model_class
        self.initial_cash = initial_cash
        self.commission = commission

    def run_rolling_evaluation(self, window_years=2, step_months=6, forward_test_year=1):
        full_data = self.data_loader
        start_date = full_data.index.min()
        end_date = full_data.index.max()

        window = pd.DateOffset(years=window_years)
        step = pd.DateOffset(months=step_months)
        forward_step = pd.DateOffset(years=forward_test_year)

        current_start = start_date
        results_summary = []
        rolling_results = []

        # Define hyperparameter grid
        param_grid = [
            {"n_estimators": 100, "max_depth": 5},
            {"n_estimators": 100, "max_depth": 10},
            {"n_estimators": 200, "max_depth": 5},
            {"n_estimators": 200, "max_depth": 10},
        ]

        while current_start + window <= end_date:
            current_end = current_start + window
            window_data = full_data[(full_data.index >= current_start) & (full_data.index < current_end)]

            print(f"\n📆 Rolling Window: {current_start.date()} to {current_end.date()}")

            best_metrics = {
                "sharpe": -float("inf"),
                "params": None,
                "model": None,
                "strategy_result": None,
                "drawdown": None,
                "trade_freq": None,
                "cerebro": None
            }

            # Try all combinations in param grid
            for params in param_grid:
                try:
                    rf_model = self.rf_model_class(window_data, **params)
                    rf_model.train()

                    data_feed = CustomPandasData(dataname=window_data)
                    cerebro = bt.Cerebro()
                    cerebro.addstrategy(RandomForestStrategy, rf_model=rf_model)
                    cerebro.adddata(data_feed)
                    cerebro.broker.set_cash(self.initial_cash)
                    cerebro.broker.setcommission(commission=self.commission)
                    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
                    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
                    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='tradeanalyzer')

                    results = cerebro.run()
                    strat = results[0]

                    sharpe = strat.analyzers.sharpe.get_analysis().get('sharperatio', None)
                    drawdown = strat.analyzers.drawdown.get_analysis().max.drawdown
                    trades = strat.analyzers.tradeanalyzer.get_analysis().total.total or 0
                    trade_freq = (trades / len(window_data)) * 100

                    if sharpe is not None and sharpe > best_metrics["sharpe"]:
                        best_metrics.update({
                            "sharpe": sharpe,
                            "params": params,
                            "model": rf_model,
                            "strategy_result": strat,
                            "drawdown": drawdown,
                            "trade_freq": trade_freq,
                            "cerebro": cerebro
                        })

                except Exception as e:
                    print(f"Failed with params {params}: {e}")
                    continue

            if best_metrics["model"] is None:
                print(" No valid model found for this window.")
                current_start += step
                continue

            print(f"Best Params: {best_metrics['params']} | Sharpe: {best_metrics['sharpe']:.2f}, MDD: {best_metrics['drawdown']:.2f}%, Trade Freq: {best_metrics['trade_freq']:.2f}%")

            # 🧪 Forward Testing
            forward_start = current_end
            forward_end = current_end + forward_step
            forward_data = full_data[(full_data.index >= forward_start) & (full_data.index < forward_end)]

            print(f"📆 Forward Test: {forward_start.date()} to {forward_end.date()}")

            if not forward_data.empty:
                rf_model_forward = self.rf_model_class(forward_data, **best_metrics["params"])
                rf_model_forward.train()
                forward_data = rf_model_forward.data

                forward_data_feed = CustomPandasData(dataname=forward_data)
                cerebro_forward = bt.Cerebro()
                cerebro_forward.addstrategy(RandomForestStrategy, rf_model=rf_model_forward)
                cerebro_forward.adddata(forward_data_feed)
                cerebro_forward.broker.set_cash(self.initial_cash)
                cerebro_forward.broker.setcommission(commission=self.commission)
                cerebro_forward.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
                cerebro_forward.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
                cerebro_forward.addanalyzer(bt.analyzers.TradeAnalyzer, _name='tradeanalyzer')

                forward_results = cerebro_forward.run()
                strat_forward = forward_results[0]

                sharpe_forward = strat_forward.analyzers.sharpe.get_analysis().get('sharperatio', None)
                drawdown_forward = strat_forward.analyzers.drawdown.get_analysis().max.drawdown
                trades_forward = strat_forward.analyzers.tradeanalyzer.get_analysis().total.total or 0
                trade_freq_forward = (trades_forward / len(forward_data)) * 100

                print(f"📈 Forward Sharpe: {sharpe_forward}, MDD: {drawdown_forward:.2f}%, Trade Freq: {trade_freq_forward:.2f}%")

                success = int(
                    (sharpe_forward is not None and sharpe_forward >= 1.8) and
                    (drawdown_forward <= 40) and
                    (trade_freq_forward >= 3)
                )

                results_summary.append({
                    'window_start': current_start.date(),
                    'window_end': current_end.date(),
                    'sharpe_backtest': best_metrics["sharpe"],
                    'mdd_backtest': best_metrics["drawdown"],
                    'trade_freq_backtest': best_metrics["trade_freq"],
                    'final_value_backtest': best_metrics["cerebro"].broker.getvalue(),
                    'sharpe_forwardtest': sharpe_forward,
                    'mdd_forwardtest': drawdown_forward,
                    'trade_freq_forwardtest': trade_freq_forward,
                    'final_value_forwardtest': cerebro_forward.broker.getvalue(),
                    'best_params': best_metrics["params"],
                    'success': success
                })

                df = strat_forward.data._dataname
                buy_signals = pd.Series(strat_forward.buy_signals, index=df.index)
                sell_signals = pd.Series(strat_forward.sell_signals, index=df.index)
                equity_curve = strat_forward.equity_curve

                rolling_results.append({
                    "df": df,
                    "buy_signals": buy_signals,
                    "sell_signals": sell_signals,
                    "equity_curve": equity_curve
                })

            current_start += step

        return pd.DataFrame(results_summary), rolling_results

    def plot_results(self, df, buy_signals, sell_signals, equity_curve):
        buy_markers = mpf.make_addplot(buy_signals * df['close'], type='scatter', markersize=100, marker='^', color='g')
        sell_markers = mpf.make_addplot(sell_signals * df['close'], type='scatter', markersize=100, marker='v', color='r')

        mpf.plot(df, type='candle', addplot=[buy_markers, sell_markers], volume=True, style='charles')

        plt.figure(figsize=(10, 4))
        plt.plot(equity_curve, label='Equity Curve', color='blue')
        plt.title('Equity Curve')
        plt.ylabel('Portfolio Value')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()
