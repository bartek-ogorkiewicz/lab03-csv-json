# część generująca ścieżki i tworząca puste pliki json i csv (na tych ścieżkach) i odczytująca informacje z już istniejących plików na tych ścieżkach; to wszystko się dzieje w current directory
# przykładowy input: [miesiąc, miesiąc2], [pn-wt, pt], [r, w] -o -t -c -j
# przyjmuję, że miesiące zapisujemy z małej litery używając polskich znaków, a dni tygodnia skrótowo: pn, wt, śr, cz, pt, sb, nd; z kolei pory dnia "rano" lub "wieczór"

import argparse
from pathlib import Path
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

def generate_paths(months, days, time):
    paths = []
    
    for n in range(len(months)): #ta pętla tworzy wszystkie ścieżki wpisane z klawiatury i dodaje je do listy ścieżek
        if len(days[n]) > 2:
            days_list = days_range(days[n]) #przekazuje dane do funkcji, która ogarnia zakresy dni tygodnia
            for day in days_list:
                if time[n] is not None: 
                    time_n = time[n]
                else: time_n = "rano"
                path = Path.cwd()/months[n]/day/time_n
                paths.append(path)
        else:
            if time[n] is not None: 
                time_n = time[n]
            else: time_n = "rano"
            path = Path.cwd()/months[n]/days[n]/time_n
            paths.append(path)

    return paths

# Funkcja odczytuje i sumuje wartosci z kolumny czas 
# dla modeli typu "A" w podanym pliku
def read_csv_file(path):
    try:
        file = open(path+".csv","r")
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
    print(0)
    #return 0

# Funkcja plik csv w podanym folderze
def generate_csv_file(path):
    try:
        file = open(path+".csv","w")
        file.write("Model; Wynik; Czas;\n")

        x = ['A','B','C'][randint(0,2)]
        y = str(randint(0,1000))
        z = str(randint(0,1000))+'s'

        file.write(x+" ; "+y+" ; "+z+" ;")
    except Exception as err:
        print("Wystąpił błąd: "+str(err))

def read_json_file(path):
    # TODO: Osoba 4
    pass

def generate_json_file(path):
    # TODO: Osoba 4
    pass

# Funkcja odczytuje dane z plików w podanym folderze
# Jeżeli pliki nie istnieją wypisuje odpowiedni komunikat
def read_files(path, f_csv, f_json):
    if not (path/"Dane.csv").exists():
        print("Nie można odczytać zawartości pliku csv. Brak pliku w podanej ścieżce.")
    elif f_csv:
        read_csv_file(path/"Dane.csv")

    if not (path/"Dane.json").exists():
        print("Nie można odczytać zawartości pliku json. Brak pliku w podanej ścieżce.")
    if f_json:
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

def days_range(range): #ta funkcja generuje całe zakresy dni tygodnia z zapisów typu pn-nd
    days_of_the_week = {"pn": 1, "wt": 2, "śr": 3, "cz": 4, "pt": 5, "sb": 6, "nd": 7}
    days_list = []

    first = range[:2]
    last = range[3:]
    i = days_of_the_week[first]

    if first == last:
        return list(days_of_the_week.keys()) #jeśli użytkownik prosi o zakres np. nd-nd to dostaje cały tydzień

    while i != days_of_the_week[last] % 7 + 1:
        days_list.append(find_key(days_of_the_week, i))
        if i > 6:
            i = 0
        i+=1
    return days_list #zwraca liste ze wszystkimi dniami tygodnia znajdującymi się w zakresie

if __name__ == "__main__":
    main()
