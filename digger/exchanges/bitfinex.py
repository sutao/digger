import urllib
import urllib2
import json
import time
import hmac,hashlib

from exchanges.base import Exchange


# API Reference:
# http://docs.bitfinex.com/docs


class Bitfinex(Exchange):
    def __init__(self, api_key=None, secret=None):
        super(Bitfinex, self).__init__()
        self._api_key = api_key
        self._secret = secret


    def _api_public(self, command, req={}):
        if command == "Orderbook":
            ret = urllib2.urlopen(urllib2.Request('https://api.bitfinex.com/v1/book/' + str(req['currencyPair'])))
            return json.loads(ret.read())
        else:
            raise NotImplemented

    def query_order_book(self, currency1, currency2):
        currency_pair = '{}{}'.format(currency1.upper(), currency2.upper())
        book = self._api_public('Orderbook', {"currencyPair": currency_pair})
        bids, asks = [], []
        for b in book['bids']:
            bids.append([b['price'], b['amount']])
        for a in book['asks']:
            asks.append([a['price'], a['amount']])
        return dict(bids=bids, asks=asks)

