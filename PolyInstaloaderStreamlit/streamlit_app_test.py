from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np




us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")



fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["red"], zoom=3, height=300)


scatter = fig.data[0]
fig.update_mapboxes(style="mapbox://styles/federicogodino/ckziqrfug006i14nyovs0ee76",accesstoken="pk.eyJ1IjoiZmVkZXJpY29nb2Rpbm8iLCJhIjoiY2t6Y3hyazgwMjNvejJvbnh0ZXptbTJkbSJ9.HBsPU_tmnC_VbsAK4FA1XQ")
fig.update_layout(margin={"r":.5,"t":0.5,"l":0.5,"b":0.5})

scatter.on_click()


"""
def update_point(trace, points, selector):
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
        with f.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s


"""



fig.show()



"""
app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)
"""