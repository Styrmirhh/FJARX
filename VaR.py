# var.py

import datetime
from scipy.stats import norm


def var_cov_var(P, c, mu, sigma): 
    """
    Variance-Covariance calculation of daily Value-at-Risk
    using confidence level c, with mean of returns mu
    and standard deviation of returns sigma, on a portfolio
    of value P.
    """
    alpha = norm.ppf(1-c, mu, sigma)
    return P - P*(alpha + 1)

 
var=var_cov_var(10000,0.95,30,15)

print("Value-at-Risk: %s", var)