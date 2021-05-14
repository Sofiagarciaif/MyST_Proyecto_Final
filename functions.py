
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
import datetime
import math as m
import pyswarms as ps


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


def f_escenarios(data):
    df_escenarios = data[['Escenario', 'Direccion', 
                          'Pips Alcistas', 'Pips Bajistas', 'Volatilidad']] 
    return df_escenarios


def f_decisiones(Operacion, SL, TP, Volumen):
    df_decisiones = pd.DataFrame(columns=['Escenario', 'Operacion', 'SL', 'TP', 'Volumen']) 
    df_decisiones['Escenario'] = ['A', 'B', 'C', 'D'] 
    df_decisiones['Operacion'] = Operacion 
    df_decisiones['SL'] = SL 
    df_decisiones['TP'] = TP 
    df_decisiones['Volumen'] = Volumen 
    return df_decisiones 


def f_backtest(df_escenarios, df_decisiones,capital_inicial):
    
    df_backtest = pd.merge(df_escenarios, df_decisiones)
    df_backtest['Resultado'] = 0
    df_backtest['Pips'] = 0
    df_backtest['Capital'] = 0
    df_backtest['Capital_acumulado'] = 0

    for i in range(len(df_backtest)):
      #PIPS  
        if df_backtest.loc[i, 'Operacion'] == 'Venta':
            if df_backtest.loc[i, 'Pips Alcistas'] >= df_backtest.loc[i, 'SL']:
                df_backtest.loc[i, 'Pips'] = df_backtest.loc[i, 'SL'] * (-1)
            elif df_backtest.loc[i, 'Pips Bajistas'] >= df_backtest.loc[i, 'TP']:
                df_backtest.loc[i, 'Pips'] = df_backtest.loc[i, 'TP']
        if df_backtest.loc[i, 'Operacion'] == 'Compra':
            if df_backtest.loc[i, 'Pips Alcistas'] >= df_backtest.loc[i, 'TP']:
                df_backtest.loc[i, 'Pips'] = df_backtest.loc[i, 'TP']
            elif df_backtest.loc[i, 'Pips Bajistas'] >= df_backtest.loc[i, 'SL']:
                df_backtest.loc[i, 'Pips'] = df_backtest.loc[i, 'SL'] * (-1)
    #RESULTADO  
        if df_backtest.loc[i, 'Pips'] >= 0:
            df_backtest.loc[i, 'Resultado'] = "Ganada"
        else:
            df_backtest.loc[i, 'Resultado'] = "Perdida"
    #CAPITAL
        df_backtest.loc[i, 'Capital'] = df_backtest.loc[i, 'Volumen'] * df_backtest.loc[i, 'Pips'] / 10000
    #CAPITAL ACUMULADO
    df_backtest.loc[0, 'Capital_acumulado'] = capital_inicial + df_backtest.loc[0, 'Capital']
    for i in range(1, len(df_backtest)):
        df_backtest.loc[i, 'Capital_acumulado'] = df_backtest.loc[i - 1, 'Capital_acumulado'] + df_backtest.loc[i, 'Capital']
        
    del df_backtest['Direccion']
    del df_backtest['Pips Alcistas']
    del df_backtest['Pips Bajistas']
    del df_backtest['Volatilidad']
    del df_backtest['SL']
    del df_backtest['TP']
    return df_backtest


def f_minimizar(df_backtest):
    maximo = max(df_backtest.Capital_acumulado)
    minimo = min(df_backtest.Capital_acumulado)
    posicion_max = df_backtest.index.get_indexer_for(df_backtest[df_backtest.Capital_acumulado == maximo].index)[0]
    posicion_min = df_backtest.index.get_indexer_for(df_backtest[df_backtest.Capital_acumulado == minimo].index)[0]

    # primero es el Drawup
    if posicion_max < posicion_min:
        # Drowdown
        drawdown_valor_inicio = df_backtest['Capital_acumulado'][posicion_max]
        drawdown_valor_fin = df_backtest['Capital_acumulado'][posicion_min]
    else:
        drawdown_valor_inicio = 100000
        drawdown_valor_fin = df_backtest['Capital_acumulado'][posicion_min]

    drawdown = drawdown_valor_fin - drawdown_valor_inicio

    return drawdown


def f_optimizacion(df_escenarios, lb, ub, operacion):
    max_bound = ub
    min_bound = lb
    bounds = (min_bound, max_bound)

    def drawdown_neg(x):
        sl = x[:4]
        tp = x[4:8]
        volumen = x[8:12]
        escenarios = f_decisiones(operacion, sl, tp, volumen)
        capital_inicial= 100000
        backtesting = f_backtest(df_escenarios, escenarios, capital_inicial)
        drawdown = f_minimizar(backtesting)

        return drawdown*-1

    options = {'c1': 5, 'c2': 3, 'w': 0.9}
    # Call instance of PSO with bounds argument
    optimizer = ps.single.GlobalBestPSO(n_particles=12, dimensions=len(ub), options=options, bounds=bounds)
    # Perform optimization
    cost, pos = optimizer.optimize(drawdown_neg, iters=100)

    operacion = ['Compra', 'Compra', 'Venta', 'Venta']
    sl = pos[:4]
    tp = pos[4:8]
    volumen = pos[8:12]

    df_decisiones_optimo = f_decisiones(operacion, sl, tp, volumen)

    return cost, df_decisiones_optimo, optimizer


def f_escenarios_test(data):
    df_escenarios_test = data
    df_escenarios_test = df_escenarios_test.iloc[12:, :]
    df_escenarios_test = df_escenarios_test.reset_index()
    return df_escenarios_test













