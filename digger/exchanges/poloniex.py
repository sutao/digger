import urllib
import urllib2
import json
import time
import hmac,hashlib

from exchanges.base import Exchange


# API Reference:
# https://poloniex.com/support/api/


class Poloniex(Exchange):
    def __init__(self, api_key=None, secret=None):
        super(Poloniex, self).__init__()
        self._api_key = api_key
        self._secret = secret

    def _create_timestamp(datestr, format="%Y-%m-%d %H:%M:%S"):
        return time.mktime(time.strptime(datestr, format))


    def _post_process(self, before):
        after = before

        # Add timestamps if there isnt one but is a datetime
        if not isinstance(after, dict):
            return after

        ret = after.get('return')
        if isinstance(ret, list):
            for x in xrange(0, len(ret)):
                if isinstance(ret[x], dict) and 'datetime' in ret[x] and 'timestamp' not in ret[x]:
                    after['return'][x]['timestamp'] = float(self._create_timestamp(after['return'][x]['datetime']))

        return after


    def _api_query(self, command, req={}):
        if (command == "returnTicker" or command == "return24Volume"):
            ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=' + command))
            return json.loads(ret.read())
        elif (command == "returnOrderBook"):
            ret = urllib2.urlopen(urllib2.Request(
                'https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        elif (command == "returnMarketTradeHistory"):
            ret = urllib2.urlopen(urllib2.Request(
                'https://poloniex.com/public?command=' + "returnTradeHistory" + '&currencyPair=' + str(
                    req['currencyPair'])))
            return json.loads(ret.read())
        else:
            req['command'] = command
            req['nonce'] = int(time.time() * 1000)
            post_data = urllib.urlencode(req)

            sign = hmac.new(self._secret, post_data, hashlib.sha512).hexdigest()
            headers = {
                'Sign': sign,
                'Key': self._api_key
            }

            ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
            jsonRet = json.loads(ret.read())
            return self._post_process(jsonRet)

    def query_ticker(self):
        return self._api_query("returnTicker")

    def query_order_book(self, currency1, currency2):
        currency_pair = '{}_{}'.format(currency1.upper(), currency2.upper())
        return self._api_query('returnOrderBook', {"currencyPair": currency_pair})
