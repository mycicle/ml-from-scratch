import aiohttp
import asyncio
import os
import numpy


"""
This needs to be rewritten
"""


async def main(): 
    url = "https://api.polygon.io/v2/aggs/ticker/O:TSLA210903C00700000/range/1/day/2021-07-22/2021-07-22?apiKey="
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)
            print(await resp.text())

class BlackModel():
    def __init__(market_price, option_type):
        raise NotImplemented()

    def calc_black_price(self, iv):
        raise NotImplemented()

    def calc_derivative_black_price(self, iv):
        raise NotImplemented()

    def get_iv(self, tol, iv0 = 0.25, max_iter = 1000):
        iv_new = iv0
        iv_old = iv_new - 1
        i = 0
        while (iv_new - iv_old) > tol and i < max_iter:
            iv_old = iv_new
            iv_new = iv_old - (self.calc_black_price(iv_old) - self.market_price) / self.calc_derivative_black_price(iv_old)
            i += 1
        return iv_new
        



class OptionChain():
    def __init__(underlying_ticker, increment, lower, upper, expiry):
        self.underlying_ticker = underlying_ticker
        self.increment = increment
        self.lower = lower
        self.upper = upper
        self.expiry = expiry
        self.strikes = [x for x in range(lower, upper+1, increment)]
        self.option_tickers = [self.get_option_ticker(strike, ) for strike in ]
    
    def get_chain(use_black_vol: bool):
        """
        Returns an options chain
        if use_black_vol then return [strike, bv]
        else then return [strike, px]
        """
        for strike in strikes:
            ticker = self.get_option_ticker()
        raise NotImplemented()

if __name__ == "__main__":
    asyncio.run(main())
