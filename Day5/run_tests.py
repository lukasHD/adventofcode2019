import day5
import unittest

# run tests like this `python -m unittest day1.py -v`


class TestRunner(unittest.TestCase):
    
    def test_day2_1_1(self):
        self.assertEqual(day5.runIntcode([1,9,10,3,2,3,11,0,99,30,40,50]), [3500,9,10,70,2,3,11,0,99,30,40,50])

    def test_day2_1_2(self):
        self.assertEqual(day5.runIntcode([1,0,0,0,99]), [2,0,0,0,99])
    
    def test_day2_1_3(self):
        self.assertEqual(day5.runIntcode([2,3,0,3,99]), [2,3,0,6,99])

    def test_day2_1_4(self):
        self.assertEqual(day5.runIntcode([2,4,4,5,99,0]), [2,4,4,5,99,9801])

    def test_day2_1_5(self):
        self.assertEqual(day5.runIntcode([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])

if __name__ == '__main__':
    unittest.main()