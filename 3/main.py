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
name_to_pos = {'Budynek': 3, 'DzialkaEwidencyjna': 2, 'KonturKlasyfikacyjny': 1, 'KonturUzytkuGruntowego': 0}
# add EGB_ to every key
name_to_pos = {f"EGB_{key}": value for key, value in name_to_pos.items()}
datas = [None] * len(name_to_pos)


for idx, layer in gpd.list_layers("Zbiór danych GML ZSK 2025.gml").iterrows():
    name = layer['name']
    data = gpd.read_file("Zbiór danych GML ZSK 2025.gml", layer=name)
    # change to geopandas dataframe
    if 'geometry' in data.columns:
        if name in name_to_pos:
            # add name as a column
            data['layer'] = name
            data['color'] = random_color()
            datas[name_to_pos[name]] = data
            data_reproj = data.to_crs(epsg=4326)
    else:
        data.to_csv(f"{data_dir}/{name}.csv", index=False)


# function to create a popup with feature's attributes
def create_popup(feature):
    popup_content = "<br>".join([f"{key}: {value}" for key, value in feature['properties'].items()])
    return folium.Popup(popup_content, max_width=300)

# visualize using folium
m = folium.Map(location=[52.26520441814408, 20.55219304492736], zoom_start=13)

for data in datas:
    fields = [key for key in data.columns if key != 'geometry']
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
