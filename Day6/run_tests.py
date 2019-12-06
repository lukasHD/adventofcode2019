import day6
import unittest

test = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""


class TestRunner(unittest.TestCase):
    

    def test_day6_1_1(self):
        self.assertEqual(day6.getTotalOrbits(test), 42)


if __name__ == '__main__':
    unittest.main()