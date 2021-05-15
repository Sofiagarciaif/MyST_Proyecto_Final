
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
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import statsmodels.api as sm
from pylab import rcParams
from scipy.stats import shapiro
from statsmodels.tsa.stattools import adfuller
import plotly.graph_objects as go


def f_grafica_hist(pmi):
    
    pmi.plot(figsize=(10,5));
    plt.ylabel("Puntos PMI");
    plt.title("Histórico PMI");
    
    return plt.show()


def f_autocorr(pmi):
    
    a = plot_acf(pmi);
    b = plot_pacf(pmi);
    
    return(a,b)

def f_dist_normal(pmi):
    
    stat, p = shapiro(pmi)
    
    alpha = 0.05
    if p > alpha:
        pv=print('Es normal')
    else:
        pv= print('No es normal')
    
    return(pv)
    
def f_estacionalidad(pmi):
    rcParams['figure.figsize'] = 16, 6
    decomposition = sm.tsa.seasonal_decompose(pmi, model='additive', period=12)
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


def f_atipicos(pmi):
    
    plt.boxplot(pmi)
    plt.title("Detección de Atípicos")
    
    return plt.show()


def reglin(x,y):
    x = sm.add_constant(x)
    model = sm.OLS(y,x).fit()
    B0 = model.params[0]
    B1 = model.params[1]
    x = x[:, 1]
    
    x2 = np.linspace(x.min(), x.max(),100)
    y_hat = x2 * B1 + B0
    plt.scatter(x, y, alpha=1)
    plt.plot(x2, y_hat, "r", alpha=1)
    plt.xlabel("Tiempo")
    plt.ylabel("PMI")
    return model, B0, B1


def reglinshow(pmi):
    
    plt.figure(figsize=(10,5))
    pmi.reset_index(inplace=True)
    reglin(pmi.index, pmi["Actual"])
    pmi.set_index("Fecha y hora", inplace=True)
    plt.title("Regresión lineal");
    
    return plt.show()


def residuosreg(pmi):
    
    plt.figure(figsize=(10,5))
    plt.title("Gráfica de residuos")
    pmi.reset_index(inplace=True)
    modelo, B0, B1 = reglin(pmi.index, pmi["Actual"])
    residuales = modelo.resid
    plt.errorbar(pmi.index, pmi["Actual"], xerr=0, yerr=[residuales, 0*residuales], linestyle = "None", color = "Green")
    pmi.set_index("Fecha y hora", inplace=True)
    
    return plt.show()


def f_graph_train(df_backtest_train,df_backtest_optimo_train):
    fig = go.Figure()
    df_backtest_train = df_backtest_train.reset_index()
    capital = df_backtest_train['Capital_acumulado']
    date = df_backtest_train['Fecha y hora']
    
    fig.add_trace(go.Scatter(x=date, y=capital, line_shape="linear", mode='lines', name='backtest no optimizado',
                             line=dict(color='blue')
                             ))
    capital_opt = df_backtest_optimo_train['Capital_acumulado']
    fig.add_trace(go.Scatter(x=date, y=capital_opt, line_shape="linear", mode='lines', name='backtest optimizado',
                             line=dict(color='black')
                             ))
    fig.show()


def f_graph_test(df_backtest_test,df_backtest_optimo_test):
    fig = go.Figure()
    capital = df_backtest_test['Capital_acumulado']
    date = df_backtest_test['Capital_acumulado']
    fig.add_trace(go.Scatter(x=date, y=capital, line_shape="linear", mode='lines', name='backtest prueba no optimizado',
                             line=dict(color='blue')
                             ))
    capital_opt = df_backtest_optimo_test['Capital_acumulado']
    fig.add_trace(go.Scatter(x=date, y=capital_opt, line_shape="linear", mode='lines', name='backtest prueba optimizado',
                             line=dict(color='black')
                             ))
    fig.show()







