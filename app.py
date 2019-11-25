from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS
from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd
import numpy as np

from markupsafe import Markup
from Predict_HistoricData import call


app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediction')
def prediction():
    symbol= "RELIANCE"
    pred_hist_LSTM, y_test, y_pred_test_LSTM, X= call(symbol)
    print(y_pred_test_LSTM)
    
#    pred_senti_LST= 
    my_plot_div = plot([Scatter(x=X, y=y_test, name='True Value'), Scatter(x=X, y=y_pred_test_LSTM, name= 'Predicted')], output_type='div')
    return render_template('prediction.html', title='Prediction', prediction=prediction, graph=Markup(my_plot_div))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
