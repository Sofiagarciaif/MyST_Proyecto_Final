
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import statsmodels.api as sm
from pylab import rcParams
from scipy.stats import shapiro
from statsmodels.tsa.stattools import adfuller


def f_grafica_hist(ipc):
    
    ipc.plot(figsize=(10,5));
    plt.ylabel("Puntos IPC");
    plt.title("Histórico IPC");
    
    return plt.show()

def f_autocorr(ipc):
    
    a = plot_acf(ipc);
    b = plot_pacf(ipc);
    
    return(a,b)

def f_dist_normal(ipc):
    
    stat, p = shapiro(ipc)
    
    alpha = 0.05
    if p > alpha:
        pv=print('Es normal')
    else:
        pv= print('No es normal')
    
    return(pv)
    
def f_estacionalidad(ipc):
    rcParams['figure.figsize'] = 16, 6
    decomposition = sm.tsa.seasonal_decompose(ipc, model='additive', period=5)
    decomposition.plot()

    return plt.show()


def f_estacionariedad(serie_de_tiempo):
    
    ## Test de DICKEY-FULLER
    adf_test = adfuller(serie_de_tiempo)
    if adf_test[1] > 0.05:
        test= print("No es estacionaria")
    else:
        test= print("Es estacionaria")
     
    return test



