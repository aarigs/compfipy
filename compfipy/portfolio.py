"""
portfolio.py

Define a specifc group of Assets along with functions that pertain to the portfolio.

### Portfolio
- [x] Aggregate specific Assets in Table
- [x] keep track of positions
- [x] keep track of fees
- [x] keep track of cost
- [x] keep track of value
- [x] Enter and Exit position
- [ ] ???Rebalance whole Portfolio???
- [x] Return weights
- [ ] Total Unrealized Performance measures (based on specific time)
- [ ] Total Unrealized Risk measures (based on specific time)
- [ ] Total Unrealized Market Comparisons (based on specific time)
- [ ] Total Realized Performance measures (based on holdings)
- [ ] Total Realized Risk measures (based on holdings)
- [ ] Total Realized Market Comparisons (based on holdings)
- [ ] Summarize Portfolio
- [ ]

"""
# libs used
import copy
import datetime as dt
import pandas as pd
import numpy as np
import scipy.stats
import collections
import tabulate

class Portfolio(object):
    """
    define a collection of assets with holdings
    """

    def __init__(self, assets=None, initial_positions=None, cash=10000.0):

        # create empty tables
        empty_table = pd.DataFrame(
            np.zeros((len(assets[0].close), len(assets))),
            columns=[symbol for symbol in assets.keys()],
            index=assets[0].close.index
        )

        positions = copy.deepcopy(empty_table)
        trades = copy.deepcopy(empty_table)

        # initial position if given
        for symbol, value in initial_positions.items():
            trades[symbol][0] = value * assets[symbol].close[0]
            positions[symbol][:] = value

        self.init_cash = cash
        self.cash = cash
        self.assets = assets
        self.positions = positions
        self.trades = trades

    def summary(self):
        """ "summarize all the holdings and performance of the portfolio """
        pass

    def trade(self, symbol='', date=-1, amount=0.0, commission_min=1.0, commission=0.0075):
        """ execute a trade and update positions """
        self.trades[symbol][date] = amount * self.assets[symbol].close[date] + min(commission_min, commission * amount)
        self.positions[symbol][date:] = self.positions[symbol][date] + amount

    # Calculate Asset-wise numbers and statistics
    def close(self, date_range=slice(None, None, None)):
        """return closing price for each asset"""
        return pd.DataFrame({symbol: asset.close[date_range] for symbol, asset in self.assets.items()})

    def pct_change(self, date_range=slice(None, None, None)):
        """return closing price returns for each asset"""
        return 100.0 * self.close(date_range).pct_change()

    def values(self, date_range=slice(None, None, None)):
        """ calculate value of each position (shares * close) """
        return self.positions[:][date_range] * self.close(date_range)

    def weights(self, date_range=slice(None, None, None)):
        """ return asset weights of portfolio """
        return self.values(date_range=date_range) / self.total_value(date_range=date_range)

    def cost_bases(self, date_range=slice(None, None, None)):
        """ calculate cost basis of assets """
        costs = self.trades.cumsum()
        return costs[date_range]

    def gains(self, date_range=slice(None, None, None)):
        """ calculate gain of assets"""
        return self.values(date_range=date_range) - self.cost_bases(date_range=date_range)

    def returns(self, date_range=slice(None, None, None)):
        """calculate returns of assets"""
        return 100.0 * self.gains(date_range=date_range) / self.cost_bases(date_range=date_range)

    # Calculate Portfolio totals as sums or weighted sums of individual assets
    def total_value(self, date_range=slice(None, None, None)):
        """calculate portfolio value"""
        return self.values(date_range=date_range).sum(axis=1)

    def total_value(self, date_range=slice(None, None, None)):
        """calculate portfolio balance (asset value + cash)"""
        return self.total_value(date_range=date_range) + self.cash

    def total_cost_basis(self, date_range=slice(None, None, None)):
        """calculate portfolio cost basis"""
        return self.cost_bases(date_range=date_range).sum(axis=1)

    # Total Performance
    def total_gain(self, date_range=slice(None, None, None)):
        """calculate portfolio gain"""
        return self.gains(date_range=date_range).sum(axis=1)

    def total_return(self, date_range=slice(None, None, None)):
        """calculate portfolio returns"""
        return (self.weights(date_range=date_range) * self.returns(date_range=date_range)).sum(axis=1)
