


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
import yfinance as yf



def f_import_ipc(ticker):

    ipc = pd.DataFrame(yf.Ticker(ticker).history(start="2019-04-30", end="2021-04-30", interval= "1wk")["Close"])

    return ipc

