# część generująca ścieżki i tworząca puste pliki json i csv (na tych ścieżkach) i odczytująca informacje z już istniejących plików na tych ścieżkach; to wszystko się dzieje w current directory
# przykładowy input: [miesiąc, miesiąc2], [pn-wt, pt], [r, w] -o -t -c -j
# przyjmuję, że miesiące zapisujemy z małej litery używając polskich znaków, a dni tygodnia skrótowo: pn, wt, śr, cz, pt, sb, nd; z kolei pory dnia "rano" lub "wieczór"

from pathlib import Path

def generate_paths_and_files_and_read_files(months, days, time, f_generate, f_read, f_csv, f_json): #te zmienne mają przechowywać dane wpisane z argparse (data i flagi)
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

    for path in paths: #ta pętla iteruje po ścieżkach i robi to, co zadały flagi (albo kiedy nie może tego zrobić to to komunikuje)
        if f_read and f_csv and (path/"Dane.csv").exists() == True: #odczytuje zawartość plików w podanej ścieżce
                print(path)
                file = open(path/"Dane.csv")
                for line in file:
                    print(line)
                file.close()
        
        if f_read and f_json and (path/"Dane.json").exists() == True: #odczytuje zawartość plików w podanej ścieżce
            print(path)
            file = open(path/"Dane.json")
            for line in file:
                print(line)
            file.close()

        if f_read == True and path.exists() == False: #daje komunikat gdy chcemy odczytać plik, którego nie ma
                print("Nie można odczytać zawartości pliku. Brak pliku w podanej ścieżce.")
               
        if f_generate and f_csv and any(path.glob("*.csv")) == True: #zapobiega duplikacji plików .csv
                print(f"Nie można utworzyć pliku. Plik .csv w {path} już istnieje.")

        if f_generate and f_json and any(path.glob("*.json")) == True: #zapobiega duplikacji plików .json
                print(f"Nie można utworzyć pliku. Plik .json w {path} już istnieje.")

        if f_generate and f_csv == True and path.exists() == False: #tworzy pusty plik .csv
                path.mkdir(parents = True, exist_ok = True)
                file = Path(path/"Dane.csv")
                file.touch()
                print(f"Utworzono plik Dane.csv w {path}")

        if f_generate and f_json == True and path.exists() == False: #tworzy pusty plik .json
                path.mkdir(parents = True, exists_ok = True)
                file = Path(path/"Dane.json")
                file.touch()
                print(f"Utworzono plik Dane.json w {path}")

def find_key(dictionary, value): #funkcja do znajdywania kluczy po wartości, używam jej póżniej w zakresach dni
    for key in dictionary:
        if dictionary[key] == value:
            return key

def days_range(range): #ta funkcja generuje całe zakresy dni tygodnia z zapisów typu pn-nd
    days_of_the_week = {"pn":1, "wt":2, "śr":3, "cz":4, "pt":5, "sb":6, "nd":7}
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