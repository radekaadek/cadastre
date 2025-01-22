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

useless_attributes = {'lokalnyId', 'przestrzenNazw', 'wersjaId', 'startObiekt', 'startWersjaObiekt', 'podstawaUtworzeniaWersjiObiektu'}
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

#joiny do dolaczenia wlascicieli dla dzialek
dzialki = datas[2]
person_data = non_geometry_datas['EGB_OsobaFizyczna']
couple_data = non_geometry_datas['EGB_Malzenstwo']
institution_data = non_geometry_datas['EGB_Instytucja']
wlasnosc_data = non_geometry_datas['EGB_UdzialWeWlasnosci']

dzialki_merged = dzialki.merge(wlasnosc_data, left_on='JRG', right_on='JRG', #polaczenie dzialek z jrg
                               suffixes=('_dzialki', '_jrg'))

dzialki_merged= dzialki_merged.merge(person_data[['pierwszeImie', #polaczenie dzialek z osobami fizycznymi
                                                    'pierwszyCzlonNazwiska',
                                                    'gml_id']], left_on='osobaFizyczna', 
                                                    right_on='gml_id', how='left')

#rename columns related to osobafizyczna
dzialki_merged = dzialki_merged.rename(columns={
    'pierwszeImie': 'osobafiz_imie',
    'pierwszyCzlonNazwiska': 'osobafiz_nazwisko'
    })

malzenstwa = couple_data.merge(person_data[['pierwszeImie', #polaczenie malzenstwa z pierwsza osoba fizyczna
                                        'pierwszyCzlonNazwiska',
                                        'gml_id']], left_on='osobaFizyczna2',
                                        right_on='gml_id', how='left', suffixes=('_malzenstwo', '_osoba1'))

#rename columns in malzenstwa related to the first person
malzenstwa = malzenstwa.rename(columns={
    'pierwszeImie': 'osoba1_imie',
    'pierwszyCzlonNazwiska': 'osoba1_nazwisko'
    })

malzenstwa = malzenstwa.merge(person_data[['pierwszeImie', #polaczenie malzenstwa z druga osoba fizyczna
                                        'pierwszyCzlonNazwiska',
                                        'gml_id']], left_on='osobaFizyczna3',
                                        right_on='gml_id', how='left')

#rename columns in malzenstwa related to one person
malzenstwa = malzenstwa.rename(columns={
    'pierwszeImie': 'osoba2_imie',
    'pierwszyCzlonNazwiska': 'osoba2_nazwisko',
    'gml_id': 'gml_id_osoba2'
    })

dzialki_merged = dzialki_merged.merge(malzenstwa[['osoba1_imie','osoba1_nazwisko',
                                    'osoba2_imie','osoba2_nazwisko',
                                    'gml_id_malzenstwo']],left_on='malzenstwo',
                                        right_on='gml_id_malzenstwo', how='left')

dzialki_merged = dzialki_merged.merge(institution_data[['nazwaPelna',
                                                       'gml_id']], left_on='instytucja1',
                                                       right_on='gml_id', how='left')
#iterate all objects from DzialkaEwidencyjna
for index, row in dzialki.iterrows():
    current_gml_id = row.gml_id
    #get all merged rows for one gml_id
    merged_rows = dzialki_merged[dzialki_merged['gml_id_dzialki'] == current_gml_id]
    ownership_attribute = ''
    #iterate all merged rows for one DzialkaEwidencyjna
    for _, merged_row in merged_rows.iterrows():
        if pd.notna(merged_row.osobafiz_imie): #row has osoba fizyczna
            ownership_attribute += (f"[Właściciel: {merged_row.osobafiz_imie} {merged_row.osobafiz_nazwisko}"
                                    f" Udział: {merged_row.licznikUlamkaOkreslajacegoWartoscUdzialu}/"
                                    f"{merged_row.mianownikUlamkaOkreslajacegoWartoscUdzialu}]")

        if pd.notna(merged_row.gml_id_malzenstwo): #row has malzenstwo
            ownership_attribute += (f"[Małżeństwo: {merged_row.osoba1_imie} {merged_row.osoba1_nazwisko} i "
                                    f"{merged_row.osoba2_imie} {merged_row.osoba2_nazwisko} "
                                    f"Udział: {merged_row.licznikUlamkaOkreslajacegoWartoscUdzialu}/"
                                    f"{merged_row.mianownikUlamkaOkreslajacegoWartoscUdzialu}]")

        if pd.notna(merged_row.nazwaPelna):#row has instytucja
            ownership_attribute += (f"[Instytucja: {merged_row.nazwaPelna} "
                                     f"Udział: {merged_row.licznikUlamkaOkreslajacegoWartoscUdzialu}/"
                                     f"{merged_row.mianownikUlamkaOkreslajacegoWartoscUdzialu}]") 
    
    #add wlasciciele column to exsisting dzialki data
    dzialki.at[index, 'wlasciciele'] = ownership_attribute

# visualize using folium
m = folium.Map(location=[52.26520441814408, 20.55219304492736], zoom_start=13, tiles=None)

datas_list = [None] * len(datas)
for key, value in datas.items():
    datas_list[key] = value

geojson_layers = dict()
for data in datas_list:
    fields = [key for key in data.columns if key not in ['geometry', 'color', 'layer', 'gml_id']]
    
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
    #store layers in a dict
    geojson_layers[layer_name] = geojson_layer

layers_ordered = ["EGB_KonturUzytkuGruntowego", 
                    "EGB_KonturKlasyfikacyjny",
                        "EGB_DzialkaEwidencyjna",
                        "EGB_Budynek",
                        "EGB_PunktGraniczny" ]

#add layers in the correct order to map
for layer_name in layers_ordered:
    fg = folium.FeatureGroup(name=layer_name, overlay=True, control=True, show=True).add_to(m)
    geojson_layers[layer_name].add_to(fg)

#osm basemap
folium.TileLayer("OpenStreetMap", show=True,control=True).add_to(m)
#empty basemap
folium.TileLayer(
    tiles="",
    attr="Blank",
    name="Brak podkładu mapowego",
    show=False
).add_to(m)

folium.LayerControl().add_to(m)
m.save("map.html")