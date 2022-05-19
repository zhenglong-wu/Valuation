
from this import d
from ApiManager import ApiManager
from Fundamentals import Fundamentals
from Dcf import Dcf

ticker = 'RTX'
apiManager = ApiManager(ticker=ticker)
fundamentals = Fundamentals(ticker=ticker, apiManager=apiManager)

dcf = Dcf(apiManager=apiManager, fundamentals=fundamentals)



