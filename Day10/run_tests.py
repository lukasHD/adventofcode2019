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

    def test_angle(self):
        self.assertEqual(day10.get_angle((0,0),(0,1)), 180)
        self.assertEqual(day10.get_angle((0,0),(1,1)), 135)
        self.assertEqual(day10.get_angle((0,0),(1,0)), 90)
        self.assertEqual(day10.get_angle((0,0),(1,-1)), 45)
        self.assertEqual(day10.get_angle((0,0),(0,-1)), 0)
        self.assertEqual(day10.get_angle((0,0),(-1,-1)), 315)
        self.assertEqual(day10.get_angle((0,0),(-1,0)), 270)
        self.assertEqual(day10.get_angle((0,0),(-1,1)), 225)

    def test_day10_2_1(self):
        bestLocation, numVisible = day10.find_best_station(day10.get_astroids(inpE))
        self.assertEqual(bestLocation, (11,13))
        self.assertEqual(numVisible, 210)
        shoot_list = day10.shoot(bestLocation, day10.get_astroids(inpE))
        self.assertEqual(shoot_list[0], (11,12))
        self.assertEqual(shoot_list[1], (12,1))
        self.assertEqual(shoot_list[2], (12,2))

        self.assertEqual(shoot_list[10-1], (12,8))
        self.assertEqual(shoot_list[20-1], (16,0))
        self.assertEqual(shoot_list[50-1], (16,9))
        self.assertEqual(shoot_list[100-1], (10,16))

        self.assertEqual(shoot_list[199-1], (9,6))
        self.assertEqual(shoot_list[200-1], (8,2))
        self.assertEqual(shoot_list[201-1], (10,9))

        self.assertEqual(shoot_list[299-1], (11,1))



if __name__ == '__main__':
    unittest.main()
