OFU = [
    "B",
    "Ba",
    "Bi",
    "Bp",
    "Bz",
    "K",
    "dr",
    "Tk",
    "Ti",
    "Tp",
    "Wm",
    "Wp",
    "Ws",
    "Tr",
    "Ls",
    "Lz",
    "N",
]
OFU1 = ["S", "Br", "Wsr", "W", "Lzr"]
OZU = ["Ł", "Ps", "Ls", "Lz", "R"]
OZK = ["I", "II", "III", "IV", "V", "VI"]
OZK1 = ["I", "II", "IIIa", "IIIb", "IVa", "IVb", "V", "VI", "VIz"]

file_path = "course_materials/Kontury_eksport_dz.txt"
with open(file_path, encoding="ISO-8859-1", newline="\r\n") as file:
    data = file.readlines()


def podziel(name) -> list:
    p = []
    if "-" not in name:
        p.append(name)
    else:
        parts = name.split("-")
        for part in parts:
            p.append(part)
    return p


def pomin(input_string, letters_to_skip):
    for letter in letters_to_skip:
        if input_string.startswith(letter):
            input_string = input_string[len(letter):]
    return input_string


def warunek1(name) -> bool:
    if name.startswith("R"):
        name = pomin(name, "R")
        for letter in OZK1:
            if letter == name:
                return True
        return False
    elif name.startswith(("Ł", "Ps", "Ls", "Lz")):
        name = pomin(name, ("Ł", "Ps", "Ls", "Lz"))
        for letter in OZK:
            if letter == name:
                return True
        return False
    return False


def warunek2(name1, name2) -> bool:
    for l in OFU1:
        if l in name1:
            if name2.startswith("R"):
                name2 = pomin(name2, "R")
                for letter in OZK1:
                    if letter == name2:
                        return True
            elif name2.startswith(("Ł", "Ps")):
                name2 = pomin(name2, ("Ł", "Ps"))
                for letter in OZK:
                    if letter == name2:
                        return True
            elif name1 == "W" and name2.startswith(("Ls", "Lz")):
                name2 = pomin(name2, ("Ls", "Lz"))
                for letter in OZK:
                    if letter == name2:
                        return True
        else:
            return False
    return False


dzialki: list[str] = []
prawidlowe = []

for line in data:
    newLine = line.strip()
    if 3 < len(newLine) < 20:
        dzialki.append(newLine)

ukosniki = []
myslniki = []
zapis_numeru = []
oznaczenie_ofu = []
dana_ofu = []
przyjecie_wartosci_ofu = []
grunt_nie_podlega = []
uzytek_ekologiczny = []
wartosc_s = []
# S-R Ł Ls może

def bad_charnumber(i: str) -> bool:
    for char in i:
        if char != r'/' and char != '-' and not char.isnumeric() and not char.isalpha():
            # print(f"Zły znak w numerze: {i}: {repr(char)}")
            return True
        if not char.isascii():
            # print(f"Znak nie jest ASCII: {i}: {repr(char)}")
            return True
    return False

for i in dzialki:

    if bad_charnumber(i):
        zapis_numeru.append(i)
        continue
        # print("Zły zapis numeru punktu: ", i)

    
    if i.count("/") != 1:
        ukosniki.append(i)
        # print("Zła ilość ukośników w nazwie: ",i)
    elif " " in i:
        myslniki.append(i)
        # print("Brak myślnika, odstęp między znakami: ", i)
        pass
    else:
        part0 = i.split("/")[0]
        part = i.split("/")[1]
        for znak in part0:
            if not (znak.isnumeric() or znak == "-"):
                zapis_numeru.append(i)
                # print("Zły zapis numeru punktu: ", i)
        else:
            name = podziel(part)
            # print(name)
            if len(name) == 1:
                if name[0] in OFU or warunek1(name[0]):
                    prawidlowe.append(i)
                elif name[0] == "E":
                    oznaczenie_ofu.append(i)
                    # print("Użytek ekologiczny nie jest aktualny: ", i)
                elif name[0] in OFU1:
                    dana_ofu.append(i)
                    # print("Dana wartość OFU musi być powiązana z OZK: ", i)
                else:
                    przyjecie_wartosci_ofu.append(i)
                    # print("Zła przyjęcie wartości OZK: ", i)
            elif len(name) == 2:
                if name[0] in OFU1 and warunek2(name[0], name[1]):
                    prawidlowe.append(i)
                elif name[0] in OFU:
                    grunt_nie_podlega.append(i)
                    # print("Podany grunt nie podlega gleboznawczej klasyfikacji gruntów: ", i)
                elif name[0] == "E":
                    uzytek_ekologiczny.append(i)
                    # print("Użytek ekologiczny nie jest aktualny: ", i)
                elif name[0] == "S" and name[1] not in {"R", "Ł", "Ps"}:
                    wartosc_s.append(i)

            elif len(name) == 3:
                if name[0] == "E":
                    uzytek_ekologiczny.append(i)
                    # print("Użytek ekologiczny nie jest aktualny ", i)

print(f"Numery z nieprawidłową ilością ukośników: {len(ukosniki)}")
for uk in ukosniki:
    print(uk)

print(f"Numery bez myślnika: {len(myslniki)}")
for mys in myslniki:
    print(mys)

print(f"Numery ze złym zapisem numeru: {len(zapis_numeru)}")
for nr in zapis_numeru:
    print(nr)

print(f"Numery z nieprawidłowym oznaczeniem OFU gdzie użytek ekologiczny nie jest aktualny: {len(oznaczenie_ofu)}")
for oz in oznaczenie_ofu:
    print(oz)

print(f"Numery z wartośćą OFU która nie jest powiązana z OZU i OZK: {len(przyjecie_wartosci_ofu)}")
for do in dana_ofu:
    print(do)

print(f"Numery z gruntem który nie podlega gleboznawczej klasyfikacji gruntów: {len(grunt_nie_podlega)}")
for gr in grunt_nie_podlega:
    print(gr)

print(f"Numery z nieprawidłowym oznaczeniem OFU gdzie użytek ekologiczny nie jest aktualny: {len(uzytek_ekologiczny)}")
for uz in uzytek_ekologiczny:
    print(uz)

print(f"Numery gdzie po S nie jest R, Ł, Ls: {len(wartosc_s)}")
for wart in wartosc_s:
    print(wart)


all_errors = list(set([*ukosniki, *myslniki, *zapis_numeru, *oznaczenie_ofu, *przyjecie_wartosci_ofu, *grunt_nie_podlega, *uzytek_ekologiczny, *dana_ofu, *wartosc_s]))

print(f"Liczba wszystkich blednych numerów: {len(all_errors)}")

# write all to a file
with open("ok.txt", "w") as file:
    for i in all_errors:
        file.write(i)
        file.write("\n")

print("Zapisano wszystkie bledny numery do pliku ok.txt")

