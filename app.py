from dash import Dash, dcc, html, Input, Output
import requests
import json
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')


r = requests.get("https://api.mapbox.com/datasets/v1/federicogodino/cl0f4sd5j08r022pnj5t7fx3d/features?access_token=sk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6eW02azFvMDFvMDNjcXBkdWppdW9tbiJ9.u715QLdqAeEZzDCpfl2AYg")

data = r.text

data = json.loads(data)
data = data['features']
input_data = pd.DataFrame(columns=['lat','lon','name','media','categoria'])




for i in data:
    row = dict.fromkeys(['lat','lon'])
    row['lat'] = i['geometry']['coordinates'][1]
    row['lon'] = i['geometry']['coordinates'][0]
    input_data = input_data.append(row,ignore_index=True)

del(data,i,r)
input_data['name'] = 'Punto 1'
input_data['media'] = 'LINKPROVA'
input_data['categoria'] = 'mobilita'

#READ TELEGRAM DATA





fig = px.scatter_mapbox(input_data, lat="lat", lon="lon",
                        hover_name="name",
                        hover_data={"media":True,
                                    "lat":False,
                                    "lon":False,
                                    "categoria":True
                                    },
                        color_discrete_sequence=["orange"],
                        zoom=11,
                        height=500)

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
    if clickData is None:
        return "Click on points in the graph"
    else:
        #Selezioni la stringa
        value = clickData['points'][0]
        value = value['customdata']
        value = value[3]
        # Seleziono nel dataframe
        df_tel = pd.read_excel('post_categorizzati.xlsx', engine='openpyxl')
        df_tel.sort_values(by='data', inplace=True)
        df_tel['categoria_2_out'].fillna('', inplace=True)

        df_tel_1 = df_tel[df_tel['categoria_1_out'] == value]
        df_tel_2 = df_tel[df_tel['categoria_2_out'] == value]

        df_out = pd.concat([df_tel_1,df_tel_2])
        df_out.sort_values(by='data',inplace=True)

        result = df_out.to_json(orient="records")
        #output = json.dumps(result, indent=2)
        #Elaboro il return
        return result


if __name__ == '__main__':
    app.run_server(debug=True)