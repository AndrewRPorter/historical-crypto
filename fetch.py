import matplotlib.pyplot as plt
import pandas as pd
import requests

class Fetcher():
    END_POINT  = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=%s&tickInterval=%s&_=%s"
    def __init__(self, market = "USDT-BTC", startDate = "0000000000000", interval = "fiveMin"):
        self.market    = market
        self.startDate = startDate
        self.interval  = interval

    def plot(self):
        '''
        matplotlib plotting for historical data
        '''
        END_POINT = self.END_POINT % (self.market, self.interval, self.startDate)
        r = requests.get(END_POINT).json()
        self.__check(r)

        data = pd.DataFrame(r["result"])  # get result data in list of dicts

        dates = []
        for date in data['T']:
            date = date.replace("T", " ")
            dates.append(date)

        figure = plt.figure()
        ax = figure.add_subplot(111)
        ax.plot(dates, data["C"])
        plt.show()

    def getData(self):
        '''
            Returns historical data in DateFrame
        '''
        END_POINT = self.END_POINT % (self.market, self.interval, self.startDate)
        r = requests.get(END_POINT).json()
        self.__check(r)

        data = pd.DataFrame(r["result"])  # get result data in list of dicts
        return data

    def __check(self, r):
        if r["success"] != True:
            if r["message"] == "INVALID_MARKET":
                raise InvalidMarketException()
            elif r["message"] == "INVALID_TICK_INTERVAL":
                raise InvalidIntervalException()
            else:
                raise InvalidParameterException()

    def __str__(self):
        return str(self.getData())

class InvalidMarketException(Exception):
    '''
    Exception for invalid market name when fetching historical data
    '''
    def __init__(self):
        pass

class InvalidIntervalException(Exception):
    '''
    Exception for invalid interval when fetching historical data
    '''
    def __init__(self):
        pass

class InvalidParameterException(Exception):
    '''
    Exception for invalid parameters when fetching historical data
    '''
    def __init__(self):
        pass

f = Fetcher()
f.plot()
