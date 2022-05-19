
from ApiManager import ApiManager
from inspect import unwrap
import requests

class Fundamentals:

    def __init__(self, ticker, apiManager):
        self.ticker = ticker
        self.cashflow = apiManager.getCashflow()
        self.income = apiManager.getIncome()
        self.balanceSheet = apiManager.getBalanceSheet()
        self.metrics = apiManager.getMetrics()
        self.riskFreeRate = apiManager.getTreasuryYield()

    def unpack(self, input):
        if unwrap(input) == "None":
            return float(0)
        else:
            return float(input)

