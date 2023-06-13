# Dokumentacja testowa

## a. Struktura systemu lub aplikacji

Plik `test_main.py` zawiera zestaw testów jednostkowych dla kluczowych komponentów aplikacji. Jest to plik testowy powiązany z plikiem `main.py`, który zawiera implementację funkcji i klas. Testy sprawdzają poprawność działania poszczególnych funkcji i klas w systemie.

## b. Scenariusze testów

Poniżej przedstawione są szczegółowe scenariusze testów:

### Test `test_get_user_input`

Scenariusz testu:
1. Symulacja wprowadzenia wartości `'abc'` przez użytkownika.
   - Oczekiwany wynik: Funkcja `get_user_input()` powinna zwrócić wartość `'abc'` i nie powinna wypisywać żadnych danych na standardowe wyjście.
2. Symulacja wprowadzenia wartości `'12'` przez użytkownika.
   - Oczekiwany wynik: Funkcja `get_user_input()` powinna zwrócić wartość `12` (jako obiekt typu `int`) i nie powinna wypisywać żadnych danych na standardowe wyjście.
3. Symulacja wprowadzenia wartości `'3.14'` przez użytkownika.
   - Oczekiwany wynik: Funkcja `get_user_input()` powinna zwrócić wartość `3.14` (jako obiekt typu `float`) i nie powinna wypisywać żadnych danych na standardowe wyjście.

### Testy dla klas `Vehicle`, `Car` i `Bus`

Scenariusze testów dla klas reprezentujących różne rodzaje pojazdów:

1. Test dla klasy `Vehicle`:
   - Tworzenie obiektu `Vehicle` z określonymi parametrami.
   - Sprawdzenie, czy metoda `get_price()` zwraca oczekiwaną wartość.
   - Sprawdzenie, czy metoda `__str__()` zwraca oczekiwany opis pojazdu.

2. Test dla klasy `Car`:
   - Tworzenie obiektu `Car` z określonymi parametrami.
   - Sprawdzenie, czy metoda `get_price()` zwraca oczekiwaną wartość.
   - Sprawdzenie, czy atrybut `wheels` ma wartość `4`.
   - Sprawdzenie, czy metoda `__str__()` zwraca oczekiwany opis samochodu.

3. Test dla klasy `Bus`:
   - Tworzenie obiektu `Bus` z określonymi parametrami.
   - Sprawdzenie, czy metoda `get_price()` zwraca oczekiwaną wartość.
   - Sprawdzenie, czy atrybut `wheels` ma wartość `6`.
   - Sprawdzenie, czy metoda `__str__()` zwraca oczekiwany opis autobusu.

### Testy innych funkcji i klas

Scenariusze testów dla innych funkcji i klas:

- Testy dla klasy `Offer`, `Bot` i funkcji `get_user_decision`, które sprawdzają poprawność działania poszczególnych metod i funkcji.
- Wszystkie testy powinny zakończyć się sukcesem (wszystkie asercje powinny być spełnione).

## c. Wykorzystane narzędzia i biblioteki

Do wykonania testów jednostkowych wykorzystano następujące narzędzia i biblioteki:
- `unittest` - biblioteka standardowa języka Python do tworzenia i uruchamiania testów jednostkowych.
- `unittest.mock` - moduł biblioteki `unittest` do tworzenia atrap obiektów i ich metod w celu testowania.
- `StringIO` - klasa z modułu `io`, która umożliwia manipulację strumieniami tekstowymi.

## d. Ewentualne problemy i ich rozwiązania

Podczas pisania testów wystąpiły następujące problemy:

1. Problem z symulacją danych wejściowych:
   - Rozwiązanie: Wykorzystano moduł `unittest.mock` do atrapowania funkcji `input()` i przekazywania oczekiwanych wartości.
2. Problem z porównywaniem wyników:
   - Rozwiązanie: Wykorzystano metody asercji z biblioteki `unittest` do porównywania oczekiwanych i rzeczywistych wyników.