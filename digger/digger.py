import itertools

from exchanges.poloniex import Poloniex
from exchanges.bitfinex import Bitfinex

pn = Poloniex()
bf = Bitfinex()

book_pn = pn.query_order_book('BTC', 'ETH')
book_bf = bf.query_order_book('ETH', 'BTC')

rows_pn = zip(book_pn['bids'], book_pn['asks'])[:10]
rows_bf = zip(book_bf['bids'], book_bf['asks'])[:10]

length = min(len(rows_bf), len(rows_pn))

print '{:>18s}{:>18s}{:>18s}{:>18s}{:>18s}{:>18s}{:>18s}{:>18s}'.format(
    'PN BID PRICE', 'PN BID AMNT', 'PN ASK PRICE', 'PN ASK AMNT',
    'BF BID PRICE', 'BF BID AMNT', 'BF ASK PRICE', 'BF ASK AMNT',
)
for i in range(length):
    print '{:18.6f}{:18.6f}{:18.6f}{:18.6f}{:18.6f}{:18.6f}{:18.6f}{:18.6f}'.format(
        float(rows_pn[i][0][0]), float(rows_pn[i][0][1]), float(rows_pn[i][1][0]), float(rows_pn[i][1][1]),
        float(rows_bf[i][0][0]), float(rows_bf[i][0][1]), float(rows_bf[i][1][0]), float(rows_bf[i][1][1]),
    )

if book_pn['asks'][0][0] < book_bf['bids'][0][0]:
    print 'Buy in PN and Sell in BF!'

if book_bf['asks'][0][0] < book_pn['bids'][0][0]:
    print 'Buy in BF and Sell in PN!'