from scipy.stats import norm
import math
import numpy as np


def calc_d1(S, K, r, t, sig):
    return (np.log(S/K) + (r + sig**2/2) * t) / (sig * math.sqrt(t))

def calc_d2(d1, t, sig):
    return d1 - sig*math.sqrt(t)

def calc_black_price(S, K, r, t, sig, call=1):
    d1 = calc_d1(S, K, r, t, sig)
    d2 = calc_d2(d1, t, sig)

    if call:
        n_d1 = norm.cdf(d1)
        n_d2 = norm.cdf(d2)
        return n_d1 * S - n_d2 * K * math.exp(-r*t)
    else: 
        n_d1 = norm.cdf(-d1)
        n_d2 = norm.cdf(-d2)
        return n_d2 * K * math.exp(-r*t) - n_d1 * S

def calc_black_price_derivative(S, t, d1):
    return S * math.sqrt(t/(2*np.pi)) * math.exp(-d1**2/2)

def calc_iv(S, K, r, t, V, call=1, sig0=0.3, tolerance=0.00001, max_iter=1000):
    first_iter = True
    i = 0
    sig_new = sig0
    sig_old = sig0
    while (abs(sig_new - sig_old) > tolerance and i < max_iter) or first_iter:
        first_iter = False
        sig_old = sig_new
        d1 = calc_d1(S, K, r, t, sig_old) # doubling up on calculating d1 for development's sake
        sig_new = sig_old - (calc_black_price(S, K, r, t, sig_old, call=call) - V)/calc_black_price_derivative(S, t, d1)
        i += 1

    return sig_new

def main():
    S = 100
    K = 105
    r = 0.05
    t = 10/365
    sig = 0.25

    C = calc_black_price(S, K, r, t, sig)
    print(C)

    Put = calc_black_price(S, K, r, t, sig, call=0)
    print(Put)

    D1 = calc_d1(S, K, r, t, sig)
    print(D1)

    D2 = calc_d2(D1, t, sig)
    print(D2)

    ivc = calc_iv(S, K, r, t, C)
    print(ivc)

    ivp = calc_iv(S, K, r, t, Put, call=0)
    print(ivp)

if __name__ == "__main__":
    main()