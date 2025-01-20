import geopandas as gpd
import folium
import os
import random
import pandas as pd


data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# function to generate a random color
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# add EGB_ to the list
name_to_pos = {'PunktGraniczny':4, 'Budynek': 3, 'DzialkaEwidencyjna': 2, 'KonturKlasyfikacyjny': 1, 'KonturUzytkuGruntowego': 0}
pos2name = {v: k for k, v in name_to_pos.items()}
# add EGB_ to every key
name_to_pos = {f"EGB_{key}": value for key, value in name_to_pos.items()}
datas = {} # position: data

useless_attributes = {'gml_id', 'lokalnyId', 'przestrzenNazw', 'wersjaId', 'startObiekt', 'startWersjaObiekt', 'podstawaUtworzeniaWersjiObiektu'}
non_geometry_datas = {}

for idx, layer in gpd.list_layers("Fixed.gml").iterrows():
    name = layer['name']
    data = gpd.read_file("Fixed.gml", layer=name)
    usless_columns = [key for key in data.columns if key in useless_attributes]
    data.drop(usless_columns, axis=1, inplace=True)
    # rename JRG2 to JRG
    if 'JRG2' in data.columns:
        data.rename(columns={'JRG2': 'JRG'}, inplace=True)
    # change to geopandas dataframe
    if 'geometry' in data.columns:
        if name in name_to_pos:
            # add name as a column
            data['layer'] = name
            data['color'] = random_color()
            # if its PunktGraniczny add wspolrzedne column with geometry
            # if name == "EGB_PunktGraniczny":
            #     data['Wspolrzedne'] = data['geometry']
            datas[name_to_pos[name]] = data
            data_reproj = data.to_crs(epsg=4326)
    else:
        non_geometry_datas[name] = data
        data.to_csv(f"{data_dir}/{name}.csv", index=False)

# visualize using folium
m = folium.Map(location=[52.26520441814408, 20.55219304492736], zoom_start=13)

datas_list = [None] * len(datas)
for key, value in datas.items():
    datas_list[key] = value

for data in datas_list:
    fields = [key for key in data.columns if key not in ['geometry', 'color', 'layer']]
    
    # Format 'Współrzędne' as a text field with a scrollbar
    data['Współrzędne'] = ''
    for idx, row in data.iterrows():
        coords = str(row['geometry'])
        layer_name = row['layer']
        # Apply slicing based on layer name
        if layer_name == 'EGB_Budynek':
            formatted_coords = coords[16:-2]
        elif layer_name in ['EGB_KonturKlasyfikacyjny', 'EGB_KonturUzytkuGruntowego', 'EGB_DzialkaEwidencyjna']:
            formatted_coords = coords[10:-2]
        elif layer_name in ['EGB_PunktGraniczny']:
            formatted_coords = coords[7:-1]
        else:
            formatted_coords = coords  # Default formatting for other layers
        # Format coordinates into a scrollable text field
        data.loc[idx, 'Współrzędne'] = (
            f"<textarea style='width: 100%; height: 100px; overflow: auto;' readonly>"
            f"{formatted_coords}</textarea>"
        )
    
    fields.append('Współrzędne')

    # Get current layer name
    geojson_layer = folium.GeoJson(
        data,
        style_function=lambda x: {'color': x['properties']['color']},
        popup=folium.GeoJsonPopup(fields=fields, max_width="500px"),  # Set popup width
        name=layer_name
    )
    # Add each GeoJSON to layer control
    fg = folium.FeatureGroup(name=layer_name, overlay=True, control=True, show=True).add_to(m)
    geojson_layer.add_to(fg)


m.save("map.html")