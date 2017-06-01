def oportunidaddesubida(ndiasmaximo,shortticker):
    from flask import Flask, request, render_template, jsonify
    import pandas.io.sql as sql
    import sqlite3
    import platform
    import datetime
    import numpy as np
    import pandas as pd
    import json
    #import pygal
    import matplotlib.pyplot as plt
    from scipy.stats import norm
    from bokeh.charts import Histogram
    import plotly
    
    #from pandas.io.data import DataReader
    from pandas_datareader import wb, DataReader
    from sklearn.linear_model import LogisticRegression
    from sklearn.lda import LDA
    from sklearn.qda import QDA
    
    from bokeh.layouts import gridplot
    from bokeh.plotting import figure, show, output_file
    symbol = shortticker
    historical_period_in_days = 365#*2
    start_date = datetime.datetime.today() - datetime.timedelta(days=historical_period_in_days)
    end_date = datetime.datetime.today()
    #start_date = datetime.datetime(2015,01,01)
    #end_date = datetime.datetime(2016,01,01)
    lags = int(ndiasmaximo)
    outcome_period = 5
    #def create_lagged_series(symbol, start_date, end_date, lags=50, outcome_period=5):
    """This creates a pandas DataFrame that stores the percentage returns of the
    adjusted closing value of a stock obtained from Yahoo Finance, along with
    a number of lagged returns from the prior trading days (lags defaults to 5 days).
    Trading volume, as well as the Direction from the previous day, are also included."""

    # Obtain stock information from Yahoo Finance
    ts = DataReader(symbol, "google", start_date-datetime.timedelta(days=2*(lags+outcome_period)), end_date)
    #ts = web.DataReader(symbol, 'google', start_date, end_date)

    ## Create the new lagged DataFrame
    tslag = pd.DataFrame(index=ts.index)
    tslag = ts[['Low', 'High']]

    tslag=tslag.sort_index(axis=0, ascending=False)
    for i in xrange(0,lags):
        tslag["lag%s" % str(i+1)] = (tslag["High"] - tslag["Low"].shift(-(i+1)))/tslag["Low"].shift(-(i+1))
    tslag = tslag[(tslag.index >= start_date) & (tslag.index<=end_date)]
    result = {}
    for item in (tslag.index):
        result[str(item).split('T')[0]]=list(tslag.ix[item,2:].values)
    result2 = {}
    valores = []
    for item in result.keys():
        for j in range(lags):
            valores.append(result[item][j])
    result2['diferencias'] = valores

    ## nuevo
    rango = {}
    interval = [-0.1, -0.07, -0.05, -0.02, 0.0, 0.02, 0.05, 0.07, 0.1]
    for i in range(len(interval)+1):
        rango[str(i+1)] = []
    for i in range(len(valores)):
        if valores[i]<= -0.10:
            rango['1'].append(valores[i])
        if (valores[i] > -0.10) & (valores[i] <= -0.07):
            rango['2'].append(valores[i])
        if (valores[i] > -0.07) & (valores[i] <= -0.05):
            rango['3'].append(valores[i])
        if (valores[i] > -0.05) & (valores[i] <= -0.02):
            rango['4'].append(valores[i])
        if (valores[i] > -0.02) & (valores[i] <= 0.00):
            rango['5'].append(valores[i])
        if (valores[i] > 0.00) & (valores[i] <= 0.02):
            rango['6'].append(valores[i])
        if (valores[i] > 0.02) & (valores[i] <= 0.05):
            rango['7'].append(valores[i])
        if (valores[i] > 0.05) & (valores[i] <= 0.07):
            rango['8'].append(valores[i])
        if (valores[i] > 0.07) & (valores[i] <= 0.10):
            rango['9'].append(valores[i])
        if (valores[i] > 0.10):
            rango['10'].append(valores[i])

    rangos = []
    percen = {}
    percen['rango'] = 'x < -10%'
    try:
        percen['percentual'] = (round((float(len(rango['1']))/len(valores)),4))
    except:
        percen['percentual'] = (0.0)
    rangos.append(percen)

    for i in range(1,len(interval),1):
        percen = {}
        percen['rango'] = str(interval[i-1]*10)+'% ' + '<= x < ' + str(interval[i]*10)+ '%'
        percen['percentual'] = (round((float(len(rango['%s' %(i+1)]))/len(valores)),4))
        rangos.append(percen)

    percen = {}
    percen['rango'] = 'x > 10%'
    try:
        percen['percentual'] = (round((float(len(rango['10']))/len(valores)),4))
    except:
        percen['percentual'] = (0.0)
    rangos.append(percen)
    per = {}
    per['rangos'] = rangos
    return json.dumps(per)
