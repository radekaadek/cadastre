import geopandas as gpd
import folium
import os
import random


data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# function to generate a random color
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# add EGB_ to the list
name_to_pos = {'PunktGraniczny':4, 'Budynek': 3, 'DzialkaEwidencyjna': 2, 'KonturKlasyfikacyjny': 1, 'KonturUzytkuGruntowego': 0}
# add EGB_ to every key
name_to_pos = {f"EGB_{key}": value for key, value in name_to_pos.items()}
datas = [None] * len(name_to_pos)


for idx, layer in gpd.list_layers("Fixed.gml").iterrows():
    name = layer['name']
    data = gpd.read_file("Fixed.gml", layer=name)
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
        data.to_csv(f"{data_dir}/{name}.csv", index=False)

# visualize using folium
m = folium.Map(location=[52.26520441814408, 20.55219304492736], zoom_start=13)

for data in datas:
    fields = [key for key in data.columns if key != 'geometry']
    # print(data['geometry'])
    data['Wspolrzedne'] = ''
    for idx, row in data.iterrows():
        data.loc[idx, 'Wspolrzedne'] = str(row['geometry'])[7:-1]
    fields.append('Wspolrzedne')
    #get current layer name
    layer_name = data.iloc[0].layer
    geojson_layer = folium.GeoJson(
        data,
        style_function=lambda x: {'color': x['properties']['color']},
        popup=folium.GeoJsonPopup(fields=fields),
        name=layer_name
    )
    #add each geojson to layer control
    fg = folium.FeatureGroup(name=layer_name, overlay=True, control=True, show=True).add_to(m)
    geojson_layer.add_to(fg)
    
folium.LayerControl().add_to(m)

m.save("map.html")
