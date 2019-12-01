# https://adventofcode.com/2019/day/1

# run tests like this `python -m unittest day1.py -v`

import unittest

class TestMethods(unittest.TestCase):
    
    def test_day1_1(self):
        a = module(12)
        self.assertEqual(a.requiredFuel(), 2)
    def test_day1_2(self):
        a = module(14)
        self.assertEqual(a.requiredFuel(), 2)
    def test_day1_3(self):
        a = module(1969)
        self.assertEqual(a.requiredFuel(), 654)
    def test_day1_4(self):
        a = module(100756)
        self.assertEqual(a.requiredFuel(), 33583)
        

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
    #unittest.main()