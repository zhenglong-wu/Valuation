
from re import A
from sys import api_version
import requests

class ApiManager:

    apiKey1 = 'IM95A052KPC7DLUE'
    apiKey2 = 'A1LBCFR5AF7A0LB0'

    def __init__(self, ticker):
        self.ticker = ticker

    def getCashflow(self):
        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={self.ticker}&apikey={self.apiKey1}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getIncome(self):
        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.ticker}&apikey={self.apiKey1}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getBalanceSheet(self):
        url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={self.ticker}&apikey={self.apiKey1}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getEarnings(self):
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={self.ticker}&apikey={self.apiKey1}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getMetrics(self):
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.ticker}&apikey={self.apiKey1}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getTreasuryYield(self):
        url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey={self.apiKey2}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getConsumerSentiment(self):
        url = f'https://www.alphavantage.co/query?function=CONSUMER_SENTIMENT&apikey={self.apiKey2}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getDurableGoodsSales(self):
        url = f'https://www.alphavantage.co/query?function=DURABLES&apikey={self.apiKey2}'
        apiReturn = requests.get(url)
        return apiReturn.json()

    def getInflationExpectation(self):
        url = f'https://www.alphavantage.co/query?function=INFLATION_EXPECTATION&apikey={self.apiKey2}'
        apiReturn = requests.get(url)
        return apiReturn.json()
