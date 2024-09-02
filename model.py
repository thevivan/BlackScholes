import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type):
    """
    Calculates the price of a European call or put option using the Black-Scholes model.

    Parameters:
    S (float): Current stock price
    K (float): Strike price
    T (float): Time to expiration (in years)
    r (float): Risk-free interest rate (continuously compounded)
    sigma (float): Volatility of the stock (annual standard deviation)
    option_type (str): 'call' or 'put'

    Returns:
    float: Price of the option
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Must be 'call' or 'put'.")

    return price

def generate_heatmap(S_range, sigma_range, K, T, r, option_type):
    prices = []
    for S in S_range:
        row = []
        for sigma in sigma_range:
            price = black_scholes(S, K, T, r, sigma, option_type)
            row.append(price)
        prices.append(row)

    df = pd.DataFrame(prices, index=S_range, columns=np.round(sigma_range, 2))
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df, annot=True, cmap='viridis', fmt='.2f', cbar_kws={'label': option_type.capitalize() + ' Option Price'}, ax=ax)
    ax.set_xlabel('Volatility')
    ax.set_ylabel('Spot Price')
    ax.set_title('Black-Scholes ' + option_type.capitalize() + ' Option Price Heatmap')
    
    return fig