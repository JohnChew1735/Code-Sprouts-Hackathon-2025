import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class RandomForestModel:
    def __init__(self, data, n_estimators=100, max_depth=None, random_state=42):
        self.data = data.copy()
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = RandomForestClassifier(n_estimators=self.n_estimators, max_depth=self.max_depth, random_state=self.random_state)
        self.scaler = StandardScaler()
        self.features = ['price_return', 'open_interest', 'addresses_count_active']
        self.last_timestamp = None
        self.X = None
        self.y = None

    def prepare_data(self):
        # Create future return and binary target
        self.data['price_return'] = self.data['close'].pct_change().shift(-1)
        self.data['target'] = (self.data['price_return'] > 0).astype(int)

        # Drop NA values
        self.data.dropna(subset=self.features + ['target'], inplace=True)

        # Track last timestamp
        if 'timestamp' in self.data.columns:
            self.last_timestamp = self.data['timestamp'].iloc[len(self.data) - 1]
        elif 'date' in self.data.columns:
            self.last_timestamp = self.data['date'].iloc[len(self.data) - 1]

        # Extract features and labels
        X = self.data[self.features]
        y = self.data['target']

        # Fit scaler on training features
        X_scaled = self.scaler.fit_transform(X)

        self.X, self.y = X_scaled, y
        return self.X, self.y

    def train(self):
        X, y = self.prepare_data()
        self.model.fit(X, y)

    def predict(self, new_data):
        # Ensure DataFrame with correct features is passed
        X_new = new_data[self.features]

        # Apply previously fitted scaler
        X_scaled = self.scaler.transform(X_new)

        # Predict
        predictions = self.model.predict(X_scaled)

        # Store results
        result_df = new_data.copy()
        result_df['prediction'] = predictions
        self.data = result_df
        return predictions

    def get_importances(self):
        # Return the feature importances from the trained model
        return self.model.feature_importances_

    def update_model(self, n_estimators=None, max_depth=None):
        if n_estimators is not None:
            self.n_estimators = n_estimators
            self.model.n_estimators = n_estimators
        if max_depth is not None:
            self.max_depth = max_depth
            self.model.max_depth = max_depth
        self.train()
