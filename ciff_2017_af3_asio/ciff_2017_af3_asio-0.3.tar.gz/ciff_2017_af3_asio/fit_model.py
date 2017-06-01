def fit_model(name, model, X_train, y_train, X_test, X_last, pred, pred_last):
    
    """Fits a classification model (for our purposes this is LR, LDA and QDA)
    using the training data, then makes a prediction and subsequent "hit rate"
    for the test data."""

    from flask import Flask, request, render_template, jsonify
    import pandas.io.sql as sql
    import sqlite3
    import platform
    import datetime
    import numpy as np
    import pandas as pd
    import json
    import pygal
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
    # Fit and predict the model on the training, and then test, data
    model.fit(X_train, y_train)
    pred[name] = model.predict(X_test)
    pred_last[name] = model.predict(X_last)

    # Create a series with 1 being correct direction, 0 being wrong
    # and then calculate the hit rate based on the actual direction
    pred["%s_Correct" % name] = (1.0+pred[name]*pred["Actual"])/2.0
    hit_rate = np.mean(pred["%s_Correct" % name])
    print "%s: %.3f" % (name, hit_rate)
    return hit_rate
