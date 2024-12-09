import geopandas as gpd
import folium
import os
import random

datas = []

data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# function to generate a random color
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

for idx, layer in gpd.list_layers("Zbiór danych GML ZSK 2025.gml").iterrows():
    name = layer['name']
    data = gpd.read_file("Zbiór danych GML ZSK 2025.gml", layer=name)
    # change to geopandas dataframe
    if 'geometry' in data.columns:
        # add name as a column
        data['layer'] = name
        data['color'] = random_color()
        datas.append(data)
        data_reproj = data.to_crs(epsg=4326)
        # data_reproj = data_reproj.to_file(f"{data_dir}/{name}.geojson", driver="GeoJSON")
    else:
        # save to csv
        print(data.info())
        data.to_csv(f"{data_dir}/{name}.csv", index=False)

# function to create a popup with feature's attributes
def create_popup(feature):
    popup_content = "<br>".join([f"{key}: {value}" for key, value in feature['properties'].items()])
    return folium.Popup(popup_content, max_width=300)

# visualize using folium
m = folium.Map(location=[52.26520441814408, 20.55219304492736], zoom_start=13)

for data in datas:
    fields = [key for key in data.columns if key != 'geometry']
    child = m.add_child(folium.GeoJson(
        data,
        style_function=lambda x: {'color': x['properties']['color']},
        popup=folium.GeoJsonPopup(fields=fields)
    ))

m.save("map.html")
