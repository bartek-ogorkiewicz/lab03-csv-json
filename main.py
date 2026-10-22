# przykładowy input: python main.py -m styczeń luty -d pn-wt pt -p r w -t -c -j
# przyjmuję, że miesiące zapisujemy z małej litery używając polskich znaków, a dni tygodnia skrótowo: pn, wt, śr, cz, pt, sb, nd; z kolei pory dnia "r" lub "w"

import argparse
from pathlib import Path
import json
from random import randint
from csv import reader


def main():
    parser = argparse.ArgumentParser(description="Tworzy lub odczytuje pliki Dane.csv i Dane.json w katalogach miesiąc/dzień/pora")
    parser.add_argument("-m", nargs="+", required=True, help="miesiące, np. styczeń luty")
    parser.add_argument("-d", nargs="+", required=True, help="dzień lub zakres dni dla każdego miesiąca, np. pn-wt pt")
    parser.add_argument("-p", nargs="*", default=[], choices=["r", "w"], help="pora dnia (r - rano, w - wieczór) dla każdego dnia, domyślnie rano")
    parser.add_argument("-t", action="store_true", help="tworzenie plików (bez -t pliki są odczytywane)")
    parser.add_argument("-c", action="store_true", help="pliki csv")
    parser.add_argument("-j", action="store_true", help="pliki json")
    args = parser.parse_args()

    if len(args.m) != len(args.d):
        parser.error("liczba miesięcy i zakresów dni musi być taka sama")

    ile_dni = 0
    for d in args.d:
        if "-" in d:
            ile_dni += len(days_range(d))
        else:
            ile_dni += 1

    pory = []
    for p in args.p:
        if p == "r":
            pory.append("rano")
        else:
            pory.append("wieczór")
    while len(pory) < ile_dni:
        pory.append("rano")

    paths = generate_paths(args.m, args.d, pory)
    create_folders_and_handle_files(paths, args.t, not args.t, args.c, args.j)

def generate_paths(months, days, times):
    paths = []
    idx = 0
    for month, d in zip(months, days):
        day_list = days_range(d) if "-" in d else [d]
        for day in day_list:
            paths.append(Path.cwd() / month / day / times[idx])
            idx += 1
    return paths

# Funkcja odczytuje i sumuje wartosci z kolumny czas 
# dla modeli typu "A" w podanym pliku
def read_csv_file(path):
    try:
        file = open(path,"r")
        file_content = reader(file)
        next(file_content, None)

        time_sum = 0
        for row in file_content:
            row = row[0].replace("\n","").replace(" ","")
            row = row.split(";")
            if row[0] == 'A':
                time_sum += int(row[2][0:-1])
        print(time_sum)
        #return time_sum
    except FileNotFoundError:
        print("Nie istnieje plik: \""+path+"\"")
    except Exception as err:
        print("Wystąpił błąd: "+str(err))
    # print(0)
    #return 0

# Funkcja plik csv w podanym folderze
def generate_csv_file(path):
    try:
        file = open(path,"w")
        file.write("Model; Wynik; Czas;\n")

        x = ['A','B','C'][randint(0,2)]
        y = str(randint(0,1000))
        z = str(randint(0,1000))+'s'

        file.write(x+" ; "+y+" ; "+z+" ;")
    except Exception as err:
        print("Wystąpił błąd: "+str(err))
    file.close()

def read_json_file(path):
    with open(path, 'r') as file:
        data = json.load(file)

    try:
        if (data["Model"] == 'A'):
            print("Dane z ", path, ": ", data["Wynik"])
    except KeyError:
        print("Niepoprawny format danych!")

def generate_json_file(path):
    letters = ['A', 'B', 'C']

    data = {
        "Model": letters[randint(0, 2)],
        "Wynik": randint(0, 1000),
        "Czas": str(randint(0, 1000)) + "s"
    }

    with open(path, 'w') as file:
        json.dump(data, file)

# Funkcja odczytuje dane z plików w podanym folderze
# Jeżeli pliki nie istnieją wypisuje odpowiedni komunikat
def read_files(path, f_csv, f_json):
    if not (path/"Dane.csv").exists():
        print("Nie można odczytać zawartości pliku csv. Brak pliku w podanej ścieżce.")
    if f_csv:
        read_csv_file(path/"Dane.csv")

    if not (path/"Dane.json").exists():
        print("Nie można odczytać zawartości pliku json. Brak pliku w podanej ścieżce.")
    elif f_json:
        read_json_file(path/"Dane.json")

def generate_files(path, f_csv, f_json):
    if f_csv:
        if any(path.glob("*.csv")): #zapobiega duplikacji plików .csv
            print(f"Nie można utworzyć pliku. Plik .csv w {path} już istnieje.")
        else:
            generate_csv_file(path/"Dane.csv")

    if f_json:
        if any(path.glob("*.json")): #zapobiega duplikacji plików .json
            print(f"Nie można utworzyć pliku. Plik .json w {path} już istnieje.")
        else:
            generate_json_file(path/"Dane.json")

def create_folders_and_handle_files(paths, f_generate, f_read, f_csv, f_json): #te zmienne mają przechowywać dane wpisane z argparse (data i flagi)
    for path in paths: #ta pętla iteruje po ścieżkach i robi to, co zadały flagi (albo kiedy nie może tego zrobić to to komunikuje)
        path.mkdir(parents = True, exist_ok = True)

        if f_read:
            read_files(path, f_csv, f_json)

        if f_generate:
            generate_files(path, f_csv, f_json)
            
def find_key(dictionary, value): #funkcja do znajdywania kluczy po wartości, używam jej póżniej w zakresach dni
    for key in dictionary:
        if dictionary[key] == value:
            return key

DNI = ["pn", "wt", "śr", "cz", "pt", "sb", "nd"]

def days_range(d_range):
    first, _, last = d_range.partition("-")
    last = last or first                      # pojedynczy dzień = zakres d-d
    i, j = DNI.index(first), DNI.index(last)  # ValueError przy złym skrócie
    return [DNI[(i + k) % 7] for k in range((j - i) % 7 + 1)]

if __name__ == "__main__":
    main()
