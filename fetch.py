import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import pandas as pd
import requests

class Fetcher():
    END_POINT  = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=%s&tickInterval=%s&_=%s"
    def __init__(self, market = "USDT-BTC", startDate = "0000000000000", interval = "day"):
        self.market    = market
        self.startDate = startDate
        self.interval  = interval
        self.refresh()

    def plot(self):
        """matplotlib plotting for historical data"""
        data = self.data
        dates = []
        for date in data['Timestamp']:
            date = date.replace("T", " ")
            dates.append(date)

        figure = plt.figure(self.market, figsize=(8, 6))
        figure.suptitle(self.market)
        ax = figure.add_subplot(111)
        ax.yaxis.set_major_locator(ticker.MultipleLocator(800))
        ax.plot(dates, data["Close"])
        plt.show()

    def getHistorical(self):
        """Returns historical data in DateFrame"""
        return self.data

    def refresh(self):
        """Refreshes data set"""
        self.data = self._fetch()

    def _fetch(self):
        """Fetches data from formatted ENDPOINT"""
        END_POINT = self.END_POINT % (self.market, self.interval, self.startDate)
        data = requests.get(END_POINT).json()
        self._check(data)
        data = pd.DataFrame(data["result"])  # get result data in list of dicts
        data.columns = ['Book Value', 'Close', 'High', 'Low', 'Open', 'Timestamp', 'Volume']
        return data

    def _check(self, r):
        """Checks query response message"""
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
    """Exception for invalid market name when fetching historical data"""
    def __init__(self):
        pass

class InvalidIntervalException(Exception):
    """Exception for invalid interval when fetching historical data"""
    def __init__(self):
        pass

class InvalidParameterException(Exception):
    """Exception for invalid parameters when fetching historical data"""
    def __init__(self):
        pass
