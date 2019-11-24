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

    call()
    my_plot_div = plot([Scatter(x=X, y=Y, name='True Value'), Scatter(x=X, y=Y, name= 'Predicted')], output_type='div')
    return render_template('prediction.html', title='Intel', prediction=prediction, graph=Markup(my_plot_div))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
