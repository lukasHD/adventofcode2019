import day10
import unittest

inpA = """.#..#
.....
#####
....#
...##"""

inpB = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

inpC = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""

inpD = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""

inpE = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""




class TestRunner(unittest.TestCase):
    
    def test_day10_1_1(self):
        bestLocation, numVisible = day10.find_best_station(day10.get_astroids(inpA))
        self.assertEqual(bestLocation, (3,4))
        self.assertEqual(numVisible, 8)

    def test_day10_1_2(self):
        bestLocation, numVisible = day10.find_best_station(day10.get_astroids(inpB))
        self.assertEqual(bestLocation, (5,8))
        self.assertEqual(numVisible, 33)

    def test_day10_1_3(self):
        bestLocation, numVisible = day10.find_best_station(day10.get_astroids(inpC))
        self.assertEqual(bestLocation, (1,2))
        self.assertEqual(numVisible, 35)

    def test_day10_1_4(self):
        bestLocation, numVisible = day10.find_best_station(day10.get_astroids(inpD))
        self.assertEqual(bestLocation, (6,3))
        self.assertEqual(numVisible, 41)

    def test_day10_1_5(self):
        bestLocation, numVisible = day10.find_best_station(day10.get_astroids(inpE))
        self.assertEqual(bestLocation, (11,13))
        self.assertEqual(numVisible, 210)

if __name__ == '__main__':
    unittest.main()
