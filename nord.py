# try and except
# try and except
# try and except
# try and except
# try and except
# try and except
# try and except

from ast import Num
from decimal import Decimal
from kucoin.client import Market
from kucoin.client import Trade
from numpy import round_
import requests
import json
import math
import datetime
from decimal import *
from struct import pack
from tkinter import Y
import requests
import time
import json
import datetime
import ccxt, time, sys
from kucoin.client import Trade
from kucoin.client import Market
from time import sleep
from pprint import pprint
from kucoin.client import Trade
from kucoin.client import Market
import pandas as pd
import asyncio
import os
import sys
from pprint import pprint
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')
import ccxt.async_support as ccxt    
import ccxt

import asyncio
import os
import sys
from pprint import pprint
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')
import ccxt.async_support as ccxt 

while True:
  import asyncio
  import os
  import sys
  from pprint import pprint
  root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  sys.path.append(root + '/python')
  import ccxt.async_support as ccxt  # noqa: E402
  async def main(asyncio_loop):
    exchange = ccxt.kucoin ({
        'asyncio_loop': asyncio_loop,
        'enableRateLimit': False,
        'apiKey':'6263188c797c73000178f84d',
        'secret':'d58f6945-c73f-4622-ad4d-94d830e5826e',
        'password':'003003kM',
    })
  
    start_capital = 1000
    url = 'https://api.kucoin.com'
    try:
        while True:  
            ticker = requests.get(url + '/api/v1/market/orderbook/level1?symbol=NORD-USDT').json()
            kucoin_dfi_usd = Decimal((ticker['data']).get('bestAsk'))
            stop_kucoin_dfi_usd = Decimal(kucoin_dfi_usd * Decimal(0.991))
            
            ticker = requests.get(url + '/api/v1/market/orderbook/level1?symbol=NORD-BTC').json()
            kucoin_dfi_btc = Decimal((ticker['data']).get('bestBid'))
            
            ticker = requests.get(url + '/api/v1/market/orderbook/level1?symbol=BTC-USDT').json()
            kucoin_btc_usd = Decimal((ticker['data']).get('bestBid'))
            stop_kucoin_btc_usd = Decimal(kucoin_btc_usd * Decimal(0.991))
         
            first_step = start_capital / kucoin_dfi_usd
            second_step = first_step * kucoin_dfi_btc
            third_step = second_step * kucoin_btc_usd
            
            spread = ((third_step - start_capital) / start_capital * 100) 
            
            print(spread)
            if spread > 0.3:
                
                while True:    
                    ticker = requests.get(url + '/api/v1/market/orderbook/level1?symbol=NORD-USDT').json()
                    new_kucoin_dfi_usd = Decimal((ticker['data']).get('price'))
                    
                    if new_kucoin_dfi_usd < Decimal(Decimal(kucoin_dfi_usd) * Decimal(0.99)):
                        cancel_orders = await exchange.cancel_all_orders('NORD-USDT')
                        pprint(cancel_orders)
                        
                        stop_loss_order = await exchange.create_order(symbol='NORD-USDT',type='limit',side='sell',amount=usdt_balance,price=new_kucoin_dfi_usd)
                        pprint(stop_loss_order)
                        break
                    
                    try:
                        #commence the trade! buy XYZ-USDT. 
                        balance = await exchange.fetch_balance()
                        usdt_balance = Decimal((balance.get("info").get("data")[0].get("balance")))
                        final = Decimal(usdt_balance / kucoin_dfi_usd)
                        final = math.floor(final * 100) / 100
                        first_order = await exchange.create_order(symbol='NORD-USDT',type='limit',side='buy',amount=final,price=kucoin_dfi_usd)
                        pprint(first_order)
                        
                    except Exception:
                        pass
                     
                    try:    
                        balance = await exchange.fetch_balance()
                        usdt_balance = Decimal((balance.get("info").get("data")[0].get("balance")))
                        final = Decimal(usdt_balance / kucoin_dfi_btc)
                        second_order = await exchange.create_order(symbol='NORD-BTC',type='limit',side='sell',amount=usdt_balance,price=kucoin_dfi_btc)
                        pprint(second_order)
                    
                    except Exception:
                        pass
                    
                    try:
                        balance = await exchange.fetch_balance()
                        usdt_balance = Decimal((balance.get("info").get("data")[0].get("balance")))
                        final = Decimal(usdt_balance / kucoin_btc_usd)
                        third_order = await exchange.create_order(symbol='BTC-USDT',type='limit',side='sell',amount=usdt_balance,price=kucoin_btc_usd)
                        pprint(third_order)

                    except Exception:
                        pass
                
    except Exception:
        pass            
    
    await exchange.close()
    
                        
  if __name__ == '__main__':
      asyncio_loop = asyncio.get_event_loop()
      asyncio_loop.run_until_complete(main(asyncio_loop))




