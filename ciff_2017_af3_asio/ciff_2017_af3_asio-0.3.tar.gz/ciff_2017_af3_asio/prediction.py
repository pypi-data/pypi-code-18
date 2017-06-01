def prediction(period,ticker):
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
    from ciff_2017_af3_asio import create_lagged_series
#    global models
    
    results =  {"TICKER":'ticker no found',"predictedprice5daysfromnow":'',"myactionrecommendaction":''}


    try:
#    ticker = "pop.mc"
#    ticker = "tef.mc"
        results =  {"TICKER":ticker,"PREDICTION_FINAL_TXT": "Error: no he podido predecir que va a pasar con la accion "+ticker}

        historical_period_in_days = 365*2
        start_date = datetime.datetime.today()-datetime.timedelta(days=historical_period_in_days)
        end_date = datetime.datetime.today()
        start_test = datetime.datetime.today()-datetime.timedelta(days=int(historical_period_in_days/2))
        n_lags=50
        n_outcome_period=int(period)
        snpret = create_lagged_series(ticker, start_date, end_date, lags=n_lags, outcome_period=n_outcome_period)


        # Drop 4 previous days, to use the prior days (from 5...to the past) of returns as predictor values, with direction as the response
        X = snpret.drop(['Volume','Today','Lag1','Lag2','Lag3','Lag4'], axis=1)
        y = snpret["Direction"]

        #
        X_last = snpret.tail(1)
#        print X_last
        for i in range(n_lags,n_outcome_period,-1):
            X_last["Lag%s" % str(i)] = X_last["Lag%s" % str(i-n_outcome_period)]
#        print X_last
        X_last = X_last.drop(['Volume','Today','Lag1','Lag2','Lag3','Lag4'], axis=1)

        # The test data is split into two parts: Before and after 1st Jan 2005.

        # Create training and test sets
        X_train = X[X.index < start_test]
        X_test = X[X.index >= start_test]
        y_train = y[y.index < start_test]
        y_test = y[y.index >= start_test]

        # Create prediction DataFrame
        pred = pd.DataFrame(index=y_test.index)
        pred["Actual"] = y_test

        pred_last = pd.DataFrame(index=X_last.index)

        # Create and fit the three models
#        print "Hit Rates:"
        models = [("LR - Logistic Regression", LogisticRegression()), ("LDA - Linear Discriminant Analysis", LDA()), ("QDA - Quadratic Discriminant Analysis", QDA())]

        results["PREDICTION_FINAL_NUM"]  = 0
        for m in models:
            try:
                print "1.0"
                results["MODEL_"+m[0]]=fit_model(m[0], m[1], X_train, y_train, X_test, X_last, pred, pred_last)
                if results["MODEL_"+m[0]] != -1.0:
                    print "1.1"
                    results["PREDICTION_MODEL_"+m[0]] = pred_last[m[0]][0]
                    print "1.2"
                    results["PREDICTION_FINAL_NUM"] += pred_last[m[0]][0]
                    print "1.3"
                else:
                    results["PREDICTION_MODEL_"+m[0]] = 0
            except:
                results["PREDICTION_MODEL_"+m[0]] = 0

        print "2.0"
        if results["PREDICTION_FINAL_NUM"] > 0:
            results["PREDICTION_FINAL_TXT"] = "La accion "+str(ticker)+ " va subir en los proximo "+ str(n_outcome_period) +" dias"
        else:
            results["PREDICTION_FINAL_TXT"] = "La accion "+str(ticker)+ " va bajar en los proximo "+ str(n_outcome_period) +" dias"
        print "3.0"

    except:
        print "ERROR!"
    #return jsonify(results)
    return json.dumps(results)
