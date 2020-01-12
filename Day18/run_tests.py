import day18
import unittest

AAA = """#########
#b.A.@.a#
#########"""
BBB = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""
CCC = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""
DDD = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""
EEE = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""


class TestRunner(unittest.TestCase):
    
    def test_day18_1_1(self):
        a = day18.Dungeon(day18.string2tree(AAA))
        self.assertEqual(a.minSteps(), 8)

    def test_day18_1_2(self):
        b = day18.Dungeon(day18.string2tree(BBB))
        self.assertEqual(b.minSteps(), 86)

    def test_day18_1_3(self):
        c = day18.Dungeon(day18.string2tree(CCC))
        self.assertEqual(c.minSteps(), 132)

    def test_day18_1_4(self):
        d = day18.Dungeon(day18.string2tree(DDD))
        self.assertEqual(d.minSteps(), 136)

    def test_day18_1_5(self):
        e = day18.Dungeon(day18.string2tree(EEE))
        self.assertEqual(e.minSteps(), 81)


if __name__ == '__main__':
    unittest.main()
