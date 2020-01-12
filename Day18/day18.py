# --- Day 18: Many-Worlds Interpretation ---

from collections import defaultdict
from copy import copy, deepcopy

def string2tree(inStr):
    return list(map(list, inStr.split('\n')))

class Dungeon():

    def __init__(self, inArray):
        self.fullMap = copy(inArray)
        self.keys = set()

    def print(self):
        print()
        for line in self.fullMap:
            for el in line:
                print(el,end='')
            print()
        print()

    def minSteps(self):
        return 42

def run_small_test():
    print("small Test 1")
    print("############")
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

    a = Dungeon(string2tree(AAA))
    a.print()
    b = Dungeon(string2tree(BBB))
    b.print()
    c = Dungeon(string2tree(CCC))
    c.print()
    d = Dungeon(string2tree(DDD))
    d.print()
    e = Dungeon(string2tree(EEE))
    e.print()


def runPartOne():
    print("run Part One")
    print("############")

def run_small_test2():
    print("small Test 2")
    print("############")

def runPartTwo():
    print("run Part Two")
    print("############")


if __name__ == '__main__':
    run_small_test()
    runPartOne()
    run_small_test2()
    runPartTwo()