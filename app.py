from flask import Flask
from flask import request, url_for, render_template, redirect
import streamlit as st

app = Flask(__name__)


@app.route('/')
def mymap():  # put application's code here

    mapbox_access_token = 'pk.eyJ1IjoibWJlbGxpbmkzMyIsImEiOiJja3plbGFwOW8xeDg5Mm9vMWl6dWN2OTdkIn0.02V_6pXLh18k069kusYaQw'


    return render_template('main.html',mapbox_access_token=mapbox_access_token)


if __name__ == '__main__':
    app.run()
