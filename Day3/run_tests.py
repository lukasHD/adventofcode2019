import day3
import unittest

# run tests like this `python -m unittest day1.py -v`


class TestRunner(unittest.TestCase):
    
    def test_day3_1_1(self):
        self.assertEqual(day3.runPartOne(["R8","U5","L5","D3"],["U7","R6","D4","L4"]), 6)
    
    def test_day3_1_2(self):
        self.assertEqual(day3.runPartOne(["R75","D30","R83","U83","L12","D49","R71","U7","L72"],["U62","R66","U55","R34","D71","R55","D58","R83"]), 159)

    def test_day3_1_3(self):
        self.assertEqual(day3.runPartOne(["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"],["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]), 135)

if __name__ == '__main__':
    unittest.main()