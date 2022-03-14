import pandas as pd
import json

def data_process(data,input_data):
    data = data.text
    data = json.loads(data)
    data = data['features']
    for i in data:
        row = dict.fromkeys(['lat','lon'])
        #print(i['geometry']['type'])
        if len(i['geometry']['coordinates']) == 2:#TODO:sostiuire la condizione con type point
           row['lat'] = i['geometry']['coordinates'][1]
           row['lon'] = i['geometry']['coordinates'][0]
           row['name'] = i['properties']['NOME']
           row['link'] = i['properties']['LINK WEB']
           row['categoria'] = i['properties']['CATEGORIA']
           row['ambito'] = i['properties']['AMBITO']
           row['description_text'] = i['properties']['COPY']

        else:
            continue

        if isinstance(row['lat'],float):
           input_data = input_data.append(row,ignore_index=True)
        else:
           pass

    return input_data
