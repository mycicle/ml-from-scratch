import numpy as np
import black_scholes
from os import getenv
from dotenv import load_dotenv

load_dotenv()
api_key: str = getenv("API_KEY")

def load_config():
    load_dotenv()

def get_api_key():
    load_config()
    api_key = getenv("API_KEY")

def get_risk_free_rate():
    return 0.05

def calc_time_to_expiry(expiry):
    raise NotImplemented()

async def get_current_prices(option_ticker, underlying_ticker):
    """
    This may be broken up into two functions: get_option_price, get_underying_price
    depending on the return values of the polygon api
    """
    raise NotImplemented()

def get_option_ticker(underlying_ticker, expiry, strike):
    raise NotImplemented()

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
        options_chain[idx, 1] = await get_market_price(underlying_ticker, expiry, strike, call=1, vol_quoted=vol_quoted)
    
    return options_chain

async def main():
    options_chain = await build_options_chain("SPX", "20220708", 350, 375, 5, call=1, vol_quoted=True)
    print(options_chain)