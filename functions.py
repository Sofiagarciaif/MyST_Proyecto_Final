
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
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
from datetime import timedelta
import datetime
import math as m



def escenarios_tabla():
    return pd.DataFrame(
        {
            'Escenario': [
                'A','B','C','D'
            ],
            'Regla': [
                'Actual >= Consensus >= Previous','Actual >= Consensus < Previous',
                'Actual < Consensus >= Previous',
                'Actual <Consensus < Previous'
            ],
            'Posicion': ['venta','venta','compra','compra'
            ],
            'Take profit (pips)': [
                20,20,10,10
            ],
            'Stop loss (pips)': [
                10,10,5,5
            ],
            'Capital (USD)': [
                1000,900,800,800
            ]

        }
    ).set_index('Escenario')


def f_escenario(data):

    data['Escenario'] = None

    for i in range(len(data)):
        if data.iloc[i, 0] >= data.iloc[i, 1] and data.iloc[i, 1] >= data.iloc[i, 2]:
            data.iloc[i, 3] = 'A'

        elif data.iloc[i, 0] >= data.iloc[i, 1] and data.iloc[i, 1] < data.iloc[i,2]:
            data.iloc[i, 3] = 'B'

        elif data.iloc[i, 0] < data.iloc[i, 1] and data.iloc[i, 1] >= data.iloc[i,2]:
            data.iloc[i, 3] = 'C'

        elif data.iloc[i, 0] < data.iloc[i, 1] and data.iloc[i, 1] < data.iloc[i,2]:
            data.iloc[i, 3] = 'D'

    return data


def operacion(p_inicial, p_final, p_max, p_min, tipo, t_profit, s_loss, fecha_hora):

    if tipo=='compra':
        tp = p_inicial + t_profit/10000
        sl = p_inicial - s_loss/10000
    else:
        tp = p_inicial - t_profit / 10000
        sl = p_inicial + s_loss / 10000


    table = pd.DataFrame(
        {'Concepto':['DateTime', 'Ventana', 'Precio inicial','Precio Final', 'Precio Max', 'Precio Min',
                     'Stop loss', 'Take profit', 'Volumen','Capital', 'Posicion'],
         'Valor':[fecha_hora, '30 min', p_inicial, p_final, p_max, p_min,
                  sl, tp, int(1000/p_inicial),'1000 USD', tipo],
        }
    )

    return table


def f_metricas(indicador,precios_gbp_usd):    
    date_time = []
    for i in indicador.index:
        date_time.append(datetime.datetime.fromtimestamp(datetime.datetime.timestamp(i)))

    tiempos = []
    for i in date_time:
        for j in range(1,62):
            tiempos.append(i - datetime.timedelta(minutes=31) + datetime.timedelta(minutes=j))

    df_filtrado_por_indicador = pd.concat([precios_gbp_usd[precios_gbp_usd.index == str(i)] for i in tiempos])

    direccion = []
    iterador_t_0 = list(range(-31, len(df_filtrado_por_indicador), 61))
    iterador_t_0.pop(0);
    iterador_t_30 = list(range(-1, len(df_filtrado_por_indicador), 61))
    iterador_t_30.pop(0);
    
    #(Dirección) Close (t_30) - Open(t_0)

    for i in iterador_t_0:  
        t_0 = df_filtrado_por_indicador.iloc[i, 0]
        for j in iterador_t_30:
            t_30 = df_filtrado_por_indicador.iloc[j, 3]
        direccion.append(t_30 - t_0)
    
    uno_y_menos_uno = []
    
    for i in direccion:
        if i > 0:
            uno_y_menos_uno.append(1)
        if i < 0:
            uno_y_menos_uno.append(-1)

    indicador["Direccion"] = uno_y_menos_uno
    
    #(Pips Alcistas) High(t_0 : t_30) – Open(t_0)
    
    high_hasta_t_30 = []
    for i in iterador_t_0: 
        high_hasta_t_30.append(max(df_filtrado_por_indicador.iloc[i: i + 31,1]))

    pips_alcistas = []
    for i in iterador_t_0:
        t_0 = df_filtrado_por_indicador.iloc[i, 0]
        for j in high_hasta_t_30:
            t_max = j
        pips_alcistas.append(t_max - t_0)
        
    indicador["Pips Alcistas"] = pips_alcistas
    indicador["Pips Alcistas"] = [m.floor(abs(i* 1000)) for i in  indicador["Pips Alcistas"]]
    
    #(Pips Bajistas) Open(t_0) – Low(t_0 : t_30) 
    
    low_hasta_t_30 = []
    for i in iterador_t_0: 
        low_hasta_t_30.append(min(df_filtrado_por_indicador.iloc[i: i + 31,1]))

    pips_bajistas = []
    for i in iterador_t_0:
        t_0 = df_filtrado_por_indicador.iloc[i, 0]
        for j in low_hasta_t_30:
            t_min = j
        pips_bajistas.append(t_0 - t_min)
        
    indicador["Pips Bajistas"] = pips_bajistas
    indicador["Pips Bajistas"] = [m.floor(abs(i* 1000)) for i in  indicador["Pips Bajistas"]]
    
    #(Volatilidad) High(t_-30 : t_30) ,  - mínimo low (t_-30:t_30)
    
    high_hasta_t_30_2 = []
    for i in iterador_t_0: 
        high_hasta_t_30_2.append(max(df_filtrado_por_indicador.iloc[i - 30: i + 31, 1]))
        
    low_hasta_t_30_2 = []
    for i in iterador_t_0: 
        low_hasta_t_30_2.append(min(df_filtrado_por_indicador.iloc[i - 30: i + 31, 2]))

    indicador["Volatilidad"] = [high_hasta_t_30_2[i] - low_hasta_t_30_2[i] for i in range(0, len(high_hasta_t_30))]
    indicador["Volatilidad"] = [m.floor(abs(i* 1000)) for i in  indicador["Volatilidad"]]
     
    return indicador



