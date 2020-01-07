# --- Day 24: Planet of Discord ---

import copy

def str2array(string):
    out = string.split('\n')
    out = list(map(list, out))
    return out

class GameOfLife:

    def __init__(self, initialState):
        self.currentState = initialState.copy()
        self.minX = 0
        self.maxX = len(initialState[0])
        self.minY = 0
        self.maxY = len(initialState)
        self.nextState = [[0 for i in range(self.maxX)] for j in range(self.maxY)] # which way around i and j ? doesn't matter here

    def getNeighbors(self, position):
        out = []
        x, y = position
        if x-1 >= self.minX:
            out.append([x-1,y])
        if x+1 < self.maxX:
            out.append([x+1,y])
        if y-1 >= self.minY:
            out.append([x,y-1])
        if y+1 < self.maxY:
            out.append([x,y+1])
        return out

    def getString(self):
        a = ''
        #a += '\n'
        for line in self.currentState:
            for el in line:
                a += el
            a += '\n'
        #a += '\n'
        return a
    
    def print(self):
        print(self.getString())

    def step(self, debug=True):
        #self.nextState = [[0 for i in range(self.maxX)] for j in range(self.maxY)] # which way around i and j ? doesn't matter here
        for y, line in enumerate(self.currentState):
            for x, current in enumerate(line):
                if debug: print("x = {} y = {}".format(x,y))
                numberAlive = 0
                for nx, ny in self.getNeighbors([x,y]):
                    if debug: print("    nx = {} ny = {}     ---     {}".format(nx, ny, self.currentState[ny][nx]))
                    if self.currentState[ny][nx] == '#':
                        numberAlive += 1
                if debug: print(numberAlive, end='     ')
                if current == '#' and numberAlive != 1:
                    self.nextState[y][x] = '.'
                    if debug: print("kill it")
                elif current == '#':
                    self.nextState[y][x] = '#'
                    if debug: print("keep it")
                if current == '.' and (numberAlive == 1 or numberAlive == 2):
                    self.nextState[y][x] = '#'
                    if debug: print("make it")
                elif current == '.':
                    self.nextState[y][x] = '.'
                    if debug: print("keep it")
        self.currentState = copy.deepcopy(self.nextState)

    def calcValue(self):
        val = 0
        res = 0
        for y, line in enumerate(self.currentState):
            for x, current in enumerate(line):
                if current == '#':
                    res += 2**val
                val += 1
        return res

    def untilRepeat(self):
        seen = set()
        #seen.add(self.calcValue())
        while (a := self.calcValue()) not in seen:
            #print("{} {}".format(a, seen))
            print("{}".format(a))
            #self.print()
            #print('.', end='', flush=True)
            seen.add(a)
            self.step(debug=False)
        print("{} {}".format(a, seen))
        return a

def load(fname = 'input'):
    with open(fname, 'r') as f:
        a = f.readlines()
        b = ''.join(a)
    print(a)
    print(b)
    return b
                
def run_small_test():
    print("small Test 1")
    print("############")
    aaa = """....#
#..#.
#..##
..#..
#...."""
    array = str2array(aaa)
    print(array)
    game = GameOfLife(array)
    print(game.getNeighbors([0,0]))
    print(game.getNeighbors([1,1]))
    print(game.getNeighbors([4,4]))
    game.print()
    game.step(debug=False)
    game.print()
    game.step(debug=False)
    game.print()
    game.step(debug=False)
    game.print()
    game.step(debug=False)
    game.print()
    bbb = """.....
.....
.....
#....
.#..."""
    game2 = GameOfLife(str2array(bbb))
    print(game2.calcValue())
    game.untilRepeat()
    print()

def runPartOne():
    print("run Part One")
    print("############")
    game1 = GameOfLife(str2array(load()))
    print()
    out = game1.untilRepeat()
    print()
    print(out)

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