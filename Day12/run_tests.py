import day12
import unittest

class TestRunner(unittest.TestCase):
    
    def test_day11_1_1(self):
        ret = day12.run_small_test2()
        self.assertEqual(ret, 4686774924)

if __name__ == '__main__':
    unittest.main()
