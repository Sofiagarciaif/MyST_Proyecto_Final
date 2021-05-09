"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import datetime as datetime


def Replace(str1):
    maketrans = str1.maketrans
    final = str1.translate(maketrans(',.', '.,', ' '))
    return final.replace(',', ", ")


def f_import_pmi():

    pmi = pd.read_excel("Indice PMI sector servicios GBP.xlsx")
    actual = [float(Replace(pmi["Actual"][i])) for i in range(0, len(pmi["Actual"]))]
    prevision = [float(Replace(pmi["Prevision"][i])) for i in range(0, len(pmi["Prevision"]))]
    anterior = [float(Replace(pmi["Anterior"][i])) for i in range(0, len(pmi["Anterior"]))]
    temp = [pmi["Fecha de publicacion"][i].replace(".","-") for i in range(0, len(pmi["Fecha de publicacion"]))]
    temp = ["{2}-{1}-{0}".format(*temp[i].split('-')) for i in range(0,len(temp))]
    fecha = [datetime.datetime.strptime(temp[i], "%Y-%m-%d") for i in range(0, len(temp))]
    
    hours = []
    for i in pmi["Hora"]:
        if isinstance(i,datetime.time):
            hours.append(i)
        else:
            hours.append(datetime.datetime.strptime(i.strip(), '%H:%M').time())
    
    pmi["Actual"] = actual
    pmi["Prevision"] = prevision
    pmi["Anterior"] = anterior
    pmi["Fecha de publicacion"] = fecha
    pmi["Hora"] = hours
    pmi.set_index("Fecha de publicacion", inplace=True);

    return pmi




