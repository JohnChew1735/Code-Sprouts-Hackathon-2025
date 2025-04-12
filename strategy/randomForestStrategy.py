import backtrader as bt
import pandas as pd

class RandomForestStrategy(bt.Strategy):
    params = (
        ('rf_model', None),  
    )

    def __init__(self):
        self.rf_model = self.params.rf_model

        # For tracking signals and equity
        self.buy_signals = []
        self.sell_signals = []
        self.equity_curve = []

    def next(self):
        # Extract the features for prediction
        new_data = pd.DataFrame([{
            'price_return': self.data.price_return[0],
            'open_interest': self.data.open_interest[0],
            'addresses_count_active': self.data.addresses_count_active[0],
        }])

        prediction = self.rf_model.predict(new_data)

        # Apply signal logic
        if prediction == 1 and not self.position:
            self.buy()
            self.buy_signals.append(1)
            self.sell_signals.append(0)
        elif prediction == 0 and self.position:
            self.sell()
            self.buy_signals.append(0)
            self.sell_signals.append(1)
        else:
            self.buy_signals.append(0)
            self.sell_signals.append(0)

        # Track equity curve
        self.equity_curve.append(self.broker.getvalue())
