# --- Day 18: Many-Worlds Interpretation ---

from collections import defaultdict
from copy import copy, deepcopy

def readInput(fname = 'input'):
    with open(fname, 'r') as f:
        a = f.readlines()
        b = ''.join(a)
    #print(b)
    return b


def string2tree(inStr):
    return list(map(list, inStr.split('\n')))

class Dungeon():

    def __init__(self, inArray):
        print("\n~~~~~~~~~~~~ new Dungeon ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        self.fullMap = copy(inArray)
        self.cleanMap = copy(inArray)
        self.cleaned = False
        self.keys = set()
        self.low   = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.upper = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.tree = defaultdict(list)
        self.robotPosition = (None, None)
        self.reachableKeys = set()
        self.allKeys = set()
        self.keyPos = {}
        self.getAllKeys()
        self.sequences = []

    def getAllKeys(self):
        for y, line in enumerate(self.fullMap):
            for x, el in enumerate(line):
                if el in self.low:
                    self.allKeys.add(el)
                    self.keyPos[el] = (x,y)
        print(self.allKeys)
        print(self.keyPos)

    def print(self, cleaned=True):
        if cleaned:
            if not self.cleaned: self.cleanUp()
            mapp = deepcopy(self.cleanMap)
        else:
            mapp = self.fullMap
        print()
        x, y = self.robotPosition
        try:
            mapp[y][x] = '@'
        except:
            pass
        for line in mapp:
            for el in line:
                print(el,end='')
            print()
        print()

    def printKeys(self):
        for key in self.keys:
            print(key,end=', ')
        print()

    def cleanUp(self):
        self.cleanMap = deepcopy(self.fullMap)
        for y, line in enumerate(self.cleanMap):
            for x, el in enumerate(line):
                if el in self.low:
                    # is lower case - remove all keys we have
                    if el in self.keys:
                        self.cleanMap[y][x] = '.'
                elif el in self.upper:
                    # is a door - replace with open or closed piece 
                    if el.lower() in self.keys:
                        self.cleanMap[y][x] = '.'
                    else:
                        self.cleanMap[y][x] = '#'
                elif el == '@':
                    # current robot position
                    self.robotPosition = (x,y)
                    self.cleanMap[y][x] = '.'
                else:
                    # is already wall or open - do nothing
                    pass
        self.cleaned = True

    def takeKey(self, key):
        #print("in takeKey(self, {})".format(key))
        self.keys.add(key)
        for y, line in enumerate(self.fullMap):
            for x, el in enumerate(line):
                #print(el)
                if el in self.low:
                    # is lower case - remove all keys we have
                    if el in self.keys:
                        #print("remove key {}".format(el))
                        self.fullMap[y][x] = '.'
                elif el in self.upper:
                    # is upper case - remove the door we have the key for
                    if el.lower() in self.keys:
                        #print("remove Door {}".format(el))
                        self.fullMap[y][x] = '.'

    def createTree(self):
        self.cleanUp()
        for y in range(len(self.cleanMap)):
            for x in range(len(self.cleanMap[0])):
                el = self.cleanMap[y][x]
                if el in ['.', '@']+self.low:
                    if self.cleanMap[y-1][x] in ['.', '@']+self.low:
                        self.tree[(x,y)].append((x,y-1))
                    if self.cleanMap[y+1][x] in ['.', '@']+self.low:
                        self.tree[(x,y)].append((x,y+1))
                    if self.cleanMap[y][x-1] in ['.', '@']+self.low:
                        self.tree[(x,y)].append((x-1,y))
                    if self.cleanMap[y][x+1] in ['.', '@']+self.low:
                        self.tree[(x,y)].append((x+1,y))

    def findReachableKeys(self, startPos):
        
        # finds shortest path between 2 nodes of a graph using BFS
        def bfs_shortest_path(graph, start, goal):
            #print("{} --- {} --- {}".format(graph, start, goal))
            #print("{} --- {}".format(start, goal))
            # keep track of explored nodes
            explored = []
            # keep track of all the paths to be checked
            queue = [[start]]
        
            # return path if start is goal
            if start == goal:
                return 0
        
            # keeps looping until all possible paths have been checked
            while queue:
                # pop the first path from the queue
                path = queue.pop(0)
                # get the last node from the path
                node = path[-1]
                if node not in explored:
                    neighbours = graph[node]
                    # go through all neighbour nodes, construct a new path and
                    # push it into the queue
                    for neighbour in neighbours:
                        new_path = list(path)
                        new_path.append(neighbour)
                        queue.append(new_path)
                        # return path if neighbour is goal
                        if neighbour == goal:
                            return new_path
        
                    # mark node as explored
                    explored.append(node)
        
            # in case there's no path between the 2 nodes
            return -1
        self.reachableKeys = []
        for key in self.allKeys - self.keys:
            path = bfs_shortest_path(self.tree, self.robotPosition, self.keyPos[key])
            if path != 0 and path != -1:
                #print("key = {}; path = {}".format(key, path))
                self.reachableKeys.append((key, len(path)-1))
        
        self.reachableKeys.sort(key=lambda x: x[1])
        return self.reachableKeys

        

    def printTree(self):
        for k,v in self.tree.items():
            print("{}: {}".format(k, v))

    def minSteps(self):
        self.sequences = []
        openSequences = []
        while True:
            steps = 0
            sequence = []
            while self.keys != self.allKeys:
                self.print(cleaned=False)
                self.cleanUp()
                self.createTree()
                self.findReachableKeys(self.robotPosition)
                print("reachable = {}".format(self.reachableKeys))
                if len(self.reachableKeys) == 0:
                    print("Nothing reachable")
                    break
                elif len(self.reachableKeys) == 1:
                    print("goto {}".format(self.reachableKeys[0]))
                    key, addSteps = self.reachableKeys[0]
                    self.takeKey(key)
                    self.fullMap[self.robotPosition[1]][self.robotPosition[0]] = '.'
                    self.robotPosition = self.keyPos[key]
                    sequence.append(key)
                    steps += addSteps
                else:
                    #raise RuntimeError("not yet implemented")
                    # TODO obviously wrong
                    print("goto {}".format(self.reachableKeys[0]))
                    key, addSteps = self.reachableKeys[0]
                    self.takeKey(key)
                    self.fullMap[self.robotPosition[1]][self.robotPosition[0]] = '.'
                    self.robotPosition = self.keyPos[key]
                    sequence.append(key)
                    steps += addSteps
            
            print("steps = {}; sequence = {}".format(steps, sequence))
            self.sequences.append([steps, sequence])
            if len(openSequences) == 0: break
        self.sequences.sort(key=lambda x: x[0])
        return self.sequences[0][0]

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
    # a.print()
    # a.keys.add('a')
    # a.cleanUp()
    # a.print()
    a.minSteps()
    b = Dungeon(string2tree(BBB))
    # b.print()
    # b.takeKey('a')
    # b.print(cleaned=False)
    # b.cleanUp()
    # b.print()
    # b.createTree()
    # #b.printTree()
    # b.findReachableKeys(b.robotPosition)
    # print(b.reachableKeys)
    b.minSteps()
    # c = Dungeon(string2tree(CCC))
    # c.print()
    # d = Dungeon(string2tree(DDD))
    # d.print()
    # e = Dungeon(string2tree(EEE))
    # e.print()


def runPartOne():
    print("run Part One")
    print("############")
    # myString = readInput()
    # print("-------------------------------------------")
    # a = Dungeon(string2tree(myString))
    # a.print()

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