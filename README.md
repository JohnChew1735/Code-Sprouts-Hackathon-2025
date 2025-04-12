# Balaena Quant

This project implements a **rolling backtest and forward test framework** for evaluating machine learning-based trading strategies using on-chain and off-chain crypto data.

---

## 📂 Project Structure

| Path                             | Description                                                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `main.py`                        | Main entry point of the project. Runs the rolling evaluation loop and visualizes results.                                |
| `backtest/`                      | Contains the core backtesting logic.                                                                                     |
| `strategy/`                      | Contains trading strategies such as Random Forest-based logic.                                                           |
| `dataloader/`                    | Responsible for loading, merging and preparing dataset from CSV files.                                                   |
| `model/`                         | Contains machine learning models, e.g., Random Forest model wrapper.                                                     |
| `customPandasData.py`            | Custom data class for integrating pandas DataFrames with Backtrader.                                                     |
| `config.py`                      | Configuration for parameters to be send to the different endpoints in retrieving dataset such as limit, start_time, etc. |
| `rolling_evaluation_results.csv` | Output file containing performance metrics from rolling evaluation (Sharpe, MDD, etc.).                                  |
| `src/` and `src_folder/`         | src contains files calling API and src_folders contain csv files storing the dataset.                                    |
| `README.md`                      | This file. Overview and documentation.                                                                                   |

---

## 🚫 Ignore These Folders

- `path/` – Internal notes or WIP paths.
- `ignore/` – Contains other endpoints and a base for randomForestModel before this library was created for debugging etc.

---

## ✅ How to Use

1. **Activate virtual environment and download dependencies**
   poetry env activate
   poetry install

2. **Run the main file** to start evaluation:
   poetry run python main.py

3. **Enter the parameters when prompted**
   You'll be asked to input features for the API.
   Default values are already set, so you can just press enter to use them.

4. **Sit back and let the model do the work**
   It will train on historical data, predict future movements, and show you key metrics like Sharpe Ratio, Drawdown, and Trade Frequency — along with a visual equity curve and buy/sell signals.
