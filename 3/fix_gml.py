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

# delete all lineswith </egb:EGB_Podmiot>
for i in range(len(lines)):
    if '<egb:EGB_Podmiot gml:id' in lines[i]:
        id = lines[i].split('"')[1]
        lines[i] = f'<egb:EGB_Podmiot>{id}</egb:EGB_Podmiot>\n'

for i in range(len(lines)):
    if '</egb:EGB_Podmiot>' in lines[i]:
        lines[i] = ''


def replace_xlink_href(lines, tag):
    # Replace xlink:href with <tag>id</tag>
    for i in range(len(lines)):
        if f'<{tag} xlink:href="' in lines[i] and lines[i][-3:-1] == '/>':
            id = lines[i].split('"')[1]
            lines[i] = f"<{tag}>{id}</{tag}>\n"
    return lines

tags_to_replace = [
    "egb:podstawaUtworzeniaWersjiObiektu",
    "egb:adresOsobyFizycznej",
    "egb:osobaFizyczna",
    "egb:dzialkaZabudowana",
    "egb:JRG2",
    "egb:lokalizacjaKonturu",
    "egb:lokalizacjaUzytku",
    "egb:JRG",
    "egb:adresDzialki",
    "egb:lokalizacjaObrebu",
    "egb:adresBudynku",
    "egb:budynekZElementamiZwiazanymi",
    "egb:osobaFizyczna2"
]

for tag in tags_to_replace:
    lines = replace_xlink_href(lines, tag)


# write to Fixed.gml
with open(output_file, 'w') as f:
    f.writelines(lines)


