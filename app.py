from dash import Dash, dcc, html, Input, Output
from data_processing import data_process
from instagrapi import Client
import requests
import json
import pandas as pd
import plotly.express as px
import warnings
import re
import os

warnings.filterwarnings('ignore')
from plotly.subplots import make_subplots

from PIL import Image
import numpy as np
import plotly.graph_objects as go


list_datasets=['cl0f4sd5j08r022pnj5t7fx3d','cl0mygcb505jv22s95tj8jab1','cl0med4ux01h521p8liyzzlqf',
               'ckzokywth2wzo2dte61czaktb','cl0f5p20u0m2e20qum84o85l8','cl0p7q5nk13c621r03a8kdmu7',
               'cl0p83jhb030r28st8jaklulv']

global list_of_files
#DATA
r_heri = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0f4sd5j08r022pnj5t7fx3d/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_cult = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0mygcb505jv22s95tj8jab1/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_inn = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0med4ux01h521p8liyzzlqf/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_h2o = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/ckzokywth2wzo2dte61czaktb/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_hous = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0f5p20u0m2e20qum84o85l8/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_space = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0p7q5nk13c621r03a8kdmu7/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")
r_natur = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0p83jhb030r28st8jaklulv/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")


#############################
#Set instagrapi new images
cl = Client()
user = 'instafinderbot'
passwd = 'instaloader'

cl.login(user, passwd)

user_id = cl.user_id_from_username("frames_of_urban_transformation")
#La query prende gli ultimi 2 risultati
medias = cl.user_medias_v1(user_id, 2)


types = ('*.jpeg', '*.jpg')
path = 'static/instagrapi'
#list_of_files=[tuple(glob.glob(i)) for i in types if len(glob.glob(i)) > 0]
list_of_files = tuple([f for f in os.listdir(path) if f.endswith('.jpg')])
list_of_files2 = tuple([f for f in os.listdir(path) if f.endswith('.jpeg')])
list_of_files = list_of_files + list_of_files2

#list_of_files = set([element for tupl in list_of_files for element in tupl])


for i in medias:
    i = dict(i)
    if len(list_of_files) > 0:
        #for j in list_of_files:
        if any(i['pk'] in s for s in list_of_files):
            pass
        else:
            print('sto scaricando')
            cl.photo_download(i['pk'],'static/instagrapi')
    else:
        print('sto scaricando')
        cl.photo_download(i['id'], 'static/instagrapi')

################################






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
                                'width':'55%',
                                }),

            html.Div(id="click-data",style={'display': 'inline-block',
                                            'width':'40%',
                                            'text-align':'center',
                                            }),


html.Div([

            html.Div(id="text-data",style={'display': 'inline-block',
                                            'width':'35%',
                                            'text_allign':'center',
                                            'margin-top':'120px',
                                            'font-family':'Open Sans',
                                            'font-size':13,
                                             'color':'black'}),


            html.Div(id="selected-data",style={'display': 'inline-block',
                                            'width':'65%',
                                            'float':'right',
                                            })
                                        ],
            style={"margin":"60px",
                   "text-align":"center"})
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

        types = ('*.jpeg', '*.jpg')
        path = 'static/instagrapi'
        # list_of_files=[tuple(glob.glob(i)) for i in types if len(glob.glob(i)) > 0]
        list_of_files = tuple([f for f in os.listdir(path) if f.endswith('.jpg')])
        list_of_files2 = tuple([f for f in os.listdir(path) if f.endswith('.jpeg')])
        list_of_files = list_of_files + list_of_files2
        # Seleziono nel dataframe
        #df_tel = pd.read_excel('post_categorizzati.xlsx', engine='openpyxl')
        #df_tel.sort_values(by='data', inplace=True)
        #df_tel['categoria_2_out'].fillna('', inplace=True)

        #df_tel_1 = df_tel[df_tel['categoria_1_out'] == value]
        #df_tel_2 = df_tel[df_tel['categoria_2_out'] == value]

        #df_out = pd.concat([df_tel_1,df_tel_2])
        #df_out.sort_values(by='data',inplace=True)
        #df_out = df_out.head(3)
        #result = df_out.to_json(orient="records")

        #try:
            #cl = Client()
            #user = 'mikesugarb'
            #passwd = 'baby-lon'
            #cl.login(user, passwd)
            #value = cl.photo_download(2790325208562442752)
            #print('ok')

        #except:#TODO codifichi l'errore
        # Create figure
        if value == 'cultura':
            #ok
            #size = 128,128
            img = np.array(Image.open('static/cultura_1.jpg').resize((1280,1280), Image.ANTIALIAS))


            img1 = np.array([])
        if value == 'natura':
            #ok
            img = np.array(Image.open('static/natura_1.jpg'))
            img1 = np.array([])
        if value == 'housing':
            #ok
            img = np.array(Image.open('static/housing_1.jpg'))
            img1 = np.array(Image.open('static/housing_2.jpg'))
        if value == 'spazio_pubblico':
            #ok
            img = np.array(Image.open('static/spazio_pubblico_1.webp'))
            img1 = np.array(Image.open('static/spazio_pubblico_2.jpg'))
        if value == 'heritage':

            img = np.array(Image.open('static/heritage_1.jpg'))
            img1 = np.array([])
        if value == 'innovazione':
            img = np.array(Image.open('static/innovazione_1.webp'))
            img1 = np.array(Image.open('static/innovazione_2.jpg'))



        fig = make_subplots(
            rows=2, cols=2)

        fig.add_layout_image(

        )


        if len(img1) > 0:
            fig.add_trace(go.Image(z=img), 1, 1)
            fig.add_trace(go.Image(z=img1), 2, 1)

        else:
            fig.add_trace(go.Image(z=img), 1, 1)

        #list_of_files

        img_test = np.array(Image.open('static/instagrapi/{}'.format(list_of_files[0])))
        img_test1 = np.array(Image.open('static/instagrapi/{}'.format(list_of_files[1])))

        fig.add_trace(go.Image(z=img_test), 1, 2)
        fig.add_trace(go.Image(z=img_test1), 2, 2)



        fig.update_layout(coloraxis_showscale=False,
                          title_text=value,title_x=0.5,
                          #title_font_size = 1.1
                          )
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
        text = value[6]

        value = value[2]

        if name == 'SOS Fornace':
            img = np.array(Image.open('static/ZFP4939.jpg'))

        elif name == 'Ghisi Skatepark':
            img = np.array(Image.open('static/Ghisi.jpg'))
        elif name == 'PLIS Basso Olona':
            img = np.array(Image.open('static/PLIS.jpg'))
        elif name == 'Sala Filatoio, Villa Burba':
            img = np.array(Image.open('static/sala_filatoio.jpg'))
        elif name == 'Comune di Rho ':
            img = np.array(Image.open('static/centr01.jpg'))
        elif name == 'CentRho':
            img = np.array(Image.open('static/map_inter01.jpg'))
        elif name == "Agenzia dell'abitare rhodense":
            img = np.array(Image.open('static/ABIT01.jpg'))
        elif name == "Arexpo":
            img = np.array(Image.open('static/EXP01.png'))
        elif name == "Terreno Expo":
            img = np.array(Image.open('static/ud2.jpg'))
        else:
            pass

        fig = go.Figure()
        fig.add_trace(go.Image(z=img))

        fig.update_layout(coloraxis_showscale=False,
                          title_text=name.upper(),title_pad_r=3,title_font_size=25,title_font_family="Arial")
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