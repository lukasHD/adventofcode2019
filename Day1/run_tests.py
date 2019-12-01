import day1
import unittest

# run tests like this `python -m unittest day1.py -v`


class TestClass(unittest.TestCase):
    
    def test_day1_1_1(self):
        a = day1.module(12)
        self.assertEqual(a.requiredFuel(), 2)
    def test_day1_1_2(self):
        a = day1.module(14)
        self.assertEqual(a.requiredFuel(), 2)
    def test_day1_1_3(self):
        a = day1.module(1969)
        self.assertEqual(a.requiredFuel(), 654)
    def test_day1_1_4(self):
        a = day1.module(100756)
        self.assertEqual(a.requiredFuel(), 33583)


class TestMethods(unittest.TestCase):
    
    def test_day1_1_5(self):
        self.assertEqual(day1.calcFuel(12), 2)
    def test_day1_1_6(self):
        self.assertEqual(day1.calcFuel(14), 2)
    def test_day1_1_7(self):
        self.assertEqual(day1.calcFuel(1969), 654)
    def test_day1_1_8(self):
        self.assertEqual(day1.calcFuel(100756), 33583)

class TestFullFuel(unittest.TestCase):

    def test_day1_2_1(self):
        self.assertEqual(day1.calcFullFuel(14), 2)
    def test_day1_2_2(self):
        self.assertEqual(day1.calcFullFuel(1969), 966)
    def test_day1_2_3(self):
        self.assertEqual(day1.calcFullFuel(100756),50346)
    def test_negative_full_fuel(self):
        self.assertEqual(day1.calcFullFuel(-10),0)
    def test_zero_full_fuel(self):
        self.assertEqual(day1.calcFullFuel(0),0)

if __name__ == '__main__':
    unittest.main()