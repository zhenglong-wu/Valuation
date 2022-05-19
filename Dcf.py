
from distutils.filelist import findall
from inspect import unwrap
import json
from re import X
from struct import unpack
from typing_extensions import Self
import numpy as np
from scipy.stats import pearsonr

from Fundamentals import Fundamentals
from ApiManager import ApiManager

class Dcf:

    def __init__(self, apiManager: ApiManager, fundamentals: Fundamentals):
        self.apiManager = apiManager
        self.fundamentals = fundamentals

    def calcIntrinsicvalue(self):

        # cost of debt

        effectiveTaxRate = self.fundamentals.unpack(self.fundamentals.income['annualReports'][0]['incomeTaxExpense']) / self.fundamentals.unpack(self.fundamentals.income['annualReports'][0]['incomeBeforeTax'])
        totalDebt = (self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][0]['shortTermDebt'])) + (self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][0]['longTermDebt'])) 
        interestExpense = self.fundamentals.unpack(self.fundamentals.income['annualReports'][0]['interestExpense'])
        costOfDebt = (interestExpense / totalDebt) / (1 - effectiveTaxRate)

        # cost of equity

        riskFreeRate = self.fundamentals.riskFreeRate['data'][0]['value'] / 100
        expectedReturn = float(0.105)
        beta = self.fundamentals.unpack(self.fundamentals.metrics['Beta'])
        costOfEquity = riskFreeRate + (beta * (expectedReturn - riskFreeRate))

        # debt/equity weights

        marketCap = self.fundamentals.unpack(self.fundamentals.metrics['MarketCapitalization'])
        debtWeight = totalDebt / (totalDebt + marketCap)
        equityWeight = marketCap / (totalDebt + marketCap)

        # WACC

        wacc = (costOfDebt * debtWeight) + (costOfEquity * equityWeight)

        # terminal value 

        terminalValue = self.fundamentals.unpack(self.fundamentals.metrics['EBITDA']) * self.fundamentals.unpack(self.fundamentals.metrics['EVToEBITDA'])

        # free cash flow 

        freeCashflowPast5y = [[1, 2, 3, 4], []]
        for i in range(3, -1, -1):
            changeInWorkingCapital = (self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][i+1]['totalCurrentAssets']) - self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][i+1]['totalCurrentLiabilities'])) - (self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][i]['totalCurrentAssets']) - self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][i]['totalCurrentLiabilities']))
            newCashFlow = self.fundamentals.unpack(self.fundamentals.income['annualReports'][i]['ebit']) + self.fundamentals.unpack(self.fundamentals.income['annualReports'][i]['depreciationAndAmortization']) - self.fundamentals.unpack(self.fundamentals.cashflow['annualReports'][i]['capitalExpenditures']) - changeInWorkingCapital
            freeCashflowPast5y[1].append(newCashFlow)
        pmcc = abs(pearsonr(freeCashflowPast5y[0], freeCashflowPast5y[1])[0])

        # free cashflow forecast 

        fcf = []

        netIncome = []
        for i in range(3, -1, -1):
            netIncome.append(self.fundamentals.unpack(self.fundamentals.cashflow['annualReports'][i]['netIncome']))
        fcfe = []
        for j in range(0, 3):
            fcfe.append(freeCashflowPast5y[1][j] / netIncome[j])
        fcfeMean = float(np.mean(fcfe))
        totalRevenue = []
        for k in range(3, -1, -1):
            totalRevenue.append(self.fundamentals.unpack(self.fundamentals.income['annualReports'][k]['totalRevenue']))
        revenueGrowthRate = []
        for x in range(1, 3):
            revenueGrowthRate.append((totalRevenue[x] - totalRevenue[x-1]) / totalRevenue[x-1])
        revenueGrowthRateMean = float(np.mean(revenueGrowthRate))
        netProfitMargin = []
        for y in (0, 3):
            netProfitMargin.append(netIncome[y] / totalRevenue[y])
        netProfitMarginMean = float(np.mean(netProfitMargin))
        totalRevenueForecast = [totalRevenue[3]]
        for z in range(0, 3):
            totalRevenueForecast.append(totalRevenueForecast[len(totalRevenueForecast)-1] * (1 + revenueGrowthRateMean))
        netIncomeForecast = []
        for i in range(0, 3):
            netIncomeForecast.append(totalRevenueForecast[i] * netProfitMarginMean)
        for j in range(0, 3):
            fcf.append(netIncomeForecast[j] * fcfeMean) 

        # discount cashflow

        fcfPresentValue = []
        for k in range(1, 4):
            fcfPresentValue.append(fcf[k-1] / (pow((1 + wacc), k)))
        fcfPresentValue.append(terminalValue / pow((1 + wacc), 4))
        ev = sum(fcfPresentValue)
        intrinsicValue = ev - totalDebt + self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][0]['cashAndCashEquivalentsAtCarryingValue'])

        return ((intrinsicValue - marketCap) / marketCap) * 100




