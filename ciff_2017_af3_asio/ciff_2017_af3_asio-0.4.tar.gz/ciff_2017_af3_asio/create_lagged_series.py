def create_lagged_series(symbol, start_date, end_date, lags=50,outcome_period=5):
    """This creates a pandas DataFrame that stores the percentage returns of the
    adjusted closing value of a stock obtained from Yahoo Finance, along with
    a number of lagged returns from the prior trading days (lags defaults to 5 days).
    Trading volume, as well as the Direction from the previous day, are also included."""

    # Obtain stock information from Yahoo Finance
#    symbol = "tef.mc"
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
    ts = DataReader(symbol, "google", start_date-datetime.timedelta(days=2*(lags+outcome_period)), end_date)

    # Create the new lagged DataFrame
    tslag = pd.DataFrame(index=ts.index)
    tslag["Today"] = ts["Close"]
    tslag["Volume"] = ts["Volume"]

    # Create the shifted lag series of prior trading period close values
    for i in xrange(0,lags):
        tslag["Lag%s" % str(i+1)] = ts["Close"].shift(i+1)

    # Create the returns DataFrame
    tsret = pd.DataFrame(index=tslag.index)
    tsret["Volume"] = tslag["Volume"]
    tsret["Today"] = tslag["Today"].pct_change()*100.0

    # If any of the values of percentage returns equal zero, set them to
    # a small number (stops issues with QDA model in scikit-learn)
    for i,x in enumerate(tsret["Today"]):
        if (abs(x) < 0.0001):
            tsret["Today"][i] = 0.0001

    # Create the lagged percentage returns columns
    for i in xrange(0,lags):
        tsret["Lag%s" % str(i+1)] = tslag["Lag%s" % str(i+1)].pct_change()*100.0

    # Create the "Direction" column (+1 or -1) indicating an up/down day
#    tsret["Direction"] = np.sign(tstsret["Today"]))

    tsret["Direction"] = np.sign(ts["Close"] - ts["Close"].shift(outcome_period))

    tsret = tsret[tsret.index >= start_date]
    return tsret
