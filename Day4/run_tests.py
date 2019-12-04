import day4
import unittest

# run tests like this `python -m unittest day1.py -v`


class TestRunner(unittest.TestCase):

    def test_hasDouble(self):
        self.assertEqual(day4.hasDouble("123456") , False)
        self.assertEqual(day4.hasDouble("113456") , True)
        self.assertEqual(day4.hasDouble("122456") , True)
        self.assertEqual(day4.hasDouble("123356") , True)
        self.assertEqual(day4.hasDouble("123446") , True)
        self.assertEqual(day4.hasDouble("123466") , True)

    def test_isValidPassword(self):
        self.assertEqual(day4.isValidPassword(111111), True)
        self.assertEqual(day4.isValidPassword(223450), False)
        self.assertEqual(day4.isValidPassword(123789), False)

    def test_decreases(self):
        self.assertEqual(day4.Decreases("545555"), True)
        self.assertEqual(day4.Decreases("554555"), True)
        self.assertEqual(day4.Decreases("555455"), True)
        self.assertEqual(day4.Decreases("555545"), True)
        self.assertEqual(day4.Decreases("555554"), True)
        self.assertEqual(day4.Decreases("555555"), False)


if __name__ == '__main__':
    unittest.main()