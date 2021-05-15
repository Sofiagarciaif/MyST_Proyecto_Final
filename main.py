
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import numpy as np
import data as dt
import functions as fn
import visualizations as vs
from pyswarms.utils.plotters import (plot_cost_history, plot_contour, plot_surface)
import matplotlib.pyplot as plt

PMI = dt.f_import_pmi()

HIST= vs.f_grafica_hist(PMI)

PRECIOSGBP = dt.f_import_precios()

vs.f_grafica_hist(PMI)

vs.f_autocorr(PMI["Actual"])

vs.reglinshow(PMI)

vs.residuosreg(PMI)

vs.f_dist_normal(PMI["Actual"])

vs.f_estacionalidad(PMI["Actual"])

vs.f_estacionariedad(PMI["Actual"])

vs.f_atipicos(PMI["Actual"])

data = fn.f_escenario(PMI)

metrica=fn.f_metricas(PMI,PRECIOSGBP)

capital_inicial = 100000

escenario = fn.f_escenarios(PMI)

Operacion= ['Venta', 'Compra', 'Venta','Compra']

SL, TP = [10, 10, 10, 10] , [20, 20, 20, 20]

Volumen= [200, 200, 200, 200]

decision = fn.f_decisiones(Operacion, SL,TP,Volumen)

backtest_train = fn.f_backtest(escenario,decision,capital_inicial)

miniback=fn.f_minimizar(backtest_train)

lb= [3,3,1,1,8,8,3,3,100000,100000,50000,50000]

ub= [10,10,3,3,20,20,6,6,500000,500000,200000,200000]

cost, df_decisiones_optimo, graph= fn.f_optimizacion(escenario,np.array(lb),np.array(ub),Operacion)

graph = plot_cost_history(cost_history=graph.cost_history)

df_backtest_optimo_train = fn.f_backtest(escenario, df_decisiones_optimo,capital_inicial)

df_escenarios_test =fn.f_escenarios_test(escenario)

df_backtest_test = fn.f_backtest(df_escenarios_test,decision,capital_inicial)

df_backtest_optimo_test= fn.f_backtest(df_escenarios_test, df_decisiones_optimo,capital_inicial)

vs.f_graph_train(backtest_train,df_backtest_optimo_train)

vs.f_graph_test(df_backtest_test,df_backtest_optimo_test)

