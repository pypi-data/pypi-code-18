def grafica(shortticker):
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
    def datetime(x):
        return np.array(x, dtype=np.datetime64)

    symbol = shortticker#"GOOG"
    df = DataReader(symbol, "google", '01/01/2016', '08/03/2017')
    df['date'] = df.index


    p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line(datetime(df['date']), df['Close'], color='#A6CEE3', legend=symbol)
    #p1.line(datetime(GOOG['date']), GOOG['adj_close'], color='#B2DF8A', legend='GOOG')
    #p1.line(datetime(IBM['date']), IBM['adj_close'], color='#33A02C', legend='IBM')
    #p1.line(datetime(MSFT['date']), MSFT['adj_close'], color='#FB9A99', legend='MSFT')
    #p1.legend.location = "top_left"

    df_array = np.array(df['Close'])
    df_dates = np.array(df['date'], dtype=np.datetime64)

    window_size = 30
    window = np.ones(window_size)/float(window_size)
    aapl_avg = np.convolve(df_array, window, 'same')

    p2 = figure(x_axis_type="datetime", title="One-Month Average")
    p2.grid.grid_line_alpha = 0
    p2.xaxis.axis_label = 'Date'
    p2.yaxis.axis_label = 'Price'
    p2.ygrid.band_fill_color = "olive"
    p2.ygrid.band_fill_alpha = 0.1

    p2.circle(df_dates, df_array, size=4, legend='close',
              color='darkgrey', alpha=0.2)

    p2.line(df_dates, aapl_avg, legend='avg', color='navy')
    p2.legend.location = "top_left"

    output_file("./templates/stocks.html", title="My Own Bokeh Example")
    show(gridplot([[p1,p2]], plot_width=400, plot_height=400))  # open a browser
    return render_template('stocks.html')
