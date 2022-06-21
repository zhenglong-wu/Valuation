
from this import d
from ApiManager import ApiManager
from Fundamentals import Fundamentals
from DCF import DCF
from CFROI import CFROI
from Ratios import Ratios

ticker = 'AAPL'
apiManager = ApiManager(ticker=ticker)
fundamentals = Fundamentals(ticker=ticker, apiManager=apiManager)

dcf = DCF(fundamentals=fundamentals)
ncfroi = CFROI(fundamentals=fundamentals)
ratios = Ratios(fundamentals=fundamentals) 

print(dcf.calcIntrinsicvalue())



