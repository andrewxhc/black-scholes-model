import math
from scipy.stats import norm


def black_scholes_merton(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Black-Scholes-Merton price for European options.
    
    Parameters:
        S (float): Current stock price
        K (float): Option strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate (annualized)
        sigma (float): Volatility of the stock (annualized)
        option_type (str): "call" for call option, "put" for put option
    
    Returns:
        float: Option price
    """
    d1 = (math.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return price
