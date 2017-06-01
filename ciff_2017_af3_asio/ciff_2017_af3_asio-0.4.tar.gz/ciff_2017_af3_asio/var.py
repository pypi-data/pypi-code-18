def var(p,c,ticker):
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
    symbol = ticker
    def var_cov_var(P, c, mu, sigma):
        """
        Variance-Covariance calculation of daily Value-at-Risk
        using confidence level c, with mean of returns mu
        and standard deviation of returns sigma, on a portfolio
        of value P.
        """
        alpha = norm.ppf(1-c, mu, sigma)
        return P - P*(alpha + 1)

    #if __name__ == "__main__":
    historical_period_in_days = 365*7
    start = datetime.datetime.today() - datetime.timedelta(days=historical_period_in_days)
    end = datetime.datetime.today()

    citi = DataReader(symbol, "google", start, end)
    citi["rets"] = citi["Close"].pct_change()

    P = float(p)   # 1,000,000 USD
    c = float(c)  # 99% confidence interval
    mu = np.mean(citi["rets"])
    sigma = np.std(citi["rets"])

    varianza = var_cov_var(P, c, mu, sigma)
    #print "Value-at-Risk: $%0.2f" % varianza
    var1= {}
    var1['Value-at-Risk'] = "$%0.2f" % varianza
    return json.dumps(var1)
