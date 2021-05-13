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
    
    pmi["Hora"] = [datetime.datetime.combine(pmi.index[i], pmi["Hora"][i]) for i in range(0, len(pmi.index))]
    pmi.rename(columns = {"Hora": "Fecha y hora"}, inplace=True)
    pmi.set_index("Fecha y hora", inplace=True)
    pmi.drop(pmi.index[0], inplace=True)
    A= pmi.drop(['Unnamed: 5'], axis=1)
    
    return A



def f_import_precios():

    gbp_usd_2019 = pd.read_csv("files/DAT_MT_GBPUSD_M1_2019.csv")
    gbp_usd_2020 = pd.read_csv("files/DAT_MT_GBPUSD_M1_2020.csv")
    gbp_usd_2021_e = pd.read_excel("files/DAT_XLSX_GBPUSD_M1_202101.xlsx")
    gbp_usd_2021_f = pd.read_excel("files/DAT_XLSX_GBPUSD_M1_202102.xlsx")
    gbp_usd_2021_m = pd.read_excel("files/DAT_XLSX_GBPUSD_M1_202103.xlsx")
    gbp_usd_2021_a = pd.read_excel("files/DAT_XLSX_GBPUSD_M1_202104.xlsx")
    
    temp = [gbp_usd_2019["Fecha"][i].replace(".","-") for i in range(0, len(gbp_usd_2019["Fecha"]))]
    fecha_2019 = [datetime.datetime.strptime(temp[i], "%Y-%m-%d") for i in range(0, len(temp))]
    
    hours_2019 = []
    for i in gbp_usd_2019["Hora"]:
        if isinstance(i,datetime.time):
            hours_2019.append(i)
        else:
            hours_2019.append(datetime.datetime.strptime(i.strip(), '%H:%M').time())
            
    gbp_usd_2019["Fecha"] = fecha_2019
    gbp_usd_2019["Hora"] = hours_2019
    
    temp = [gbp_usd_2020["Fecha"][i].replace(".","-") for i in range(0, len(gbp_usd_2020["Fecha"]))]
    fecha_2020 = [datetime.datetime.strptime(temp[i], "%Y-%m-%d") for i in range(0, len(temp))]
    
    hours_2020 = []
    for i in gbp_usd_2020["Hora"]:
        if isinstance(i,datetime.time):
            hours_2020.append(i)
        else:
            hours_2020.append(datetime.datetime.strptime(i.strip(), '%H:%M').time())
            
    gbp_usd_2020["Fecha"] = fecha_2020
    gbp_usd_2020["Hora"] = hours_2020
    
    fechayhora_2019 = [datetime.datetime.combine(gbp_usd_2019["Fecha"][i], gbp_usd_2019["Hora"][i]) for i in range(0, len(gbp_usd_2019["Fecha"]))]
    gbp_usd_2019["Fecha"] = fechayhora_2019
    gbp_usd_2019.drop(["Hora"], axis=1, inplace=True)
    gbp_usd_2019.rename(columns={"Fecha": "Fecha y hora"}, inplace=True)
    
    fechayhora_2020 = [datetime.datetime.combine(gbp_usd_2020["Fecha"][i], gbp_usd_2020["Hora"][i]) for i in range(0, len(gbp_usd_2020["Fecha"]))]
    gbp_usd_2020["Fecha"] = fechayhora_2020
    gbp_usd_2020.drop(["Hora"], axis=1, inplace=True)
    gbp_usd_2020.rename(columns={"Fecha": "Fecha y hora"}, inplace=True)
    
    frames = [gbp_usd_2019, gbp_usd_2020, gbp_usd_2021_e, gbp_usd_2021_f, gbp_usd_2021_m, gbp_usd_2021_a]
    precios_gbp_usd = pd.concat(frames)
    precios_gbp_usd.set_index("Fecha y hora", inplace=True)

    return precios_gbp_usd









