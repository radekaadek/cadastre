input_file = 'Zbiór danych GML ZSK 2025.gml'
output_file = 'Fixed.gml'

with open(input_file, 'r') as f:
    lines = f.readlines()

#### UDZIAL WE WLASNOSCI
# delete all lineswith <egb:podmiotUdzialuWlasnosci>
for i in range(len(lines)):
    if '<egb:podmiotUdzialuWlasnosci>' in lines[i]:
        lines[i] = ''

# delete all lineswith </egb:podmiotUdzialuWlasnosci>
for i in range(len(lines)):
    if '</egb:podmiotUdzialuWlasnosci>' in lines[i]:
        lines[i] = ''

# change all
# <egb:EGB_Podmiot gml:id="pdm.3b5110fb-d6d4-4854-8ae8-00a95c1b4be0">
# to
# <egb:EGB_Podmiot>pdm.3b5110fb-d6d4-4854-8ae8-00a95c1b4be0</egb:EGB_Podmiot>
# and delete all
# <\egb:EGB_Podmiot>

# delete all lineswith </egb:EGB_Podmiot>
for i in range(len(lines)):
    if '</egb:EGB_Podmiot>' in lines[i]:
        lines[i] = ''

for i in range(len(lines)):
    if '<egb:EGB_Podmiot gml:id' in lines[i]:
        id = lines[i].split('"')[1]
        lines[i] = f'<egb:EGB_Podmiot>{id}</egb:EGB_Podmiot>\n'

# change all <egb:podstawaUtworzeniaWersjiObiektu xlink:href="PL.PZGiK.179.EGiB_aadb7f8f-066b-44e6-ae19-0994cbea4448_2007-06-04T11-36-35" xlink:type="simple"/>
# to
# <egb:podstawaUtworzeniaWersjiObiektu>PL.PZGiK.179.EGiB_aadb7f8f-066b-44e6-ae19-0994cbea4448_2007-06-04T11-36-35</egb:podstawaUtworzeniaWersjiObiektu>
for i in range(len(lines)):
    if r'<egb:podstawaUtworzeniaWersjiObiektu xlink:href="' in lines[i]:
        id = lines[i].split('"')[1]
        lines[i] = f'<egb:podstawaUtworzeniaWersjiObiektu>{id}</egb:podstawaUtworzeniaWersjiObiektu>\n'



#### OsobaFizyczna
# change all <egb:adresOsobyFizycznej xlink:href="PL.PZGiK.179.EGiB_8e0cc5e9-d059-459a-93c7-48f957a8d09d_2022-10-13T12-17-41" xlink:type="simple"/>
# to <egb:adresOsobyFizycznej>PL.PZGiK.179.EGiB_8e0cc5e9-d059-459a-93c7-48f957a8d09d_2022-10-13T12-17-41</egb:adresOsobyFizycznej>
for i in range(len(lines)):
    if r'<egb:adresOsobyFizycznej xlink:href="' in lines[i] and lines[i][-3:-1] == '/>':
        id = lines[i].split('"')[1]
        lines[i] = f"<egb:adresOsobyFizycznej>{id}</egb:adresOsobyFizycznej>\n"

# change all <egb:osobaFizyczna xlink:href="PL.PZGiK.179.EGiB_fd812b09-b957-46e8-a3c1-fbedec2bfb7d_2024-04-26T15-52-50" xlink:type="simple"/>
# to <egb:osobaFizyczna>PL.PZGiK.179.EGiB_fd812b09-b957-46e8-a3c1-fbedec2bfb7d_2024-04-26T15-52-50</egb:osobaFizyczna>
for i in range(len(lines)):
    if r'<egb:osobaFizyczna xlink:href="' in lines[i] and lines[i][-3:-1] == '/>':
        id = lines[i].split('"')[1]
        lines[i] = f"<egb:osobaFizyczna>{id}</egb:osobaFizyczna>\n"


#### adresZameldowania jest ok

# write to Fixed.gml
with open(output_file, 'w') as f:
    f.writelines(lines)


