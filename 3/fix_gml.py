input_file = 'Zbiór danych GML ZSK 2025.gml'
output_file = 'Fixed.gml'

with open(input_file, 'r') as f:
    lines = f.readlines()

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
        lines[i+1] = ''

# change all <egb:podstawaUtworzeniaWersjiObiektu xlink:href="PL.PZGiK.179.EGiB_aadb7f8f-066b-44e6-ae19-0994cbea4448_2007-06-04T11-36-35" xlink:type="simple"/>
# to
# <egb:podstawaUtworzeniaWersjiObiektu>PL.PZGiK.179.EGiB_aadb7f8f-066b-44e6-ae19-0994cbea4448_2007-06-04T11-36-35</egb:podstawaUtworzeniaWersjiObiektu>
for i in range(len(lines)):
    if r'<egb:podstawaUtworzeniaWersjiObiektu xlink:href="' in lines[i] and r'' == lines[i][-2:]:
        id = lines[i].split('"')[1]
        lines[i] = f'<egb:podstawaUtworzeniaWersjiObiektu>{id}</egb:podstawaUtworzeniaWersjiObiektu>\n'


# write to Fixed.gml
with open(output_file, 'w') as f:
    f.writelines(lines)


