""" Program-prezentacja na zajęcia """
from abc import ABC
import random
import time
from threading import Thread

# Stworzylam funkcje rekurencyjna do obslugi licytacji w celu patrz linia 7
def serve(offer, level=0):
    ''' Funkcja obsługi licytacji, przyjmuje ofertę.
    Level oznacza poziom licytacji:
    0 - po raz pierwszy
    1 - po raz drugi
    2 - po raz trzeci (ostatni). '''
    price = offer.get_price()
    time.sleep(2.5) #kod wykonywany po 2.5s.
    if price != offer.get_price(): #warunek spełnniony, gdy cenę zmieni inny licytujący
        return serve(offer)

    if offer.get_person() is not None: #jeśli ktoś złozył ofertę, wyświetlany jest komunikat zgodny z poziomem licytacji oraz zawierający kwotę z oferty
        print(f'{offer.get_price()} po raz {["pierwszy.", "drugi!", "TRZECI!"][level]}')
    else: #jeśli nikt nie złozył oferty, wyświetlany jest komunikat zgodny z poziomem licytacji
        print(f'Czy będą jakieś oferty? Po raz {["pierwszy.", "drugi!", "TRZECI!"][level]}')

    if level == 2: #na ostatnim poziomie licytacji wyświetlany jest komunikat zalezny od tego czy ktoś złozył ofertę
        print('Sprzedane!' if offer.get_person() is not None else 'Zamykam licytację.')
        return offer

    return serve(offer, level+1) #funkacja wywoływana z kolejnym poziomem licytacji

TS = 0 #licznik czasu
def sum_time(func):
    ''' Dekorator kumulujący czas '''
    def wrapper(*a, **kwa):
        global TS
        t0 = time.time()
        v = func(*a, **kwa)
        TS += time.time()-t0
        return v

    return wrapper

# Uzylam wrappera do liczenia sumarycznego czasu wybierania przez uzytkownika
# poniewaz to najschludniejsza forma, przenoszaca logike dzialani wgłąb '''
@sum_time
def get_user_input(msg: str, return_type: type, options: list = None, flags: list = None):
    ''' type jest callable, więc mozemy potraktować tę funkcję jako wyższego rzędu '''
    while True:
        value = input(msg)

        try:
            value_cast = return_type(value)

            error_displayed = False  # Flag to track if an error message has been displayed

            if options is not None and len(options):
                if value_cast not in options:
                    print(f'Podaj jedną z dostępnych wartości: {", ".join(map(str, options))}')
                    error_displayed = True

            if flags is not None and len(flags):
                if ('Positive' in flags) and return_type in [int, float]:
                    if value_cast <= 0:
                        print('Podaj dodatnią wartość.')
                        error_displayed = True

                if ('NotEmpty' in flags) and return_type in [str]:
                    if len(value_cast) == 0:
                        print('Musisz coś wpisać...')
                        error_displayed = True

                    if value_cast.isspace():
                        print('Naprawdę musisz coś wpisać...')
                        error_displayed = True

            if not error_displayed:  # Return the value only if no error message has been displayed
                return value_cast

        except ValueError:
            print('Niepoprawna wartość')

# @sum_time
# def get_user_input(msg: str, return_type: type, options: list = None, flags: list = None):
#     ''' type jest callable, więc mozemy potraktować tę funkcję jako wyzszego rzędu '''
#     while True:
#         value = input(msg) #wyświetlenie komunikatu przekazanego w parametrze msg i pobranie wartości wpisanej przez uzytkownika

#         try:
#             value_cast = return_type(value) #sprawdzenie czy wpisana wartość jest oczekiwanego typu

#             if options is not None and len(options): 
#                 if value_cast not in options: #jeśli wpisana wartość nie jest jedną z oczekiwanych wartości, wyświetlenie komunikatu z dopuszczalnymi wartościami i kontynuacja kolejnej iteracji
#                     print(f'Podaj jedną z dostępnych wartości: {", ".join(map(str, options))}')
#                     continue

#             if flags is not None and len(flags):
#                 if ('Positive' in flags) and return_type in [int, float]:
#                     if value_cast <= 0: #wyświetlenie komunikatu, jeśli wpisana wartość nie jest dodatnia w przypadku flagi 'Positive' i oczekiwanego typu int, float; kontynuacja kolejnej iteracji
#                         print('Podaj dodatnią wartość.')
#                         continue

#                 if ('NotEmpty' in flags) and return_type in [str]:
#                     if len(value_cast) == 0: #wyświetlenie komunikatu, jeśli nic nie zostało wpisane w przypadku flagi 'NotEmpty' i oczekiwanego typu string; kontynuacja kolejnej iteracji
#                         print('Musisz coś wpisać...')
#                         continue

#                     if value_cast.isspace(): #wyświetlenie komunikatu, jeśli wpisano tylko białe znaki; kontynuacja kolejnej iteracji
#                         print('Naprawdę musisz coś wpisać...')
#                         continue

#             return value_cast
#         except ValueError: #obsługa wyjątku wpisania wartości w innym typie niz oczekiwany
#             print('Niepoprawna wartość')


class Vehicle(ABC):
    ''' Klasa abstrakcyjna pojazdu ogólnego'''
    def __init__(self, brand: str, model: str, year: int, price: float) -> None:
        self.brand = brand
        self.model = model
        self.year = year
        self.vehicle_type = "ABSTRACT RUNNER"
        self.wheels = -1
        self.price = price

    def get_price(self):
        ''' Zwraca cenę pojazdu '''
        return self.price

    def __str__(self):
        ''' reprezentacja obiektu klasy w postaci stringa '''
        return f'{self.vehicle_type} {self.brand} {self.model} z {self.year}r. - {self.price}zł'

class Car(Vehicle):
    ''' Klasyczny samochód osobowy. Dziedziczy po klasie Vehicle '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vehicle_type = "SAMOCHÓD OSOBOWY"
        self.wheels = 4 #liczba kół

class Bus(Vehicle):
    ''' Klasyczny bus wieloosobowy. Dziedziczy po klasie Vehicle '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vehicle_type = "AUTOBUS"
        self.wheels = 6 #liczba kół

class Offer:
    ''' Oferta do licytacji. W konstruktorze przekazujemy kwotę i wybraną ofertę '''
    def __init__(self, price, item) -> None:
        self.price = price
        self.item = item
        self.person = None
        self.last_bid_time = None
        self.interested = [] #zainteresowani ofertą

    def get_price(self):
        ''' Zwraca kwotę oferty '''
        return self.price

    def get_person(self):
        ''' Zwraca osobę będącą właścicielem proponowanej kwoty '''
        return self.person

    def get_last_bid_time(self):
        return self.last_bid_time

    def vote_interested(self, person):
        ''' Dodaje do listy zainteresowanych ofertą osobę przekazaną w parametrze person, aby móc sprawdzić ilu jest zainteresowanych ofertą '''
        self.interested.append(person)

    def interested_above_1(self):
        ''' Zwraca czy jest więcej niz jedna osoba zainteresowana ofertą, aby tylko w takim przypadku uruchomić licytację '''
        return len(self.interested)>1

    def bid_price(self, price, person):
        ''' Licytowanie '''
        if id(person) == id(self.person): #sprawdzenie czy ten sam uzytkownik próbuje przebić swoją ofertę, jeśli tak - koniec funkcji
            return

        if price >= self.price * 1.1: #warunek proponowana kwota musi być wyzsza o min. 10% aktualnej kwoty
            self.price = round(price, 2) #nowa cena oferty zaokrąglona do 2 miejsc po przecinku
            self.person = person #przypisanie osoby do oferty
            print(f'Cena podbita do {self.price} przez {self.person}') #wyświetlenie komunikatu zawierającego nową cenę oferty i jej właściciela
        else:
            print(f'{person} próbował podbić cenę, niestety nie wystarczającą kwotą.')

    def get_result(self):
        ''' Zwraca wynik licytacji, którego treść zalezna jest od tego czy ktoś został przypisany do oferty '''
        if self.person is None:
            return f'Nikt nie wygrał {self.item}'

        return f'{self.item} zgarnął {self.person} za kwotę bagatela {self.price}! Gratulacje.'


class Bot(Thread):
    ''' Klasa bot dziedziczy po Thread, aby tworzyć wątki. Bot jest uczestnikiem licytacji '''
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.running = False #decyduje czy Bot jest w trakcie działania
        self.offer = None #aktualnie otwarta do licytowania oferta
        self.owns = [] #oferty wygrane przez Bota

    def request_leave(self):
        ''' Zakończenie działania Bota'''
        self.running = False

    def add_own(self, own: str):
        ''' Dodanie wygranej oferty do właściciela '''
        self.owns.append(own)

    def show_offer(self, offer):
        ''' Randomowo ustala zainteresowanych ofertą '''
        if offer is None:
            self.offer = None
        elif random.randint(0, 1) == 0: #jeśli wylosowana wartość to 0, dodaje Bota do listy zainteresowanych ofertą
            if len(self.owns) > 0:
                print(f'{self}, właściciel {", ".join(self.owns)} wygląda na zainteresowanego.')
            else:
                print(f'{self} wygląda na zainteresowanego.')
            self.offer = offer
            self.offer.vote_interested(self) #Dodaje Bota do listy zainteresowanych ofertą

    def run(self):
        ''' Nadpisanie metody run(), czyli co wątek powinien zrobić po uruchomieniu '''
        self.running = True #rozpoczęcie działania Bota
        print(f'{self.name} wchodzi do programu')

        while self.running: #dopóki Bot działa
            if self.offer is not None:
                if random.randint(0, 10) == 0: #jeśli wylosowana liczba jest równa 0
                    new_price = self.offer.get_price() * (random.randint(101, 130)/100) #kwota oferty podniesiona o 1%-30%
                    self.offer.bid_price(new_price, self) #próbwa podbicia oferty nową kwotą

            time.sleep(1) #kontynuacja po 1s

        print(f'{self} opuszcza program') #komunikat po zakończeniu działania Bota

    def __str__(self):
        return f'Bot {self.name}'

def get_user_decision():
    ''' Pobranie decyzji uzytkownika. 
    W pierwszym parametrze przekazana jest wiadomość do wyświetlenia, 
    w drugim parametrze oczekiwany typ wprowadzonej przez uzytkownika wartości,
    w trzecim parametrze dopuszczalne wartości, które mogą zostać wpisane przez uzytkownika '''
    return get_user_input('''
        1 - dodaj ofertę,
        2 - przeglądaj ofery
        3 - otwórz licytację

        0 - zakończ
    <wybór>:''', int, [0, 1, 2, 3])

def main():
    ''' Metoda główna '''
    print(''' Witaj w systemie aukcji pojazdów róznego typu (tylko samochody i autobusy). ''')

    vehicles = [ #utworzenie początkowej listy ofert pojazdów
        Car(**{
            'brand': 'Seat',
            'model': 'Eebiza',
            'year': random.randint(2000, 2020),
            'price': random.randint(5000, 100000)
        }),
        Bus(**{
            'brand': 'Seat',
            'model': 'Busbiza',
            'year': random.randint(2000, 2020),
            'price': random.randint(5000, 100000)
        }),
        Bus(**{
            'brand': 'Yeah',
            'model': 'Hell',
            'year': random.randint(2000, 2020),
            'price': random.randint(5000, 100000)
        }),
    ]

    bots = [Bot('Johnny'), Bot('Heard'), Bot('Somenoise'), Bot('Ambier'), Bot('Justyna')] #utworzenie listy botów, które będą licytować
    _ = [bot.start() for bot in bots] #uruchamia nowy wątek poprzez wywołanie metody start(), która wywołuje metodę run(); _ zapis wyciszający pylint

    # Pętla główna programu
    while True:
        user_input = get_user_decision()

        # Podmenu tworzenia pojazdu
        if user_input == 1:
            print('Tworzenie pojazdu. W dowolnym momencie wprowadź 0, aby anulować.')
            vehicle = get_user_input('Podaj typ (A - Autobus, O - Osobowy): ', str, ['A', 'O', '0'])
            if vehicle == '0':
                continue
            brand = get_user_input('Podaj markę: ', str, flags=['NotEmpty'])
            if brand == '0':
                continue
            model = get_user_input('Podaj model: ', str, flags=['NotEmpty'])
            if model == '0':
                continue
            year = get_user_input('Podaj rok produkcji: ', int, flags=['Positive'])
            if year == 0:
                continue
            price = get_user_input('Podaj cenę pojazdu: ', float, flags=['Positive'])
            if price == 0:
                continue

            cls = Bus if vehicle == 'A' else Car #ustalenie jakiej klasy zostanie utworzony obiekt na podstawie wartości podanej przez uzytkownika; 
            #jeśli uzytkownik wpisał 'A', to zostanie utworzony obiekt klasy Autobus, a w innym przypadku obiekt klasy Car
            obj = cls(**{'brand': brand, 'model': model, 'year': year, 'price': price})

            accept = get_user_input(f'Zatwierdzić "{obj}"? [T/N]: ', str, options=['T', 'N'])
            if accept == 'N': #jeśli uzytkownik wpisał N, to zostanie uruchomiona kolejna iteracja, a jeśli T, to zostanie dodana nowa oferta pojazdu
                continue

            print(f'Oferta dodana: {obj}')
            vehicles.append(obj)

        # Dzielona lista ofert dla podglądu i rozpoczęcia licytacji
        elif user_input in [2, 3]:
            if len(vehicles) == 0:
                print('Brak ofert.')
                continue

            opts = [-1] #opcje do wyboru, -1 dla powrotu
            for opt, obj in enumerate(vehicles):
                print(f'{opt} - {obj}')
                opts.append(opt)

            # Wybór oferty do licytowania
            if user_input == 3:
                print('-1 - wróć')
                offer_choice = get_user_input('Wybierz ofertę: ', int, options=opts)
                if offer_choice == -1:
                    continue

                obj = vehicles[offer_choice]
                print('Wybrany pojazd: == ', obj, ' ==')

                offer = Offer(obj.get_price(), f'{obj}')
                _ = [bot.show_offer(offer) for bot in bots] # ustalenie zainteresowanych ofertą; _ zapis wyciszający pylint

                print('Otwieramy licytację...')
                time.sleep(2)

                if not offer.interested_above_1():
                    print('Niestety małe zainteresowanie. Przekładamy na kiedy indziej.')
                    _ = [bot.show_offer(None) for bot in bots] # zresetowanie wszystkim Botom oferty na którą aktualnie trwa licytacja; jeśli zainteresowanych nie jest min. 2 rezygnujemy z licytacji tej oferty;
                    continue

                serve(offer)

                person = offer.get_person()
                if person is not None:
                    person.add_own(f'{obj}') #dodaje wygraną ofertę do ofert uzytkownika
                    del vehicles[offer_choice] #usuwa ofertę z listy ofert dostępnych do licytacji

                _ = [bot.show_offer(None) for bot in bots] # zresetowanie wszystkim Botom oferty na którą aktualnie trwa licytacja;
                print(offer.get_result())

        elif user_input == 0: #zakończenie działania programu
            print('Dziękuje, do zobaczenia.')
            break

    _ = [bot.request_leave() for bot in bots]

    for bot in bots:
        bot.join() #blokuje wątek wywołujący do czasu gdy wątki bot zakończą się

    print('[end]')
    print(f'Suma czasu na decydowanie się w menu: {round(TS, 1)}s.')

if __name__ == '__main__':
    main()
 