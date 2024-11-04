import tkinter as tk
import io

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

file_path = "course_materials/kontrolny_plik.txt"
with open(file_path, encoding="ISO-8859-2", newline="\r\n") as file:
    data = file.readlines()


def podziel(name: str) -> list:
    return name.split("-") if "-" in name else [name]


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

for line in data:
    newLine = line.strip()
    if 3 < len(newLine) < 20:
        dzialki.append(newLine)

nums = set()
powtorzone: list[str] = []
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
        if char.isspace():
            # print(f"Zły znak w numerze: {i}: {repr(char)}")
            return True
    return False

def powtorzone_numbers(nums: list[str]) -> list[str]:
    return [num for num in nums if nums.count(num) > 1]


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
    else:
        part0 = i.split("/")[0]
        part = i.split("/")[1]
        for znak in part0:
            if not (znak.isnumeric() or znak == "-"):
                zapis_numeru.append(i)
                # print("Zły zapis numeru punktu: ", i)
        else:
            if part0 in nums:
                powtorzone.append(i)
            nums.add(part0)
            name = podziel(part)
            if len(name) > 2:
                # print(name)
                zapis_numeru.append(i)
                continue
            # print(name)
            if len(name) == 1:
                if name[0] in OFU or warunek1(name[0]):
                    continue
                elif name[0] == "E":
                    oznaczenie_ofu.append(i)
                    continue
                    # print("Użytek ekologiczny nie jest aktualny: ", i)
                elif name[0] in OFU1:
                    dana_ofu.append(i)
                    continue
                    # print("Dana wartość OFU musi być powiązana z OZK: ", i)
                else:
                    przyjecie_wartosci_ofu.append(i)
                    continue
                    # print("Zła przyjęcie wartości OZK: ", i)
            elif len(name) == 2:
                if name[0] in OFU1 and warunek2(name[0], name[1]):
                    continue
                if name[0] in OFU:
                    grunt_nie_podlega.append(i)
                    # print("Podany grunt nie podlega gleboznawczej klasyfikacji gruntów: ", i)
                elif name[0] == "E":
                    uzytek_ekologiczny.append(i)
                    # print("Użytek ekologiczny nie jest aktualny: ", i)
                elif name[0] == "S" and name[1] not in {"R", "Ł", "Ps"}:
                    wartosc_s.append(i)

stream = io.StringIO()
if len(ukosniki) > 0:
    stream.write(f"Numery z nieprawidłową ilością ukośników: {len(ukosniki)}\n")
    for uk in ukosniki:
        stream.write(f"{uk}\n")

if len(myslniki) > 0:
    stream.write(f"Numery bez myślnika: {len(myslniki)}\n")
    for mys in myslniki:
        stream.write(f"{mys}\n")

if len(zapis_numeru) > 0:
    stream.write(f"Numery ze złym zapisem numeru: {len(zapis_numeru)}\n")
    for nr in zapis_numeru:
        stream.write(f"{nr}\n")

if len(oznaczenie_ofu) > 0:
    stream.write(f"Numery z nieprawidłowym oznaczeniem OFU gdzie użytek ekologiczny nie jest aktualny: {len(oznaczenie_ofu)}\n")
    for oz in oznaczenie_ofu:
        stream.write(f"{oz}\n")

if len(przyjecie_wartosci_ofu) > 0:
    stream.write(f"Numery z wartośćą OFU która nie jest powiązana z OZU i OZK: {len(przyjecie_wartosci_ofu)}\n")
    for do in przyjecie_wartosci_ofu:
        stream.write(f"{do}\n")

if len(grunt_nie_podlega) > 0:
    stream.write(f"Numery z gruntem który nie podlega gleboznawczej klasyfikacji gruntów: {len(grunt_nie_podlega)}\n")
    for gr in grunt_nie_podlega:
        stream.write(f"{gr}\n")

if len(uzytek_ekologiczny) > 0:
    stream.write(f"Numery z nieprawidłowym oznaczeniem OFU gdzie użytek ekologiczny nie jest aktualny: {len(uzytek_ekologiczny)}\n")
    for uz in uzytek_ekologiczny:
        stream.write(f"{uz}\n")

if len(dana_ofu) > 0:
    stream.write(f"Numery z nieprawidłową daną OFU: {len(dana_ofu)}\n")
    for do in dana_ofu:
        stream.write(f"{do}\n")

if len(wartosc_s) > 0:
    stream.write(f"Numery gdzie po S nie jest R, Ł, Ls: {len(wartosc_s)}\n")
    for wart in wartosc_s:
        stream.write(f"{wart}\n")

if len(powtorzone) > 0:
    stream.write(f"Powtarzające się numery: {len(powtorzone)}\n")
    for rep in powtorzone:
        stream.write(f"{rep}\n")


all_errors = {*ukosniki, *myslniki, *zapis_numeru, *oznaczenie_ofu, *przyjecie_wartosci_ofu, *grunt_nie_podlega, *uzytek_ekologiczny, *dana_ofu, *wartosc_s}

stream.write(f"Liczba wszystkich blednych numerów: {len(all_errors) + len(powtorzone)}\n")

stream.write(f"{len(dzialki) - len(all_errors)}\n")

print(stream.getvalue())

# write all to a file
file_name = "ok.txt"
with open(file_name, "w") as file:
    for i in all_errors:
        file.write(i)
        file.write("\n")

print(f"Zapisano wszystkie bledne numery do pliku {file_name}")

window = tk.Tk()
window.title("Błędy")
window.geometry("500x500")

tk.Label(window, text=stream.getvalue()).pack()

window.mainloop()

