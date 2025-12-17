import numpy as np
from backtesting import Backtest, Strategy
from backtesting.test import SMA
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class SMABuySellStrategy(Strategy):
    sma_period = 14  # Default SMA period, will be optimized
    buy_pct = 1.0    # Default buy percentage below SMA, will be optimized
    sell_pct = 1.0   # Default sell percentage above SMA, will be optimized

    def init(self):
        # Calculate the SMA using the Close price and the sma_period
        self.sma = self.I(SMA, self.data.Close, self.sma_period)

    def next(self):
        # Calculate the buying and selling thresholds
        buy_threshold = self.sma[-1] * (1 - self.buy_pct / 100)
        sell_threshold = self.sma[-1] * (1 + self.sell_pct / 100)

        # If the Close price is below the buy threshold, buy
        if len(self.data.Close) > 0 and self.data.Close[-1] < buy_threshold:
            self.buy()

        # If the Close price is above the sell threshold, sell
        elif len(self.data.Close) > 0 and self.data.Close[-1] > sell_threshold:
            self.position.close()

# Load the data
data_path = '/Users/md/Dropbox/dev/github/OpenAI Debugger/backtests/dogwifhat/WIF_4h_50000.csv'  
#data_path = '/Users/md/Dropbox/dev/github/hyper-liquid-trading-bots/data/POPCAT_4h_5000.csv' # popcat
data = pd.read_csv(data_path, index_col=0, parse_dates=True)

# Correct the column names to match the DataFrame
data = data[['open', 'high', 'low', 'close', 'volume']]
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# Sort the data index in ascending order
data = data.sort_index()

# Create and configure the backtest
bt = Backtest(data, SMABuySellStrategy, cash=100000, commission=0.002)

# Optimization with heatmap
opt_stats, heatmap = bt.optimize(
    sma_period=range(10, 20),     # Test SMA periods from 10 to 50
    buy_pct=range(10, 25),         # Test buy percentages from 1% to 10%
    sell_pct=range(10, 25),        # Test sell percentages from 1% to 10%
    maximize='Equity Final [$]',
    constraint=lambda param: param.sma_period > 0 and param.buy_pct > 0 and param.sell_pct > 0,  # Ensure all parameters are positive
    return_heatmap=True,
)


# Print the optimization results
print(opt_stats)

# Convert heatmap data to a 2D DataFrame for plotting
heatmap_df = heatmap.unstack(level='buy_pct').T

# Plot the heatmap for the optimization results
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_df, annot=True, fmt=".2f", cmap='viridis')
plt.title("Optimization Heatmap")
plt.xlabel("Sell Percentage (%)")
plt.ylabel("Buy Percentage (%)")
plt.show()

# Run the backtest with the best parameters
results = bt.run(sma_period=opt_stats.sma_period, buy_pct=opt_stats.buy_pct, sell_pct=opt_stats.sell_pct)
print(results)

# Plot the performance
bt.plot()