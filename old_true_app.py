from dash import Dash
import plotly.express as px
import pandas as pd
import numpy as np
import requests
import json
from dash import html, dcc
from dash.dependencies import Input, Output


#Query dataset dal progetto con l'indirizzo corretto

#Sistemiamo il dataset
r = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0f4sd5j08r022pnj5t7fx3d/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")

data = r.text

data = json.loads(data)
data = data['features']
input_data = pd.DataFrame(columns=['lat','lon','name','media'])

for i in data:
    row = dict.fromkeys(['lat','lon'])
    row['lat'] = i['geometry']['coordinates'][1]
    row['lon'] = i['geometry']['coordinates'][0]
    input_data = input_data.append(row,ignore_index=True)

input_data['name'] = 'Punto 1'
input_data['media'] = 'LINKPROVA'


fig = px.scatter_mapbox(input_data, lat="lat", lon="lon",
                        hover_name="name",
                        hover_data={"media":True,
                                    "lat":False,
                                    "lon":False
                                    },
                        color_discrete_sequence=["green"],
                        zoom=11,
                        height=300)

fig.update_mapboxes(style="mapbox://styles/federicogodino/ckziqrfug006i14nyovs0ee76",accesstoken="pk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6Y3hyazgwMjNvejJvbnh0ZXptbTJkbSJ9.HBsPU_tmnC_VbsAK4FA1XQ")
fig.update_layout(clickmode='event+select')

#fig.update_layout(margin={"r":.5,"t":0.5,"l":0.5,"b":0.5})



app = Dash(__name__)
server = app.server


app.layout = html.Div([
    dcc.Graph(
              id='basic-interactions',
              figure=fig),

    html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data'),
        ], className='three columns'),

html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data'),
        ], className='three columns'),

])

#TODO : mettergli il risultato di instaloader

@app.callback(
    Output("click-data", "children"),
    Input('basic-interactions', 'clickData'))

def display_click_data(clickData):
    return 'PORCO DIO OVINO'


if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)

