import asyncio
import time
import numpy as np
import black_scholes
from typing import cast
from os import getenv
from datetime import datetime
from dotenv import load_dotenv
from polygon import RESTClient
from urllib3 import HTTPResponse

def load_config():
    load_dotenv()

def get_api_key():
    load_config()
    return getenv("API_KEY")

def get_risk_free_rate():
    return 0.05

def calc_time_to_expiry(expiry):
    raise NotImplemented()

async def get_current_prices(option_ticker, underlying_ticker):
    """
    This may be broken up into two functions: get_option_price, get_underying_price
    depending on the return values of the polygon api
    """
    now = round(time.time() * 1000)
    one_minute_ago = round(now - 1000)
    client = RESTClient(get_api_key())
    option_aggs = cast(HTTPResponse, 
                        client.get_aggs(
                            option_ticker,
                            1,
                            "minute",
                            str(one_minute_ago), 
                            str(now), 
                            raw=True
                        ))
    print(option_aggs.geturl())
    print(option_aggs.status)
    print(option_aggs.data)
    return option_aggs

def get_option_ticker(underlying_ticker, expiry, strike, call=1):
    strike_string = str(float(strike))
    [dollars_string, cents_string] = strike_string.split('.')

    while len(cents_string) < 3:
        cents_string += '0'
    while len(dollars_string) < 5:
        dollars_string = '0' + dollars_string
    
    type_string = 'C' if call else 'P'

    return "O:" + underlying_ticker.upper() + datetime.strftime(expiry, '%y%m%d') + type_string + dollars_string + cents_string


async def get_market_price(underlying_ticker, expiry, strike, call=1, vol_quoted=False):
    option_ticker = get_option_ticker(underlying_ticker, expiry, strike)
    market_price, underlying_price = await get_current_prices(option_ticker, underlying_ticker)

    if vol_quoted:
        r = get_risk_free_rate()
        t = calc_time_to_expiry(expiry)
        return black_scholes.calc_iv(underlying_price, strike, r, t, market_price, call=call)
    else:
        return market_price

async def build_options_chain(underlying_ticker, expiry, lower, upper, increment, call=1, vol_quoted=False):
    strikes = [x for x in range(lower, upper, increment)]
    options_chain = np.empty((len(strikes), 2))

    for idx, strike in enumerate(strikes):
        options_chain[idx, 0] = strike
        options_chain[idx, 1] = await get_market_price(underlying_ticker, expiry, strike, call=call, vol_quoted=vol_quoted)
    
    return options_chain

async def main():
    # load_config()
    # options_chain = await build_options_chain("SPX", "20220708", 350, 375, 5, call=1, vol_quoted=True)
    # print(options_chain)
    # print(get_option_ticker("F", datetime(2021, 11, 19), 14, call=0))
    underlying_ticker = "SPX"
    option_ticker = get_option_ticker(underlying_ticker, datetime(2022, 7, 10), 400)
    a = await get_current_prices(option_ticker, underlying_ticker)

if __name__ == "__main__":
    asyncio.run(main())