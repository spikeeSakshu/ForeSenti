from flask import Flask, render_template, request, url_for, redirect
from flask_restful import Api
from flask_cors import CORS
from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd
import numpy as np

from markupsafe import Markup
from Predict_HistoricData import call
from Predict_Sentiment import call_senti

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        symbol = request.form.get('tinker')
        return redirect(url_for('prediction', symbol=symbol))
    return render_template('index.html')

@app.route('/prediction')
def prediction():
    symbol = request.args.get('symbol', None)
      
    print(symbol)

    
    pred_, y_test, y_pred_test_LSTM, X= call(symbol)
    
    
    
    y_pred_test_LSTM= y_pred_test_LSTM.flatten()
    print(y_pred_test_LSTM)
#    print('Y_test', y_test)
    
    pred_senti= call_senti(symbol)
    
    pred= (pred_senti+pred_)/2
    
    my_plot_div = plot([Scatter(x=X, y=y_test, name='True Value'), Scatter(x=X, y=y_pred_test_LSTM, name= 'Predicted')], output_type='div')
    
    return render_template('prediction.html', title='Prediction', prediction=[pred-10,pred+10], graph=Markup(my_plot_div))

      

if __name__ == '__main__':
    app.run(port=5000, debug=True)
