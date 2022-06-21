

from Fundamentals import Fundamentals

class CFROI:

    def __init__(self, fundamentals: Fundamentals):
        self.fundamentals = fundamentals

    def getWacc(self):

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

        return wacc

    def calculateCashflowReturnOnInvestment(self):

        wacc = self.getWacc

        ocf = []

        for i in range(4, -1, -1):
            ocf.append(self.fundamentals.unpack(self.fundamentals.cashflow['annualReports'][i]['operatingCashflow']))

        # capital employed = Total Equity + Short Term Debt + Capital Lease Obligations + Long Term Debt

        capitalEmployed = self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][0]['totalShareholderEquity']) + self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][0]['shortTermDebt']) + self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][0]['capitalLeaseObligations']) + self.fundamentals.unpack(self.fundamentals.balanceSheet['annualReports'][0]['longTermDebt'])

        cfroi = ocf[len(ocf)-1] / capitalEmployed

        ncfroi = cfroi - wacc

        return ncfroi

    

    