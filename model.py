import numpy as np
from scipy.stats import norm

class PricingModel:
    def __init__(self, time, strike, spot, vol, rate):
        self.time = time
        self.strike = strike
        self.spot = spot
        self.vol = vol
        self.rate = rate

    def calculate(self):
        d1 = (np.log(self.spot / self.strike) + (self.rate + 0.5 * self.vol ** 2) * self.time) / (self.vol * np.sqrt(self.time))
        d2 = d1 - self.vol * np.sqrt(self.time)

        # Call and Put Prices
        self.call_price = self.spot * norm.cdf(d1) - (self.strike * np.exp(-(self.rate * self.time)) * norm.cdf(d2))
        self.put_price = (self.strike * np.exp(-(self.rate * self.time)) * norm.cdf(-d2)) - self.spot * norm.cdf(-d1)

        # Delta
        self.call_delta = norm.cdf(d1)
        self.put_delta = self.call_delta - 1

        # Gamma
        self.gamma = norm.pdf(d1) / (self.spot * self.vol * np.sqrt(self.time))

        # Theta
        self.call_theta = (-self.spot * norm.pdf(d1) * self.vol / (2 * np.sqrt(self.time)) 
                           - self.rate * self.strike * np.exp(-self.rate * self.time) * norm.cdf(d2))
        self.put_theta = (-self.spot * norm.pdf(d1) * self.vol / (2 * np.sqrt(self.time)) 
                          + self.rate * self.strike * np.exp(-self.rate * self.time) * norm.cdf(-d2))

        # Vega
        self.vega = self.spot * norm.pdf(d1) * np.sqrt(self.time)

        # Rho
        self.call_rho = self.strike * self.time * np.exp(-self.rate * self.time) * norm.cdf(d2)
        self.put_rho = -self.strike * self.time * np.exp(-self.rate * self.time) * norm.cdf(-d2)

        # Vanna
        self.vanna = self.vega * (d1 / self.vol)

        # Volga
        self.volga = self.vega * d1 * d2 / self.vol

        return self.call_price, self.put_price

