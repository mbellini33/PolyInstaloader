from dash import Dash, dcc, html, Input, Output,dash_table
from data_processing import data_process
import requests
import json
import pandas as pd
import plotly.express as px
import warnings
import re
import dash_bootstrap_components as dbc
from instagrapi import Client
import instagrapi
warnings.filterwarnings('ignore')
from plotly.subplots import make_subplots

from PIL import Image
import numpy as np
import plotly.graph_objects as go



#DATA
r_heri = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0f4sd5j08r022pnj5t7fx3d/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_cult = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0mygcb505jv22s95tj8jab1/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_inn = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0med4ux01h521p8liyzzlqf/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_h2o = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/ckzokywth2wzo2dte61czaktb/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_hous = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0f5p20u0m2e20qum84o85l8/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_space = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0p7q5nk13c621r03a8kdmu7/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_natur = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0p83jhb030r28st8jaklulv/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")

input_data = pd.DataFrame(columns=['lat','lon','name','categoria','link','ambito','size'])

input_data = data_process(r_heri,input_data)
input_data = data_process(r_cult,input_data)
input_data = data_process(r_inn,input_data)
input_data = data_process(r_h2o,input_data)
input_data = data_process(r_hous,input_data)
input_data = data_process(r_space,input_data)
input_data = data_process(r_natur,input_data)



input_data['size'] = 5
input_data['categoria'] = input_data['categoria'].apply(lambda x: x.lower())
input_data['categoria'] = input_data['categoria'].apply(lambda x: re.sub('culture','cultura',x))
input_data['categoria'] = input_data['categoria'].apply(lambda x: re.sub('spazio pubblico','spazio_pubblico',x))



fig = px.scatter_mapbox(input_data, lat="lat", lon="lon",
                        hover_name="name",
                        hover_data={"lat":False,
                                    "lon":False,
                                    "categoria":True,
                                    "link":False,
                                    "ambito":True,
                                    "size":False,
                                    'description_text':False,
                                    },
                        color_discrete_sequence=["orange"],
                        zoom=12,
                        size='size',
                        size_max=9,
                        height=500)

fig.update_mapboxes(style="mapbox://styles/federicogodino/ckziqrfug006i14nyovs0ee76",accesstoken="pk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6Y3hyazgwMjNvejJvbnh0ZXptbTJkbSJ9.HBsPU_tmnC_VbsAK4FA1XQ")
fig.update_layout(clickmode='event+select')

#fig.update_layout(margin={"r":.5,"t":0.5,"l":0.5,"b":0.5})
app = Dash(__name__)
server = app.server


app.layout = html.Div([
            dcc.Graph(
                        id='basic-interactions',
                        figure=fig,style={'display': 'inline-block',
                                'width':'45%',
                                }),

            html.Div(id="click-data",style={'display': 'inline-block',
                                            'width':'30%',
                                            'text-align':'center',
                                            }),


html.Div([

            html.Div(id="text-data",style={'display': 'inline-block',
                                            'width':'45%',
                                            'text-align':'center',
                                            }),


            html.Div(id="selected-data",style={'display': 'inline-block',
                                            'width':'20%',
                                            'text-align':'center',
                                            })
                                        ])
])



@app.callback(
    Output("click-data", "children"),
    Input('basic-interactions', 'clickData'))

def display_click_data(clickData):
    if clickData is None:
        return "Click on points in the graph"
    else:
        #Selezioni la stringa
        value = clickData['points'][0]
        value = value['customdata']
        value = value[2]
        # Seleziono nel dataframe
        df_tel = pd.read_excel('post_categorizzati.xlsx', engine='openpyxl')
        df_tel.sort_values(by='data', inplace=True)
        df_tel['categoria_2_out'].fillna('', inplace=True)

        df_tel_1 = df_tel[df_tel['categoria_1_out'] == value]
        df_tel_2 = df_tel[df_tel['categoria_2_out'] == value]

        df_out = pd.concat([df_tel_1,df_tel_2])
        df_out.sort_values(by='data',inplace=True)
        df_out = df_out.head(3)
        result = df_out.to_json(orient="records")

        #try:
            #cl = Client()
            #user = 'mikesugarb'
            #passwd = 'baby-lon'
            #cl.login(user, passwd)
            #value = cl.photo_download(2790325208562442752)
            #print('ok')

        #except:#TODO codifichi l'errore
        img = np.array(Image.open('download.jpg'))
        img1 = np.array(Image.open('download_1.jpg'))
        fig = make_subplots(
            rows=2, cols=1)
        fig.add_trace(go.Image(z=img), 1, 1)
        fig.add_trace(go.Image(z=img1), 2, 1)
        fig.update_layout(coloraxis_showscale=False,
                          title_text=value)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        return dcc.Graph(figure=fig)

@app.callback(
    Output("selected-data", "children"),
    Input('basic-interactions', 'selectedData'))

def display_select_data(selectedData):
    if selectedData is None:
        return ""
    else:

        value = selectedData['points'][0]
        name = value['hovertext']
        value = value['customdata']

        value = value[2]
        img = np.array(Image.open('download.jpg'))
        fig = make_subplots(
            rows=1, cols=1)
        fig.add_trace(go.Image(z=img), 1, 1)

        fig.update_layout(coloraxis_showscale=False,
                          title_text=name)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        return dcc.Graph(figure=fig)

@app.callback(
    Output("text-data", "children"),
    Input('basic-interactions', 'selectedData'))
def display_text_data(selectedData):
    if selectedData is None:
        return ""
    else:
        value = selectedData['points'][0]
        name = value['hovertext']
        value = value['customdata']
        value = value[6]
        return value



if __name__ == '__main__':
    app.run_server(debug=True)