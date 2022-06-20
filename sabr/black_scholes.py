from scipy.stats import norm
import math
import numpy as np

def get_Z_value(x, mu, sig):
    return (x - mu) / sig

def calc_d1(S, K, r, t, sig):
    return (np.log(S/K) + (r + sig**2/2) * t) / (sig * math.sqrt(t))

def calc_d2(d1, t, sig):
    return d1 - sig*math.sqrt(t)

def calc_black_price(S, K, r, t, sig):
    d1 = calc_d1(S, K, r, t, sig)
    d2 = calc_d2(d1, t, sig)
    n_d1 = norm.cdf(get_Z_value(d1, S, sig))
    n_d2 = norm.cdf(get_Z_value(d2, S, sig))
    
    return n_d1 * S - n_d2 * K * math.exp(-r*t)

def calc_call_black_price_derivative():
    raise NotImplemented()

def calc_put_black_price_derivative():
    raise NotImplemented()

def calc_iv():
    raise NotImplemented()


def main():
    S = 100
    K = 105
    r = 0.05
    t = 10
    sig = 25

    C = calc_black_price(S, K, r, t, sig)
    print(C)

    Z = get_Z_value(K, S, sig)
    print(Z)

    D1 = calc_d1(S, K, r, t, sig)
    print(D1)

    D2 = calc_d2(D1, t, sig)
    print(D2)


if __name__ == "__main__":
    main()