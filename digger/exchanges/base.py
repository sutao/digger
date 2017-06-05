

class Exchange(object):
    """
    Basic class for all exchanges. This class defines common interfaces for all exchanges.
    """

    def queryOrderBook(self, currency1, currency2):
        """
        Queries the current order book of a certain currency on the market
        :param currency1: Ticker for the buying currency, eg. BTC
        :param currency2: Ticker for the selling currency, eg. ETH
        :return: A dictionary in the format below
            {
                'bids': [[price1, volume1], [price2, volume2], ...],
                'asks': [[price1, volume1], [price2, volume2], ...],
            }
        """
        raise NotImplemented

    def queryTicker(self):
        raise NotImplemented
