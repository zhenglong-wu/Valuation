
from sys import api_version
import requests

class ApiManager:

    apiKey = 'IM95A052KPC7DLUE'

    def __init__(self, ticker):
        self.ticker = ticker

    def getCashflow(self):
        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={self.ticker}&apikey={self.apiKey}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getIncome(self):
        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.ticker}&apikey={self.apiKey}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getBalanceSheet(self):
        url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={self.ticker}&apikey={self.apiKey}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getEarnings(self):
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={self.ticker}&apikey={self.apiKey}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getMetrics(self):
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.ticker}&apikey={self.apiKey}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getTreasuryYield(self):
        url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey={self.apiKey}'
        apiReturn = requests.get(url)
        return apiReturn.json()

