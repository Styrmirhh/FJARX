import numpy as np
import matplotlib.pyplot as plt
import cvxopt as opt
from cvxopt import blas, solvers
import pandas as pd

import pandas as pd
import numpy as np 

#taka commentið hér út til að sækja gögnin líka
#_________________________________________
#import bondscrapetest 


# Turn off progress printing 
solvers.options['show_progress'] = False

def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.randn(n)
    return k / sum(k)

def random_portfolio(returns, C):
    ''' 
    Returns the mean and standard deviation of returns for a random portfolio
    '''

    p = np.asmatrix(np.mean(returns, axis=0))
    w = np.asmatrix(rand_weights(returns.shape[1]))
    
    mu = w * p.T
    sigma = np.sqrt(np.dot(np.dot(w,C),w.T))
    # This recursion reduces outliers to keep plots pretty
    if sigma > 2:
        return random_portfolio(returns, C)
    return mu, sigma


