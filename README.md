# Lubimyczytac.pl Scraper

**Polish version available below**

Unlike other popular reading trackers, lubimyczytac.pl does not allow its users to export their data.

This is a scraper that goes over the user's public profile to extract their reading history. This can be converted to a goodreads library format, allowing the user to import their library to other tracking apps that support it.

## Instructions

### Pre-requistes

You will need to install:

- python
- chromedriver (https://googlechromelabs.github.io/chrome-for-testing/)

### Usage

Clone the repository:

```console
git clone https://github.com/dominika01/lubimyczytac-scraper.git
```

In main.py, set:

```py
url = "your profile url" # Moje konto -> Biblioteczka -> Generuj link (on the right side)
num_pages = 1 # replace with the number of pages your profile has
half_stars = False # replace with true if importing data to an app supporting half star ratings
driver_path = "path/to/chromedriver" # path to your chromedriver
```

Run the script:

```console
python main.py
```

This will generate two files:

- *library.csv* containing the data from your library
- *gr_library.csv* containing the data formatted to match Goodreads

You can upload *gr_library.csv* to most popular book tracking apps like Goodreads or Storygraph to import your Lubimyczytac library.

## Instrukcje po polsku

Kod umożliwia zebranie danych z publicznego profilu uzytkownika na lubimyczytac.pl i zapisania ich w osobnym pliku. Te dane mogą być zaimportowane na inne popularne portale czytelnicze.

### Wymania

Najpierw zainstaluj:

- python
- chromedriver (https://googlechromelabs.github.io/chrome-for-testing/)

### Użycie

Zklonuj to repozytorium:

```console
git clone https://github.com/dominika01/lubimyczytac-scraper.git
```

W pliku main.py, zamień dane:

```py
url = "link do profilu" # Moje konto -> Biblioteczka -> Generuj link (po prawej stronie)
num_pages = 1 # zamien na liczbe stron na twoim profilu
half_stars = False # zamien na True jesli importujesz dane na strone ktora uzywa ocen majacych polowe gwiazdki
driver_path = "path/to/chromedriver" # sciezka do twojego chromedriver
```

Uruchom kod:

```console
python main.py
```

To wygeneruje dwa pliki:

- *library.csv* zawiera dane z twojej biblioteki
- *gr_library.csv* zawiera te dane w formacie Goodreads

Plik *gr_library.csv* można wykorzystać do importu danych na większości aplikacji czytelniczych, takich jak Goodreads lub Storygraph.
