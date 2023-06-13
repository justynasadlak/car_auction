import unittest
from unittest.mock import patch
from io import StringIO
from main import *

class TestMain(unittest.TestCase):
    def test_get_user_input(self):
        with patch('builtins.input', return_value='abc'), patch('sys.stdout', new=StringIO()) as mock_stdout:
            result = get_user_input('Enter a value: ', str)
            self.assertEqual(result, 'abc')
            self.assertEqual(mock_stdout.getvalue().strip(), '')

        with patch('builtins.input', return_value='12'), patch('sys.stdout', new=StringIO()) as mock_stdout:
            result = get_user_input('Enter a value: ', int)
            self.assertEqual(result, 12)
            self.assertEqual(mock_stdout.getvalue().strip(), '')

        with patch('builtins.input', return_value='3.14'), patch('sys.stdout', new=StringIO()) as mock_stdout:
            result = get_user_input('Enter a value: ', float)
            self.assertEqual(result, 3.14)
            self.assertEqual(mock_stdout.getvalue().strip(), '')

    def test_Vehicle(self):
        vehicle = Vehicle('Toyota', 'Corolla', 2022, 25000)
        self.assertEqual(vehicle.get_price(), 25000)
        self.assertEqual(str(vehicle), 'ABSTRACT RUNNER Toyota Corolla z 2022r. - 25000zł')

    def test_Car(self):
        car = Car(brand='Seat', model='Ibiza', year=2021, price=15000)
        self.assertEqual(car.get_price(), 15000)
        self.assertEqual(car.wheels, 4)
        self.assertEqual(str(car), 'SAMOCHÓD OSOBOWY Seat Ibiza z 2021r. - 15000zł')

    def test_Bus(self):
        bus = Bus(brand='Volvo', model='B10M', year=1999, price=50000)
        self.assertEqual(bus.get_price(), 50000)
        self.assertEqual(bus.wheels, 6)
        self.assertEqual(str(bus), 'AUTOBUS Volvo B10M z 1999r. - 50000zł')

    def test_Offer(self):
        offer = Offer(100, 'Vehicle')
        self.assertEqual(offer.get_price(), 100)
        self.assertIsNone(offer.get_person())
        offer.bid_price(150, 'John')
        self.assertEqual(offer.get_price(), 150)
        self.assertEqual(offer.get_person(), 'John')
        self.assertEqual(offer.get_result(), 'Vehicle zgarnął John za kwotę bagatela 150! Gratulacje.')

    def test_Bot(self):
        bot = Bot('John')
        self.assertFalse(bot.running)
        bot.request_leave()
        self.assertFalse(bot.running)
        bot.add_own('Car')
        self.assertEqual(bot.owns, ['Car'])
        bot.show_offer(None)
        self.assertIsNone(bot.offer)

    @patch('builtins.input', return_value=0)
    def test_get_user_decision(self, mock_input):
        result = get_user_decision()
        self.assertEqual(result, 0)

    
    def test_Offer_interested_above_1(self):
        offer = Offer(100, 'Vehicle')
        self.assertFalse(offer.interested_above_1())

        offer.vote_interested('John')
        self.assertFalse(offer.interested_above_1())

        offer.vote_interested('Alice')
        self.assertTrue(offer.interested_above_1())

    def test_Offer_bid_price(self):
        offer = Offer(100, 'Vehicle')

        offer.bid_price(120, 'John')
        self.assertEqual(offer.get_price(), 120)
        self.assertEqual(offer.get_person(), 'John')

        offer.bid_price(110, 'Alice')
        self.assertEqual(offer.get_price(), 120)  # Price should remain unchanged
        self.assertEqual(offer.get_person(), 'John')  # Person should remain unchanged

if __name__ == '__main__':
    unittest.main()
