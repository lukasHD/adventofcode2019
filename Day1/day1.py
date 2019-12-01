# https://adventofcode.com/2019/day/1

# run tests like this `python -m unittest day1.py -v`

import unittest

class TestClass(unittest.TestCase):
    
    def test_day1_1_1(self):
        a = module(12)
        self.assertEqual(a.requiredFuel(), 2)
    def test_day1_1_2(self):
        a = module(14)
        self.assertEqual(a.requiredFuel(), 2)
    def test_day1_1_3(self):
        a = module(1969)
        self.assertEqual(a.requiredFuel(), 654)
    def test_day1_1_4(self):
        a = module(100756)
        self.assertEqual(a.requiredFuel(), 33583)


class TestMethods(unittest.TestCase):
    
    def test_day1_1_5(self):
        self.assertEqual(calcFuel(12), 2)
    def test_day1_1_6(self):
        self.assertEqual(calcFuel(14), 2)
    def test_day1_1_7(self):
        self.assertEqual(calcFuel(1969), 654)
    def test_day1_1_8(self):
        self.assertEqual(calcFuel(100756), 33583)

class TestFullFuel(unittest.TestCase):

    def test_day1_2_1(self):
        self.assertEqual(calcFullFuel(14), 2)
    def test_day1_2_2(self):
        self.assertEqual(calcFullFuel(1969), 966)
    def test_day1_2_3(self):
        self.assertEqual(calcFullFuel(100756),50346)
    def test_negative_full_fuel(self):
        self.assertEqual(calcFullFuel(-10),0)
    def test_zero_full_fuel(self):
        self.assertEqual(calcFullFuel(0),0)
    

def calcFuel(mass):
    fuel = int(mass / 3) - 2
    return max(0, fuel)

# def calcFullFuel(mass):
#     fuel = calcFuel(mass)
#     if fuel < 0:
#         fuel = 0
#     print("For mass {} required Fuel is {}".format(mass, fuel))
#     else:
#         additionalFuel = calcFullFuel(fuel)
#         if additionalFuel > 0:
#             fuel = fuel + calcFullFuel(fuel)
#     return fuel

def calcFullFuel(mass):
    '''
    Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. However, that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel should instead be treated as if it requires zero fuel; the remaining mass, if any, is instead handled by wishing really hard, which has no mass and is outside the scope of this calculation.
    '''
    if mass <= 0:
        return 0
    else:
        fuel = calcFuel(mass)
        print ("Fuel: {}".format(fuel))
        return fuel + calcFullFuel(fuel)

class module:
    def __init__(self, mass=0):
        self.mass = mass

    def requiredFuel(self):
        return int(self.mass / 3) - 2

    def print_fuel(self):
        print("For mass {} required Fuel is {}".format(a.mass, a.requiredFuel()))


def inputToIntList(fname='input'):
    intList = []
    with open(fname, 'r') as f:
        for line in f:
            intList.append(int(line))
    return intList

if __name__ == '__main__':
    modulMasses = inputToIntList()
    for mass in modulMasses:
        #print(mass)
        a = module(mass)
        a.print_fuel()
    print ("______________")
    #fuelcalculator = lambda x: calcFuel(x)
    fuelList = list(map(lambda x: calcFuel(x), modulMasses))
    print(fuelList)
    print(sum(fuelList)) #should return 3299598
    #unittest.main()