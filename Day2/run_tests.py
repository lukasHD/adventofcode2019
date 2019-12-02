import day2
import unittest

# run tests like this `python -m unittest day1.py -v`


class TestRunner(unittest.TestCase):
    
    def test_day2_1_1(self):
        self.assertEqual(day2.runIntcode([1,9,10,3,2,3,11,0,99,30,40,50]), [3500,9,10,70,2,3,11,0,99,30,40,50])
    
if __name__ == '__main__':
    unittest.main()