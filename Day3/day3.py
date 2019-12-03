# day3 
import sys 
sys.path.append('../helper')
from helper import timer

def loadInput(fname='input'):
    with open(fname, 'r') as f:
        L1 = list(f.readline().rstrip().split(','))
        L2 = list(f.readline().rstrip().split(','))
        #print(L1)
        #print(L2)
    return L1, L2

def parseElement(E):
    direction = E[0].upper()
    if direction not in ["L", "R", "U", "D"]: raise TypeError("Direction should be one of L, R, U, D")
    lenght = int(E[1:])
    return (direction, lenght)

def parseInput(L):
    out = [parseElement(x) for x in L]
    return out

def getNextCorner(pos, command):
    x,y = pos
    c,d = command
    if c == "R":
        x += d
    elif c == "L":
        x -= d
    elif c == "U":
        y += d
    elif c == "D":
        y -= d
    else:
        raise TypeError()
    return (x,y)

def getWire(commandList, startPos=(0,0)):
    x,y = startPos
    wire =[startPos]
    for command in commandList:
        c,d = command
        for _ in range(d):
            if c == "R":
                x += 1
            elif c == "L":
                x -= 1
            elif c == "U":
                y += 1
            elif c == "D":
                y -= 1
            else:
                raise TypeError()
            wire.append((x,y))
    return wire

def manhattanDistance(t, s=(0,0)):
    return abs(t[0] - s[0]) + abs(t[1] - s[1])

def getIntersections(wire1, wire2):
    set1 = set(wire1)
    set2 = set(wire2)
    points = set1.intersection(set2)
    points.remove((0,0))
    #print(points)
    return(points)
    
def getDistanceToPointOnWire(wire, point):
    return wire.index(point)

def runPartOne(L1, L2):
    parsedL1 = parseInput(L1)
    parsedL2 = parseInput(L2)
    wire1 = getWire(parsedL1)
    wire2 = getWire(parsedL2)
    points = getIntersections(wire1, wire2)
    distances = [manhattanDistance(x) for x in points]
    #print(distances)
    res = min(distances)
    print(res)
    return res

def runPartTwo(L1, L2):
    parsedL1 = parseInput(L1)
    parsedL2 = parseInput(L2)
    wire1 = getWire(parsedL1)
    wire2 = getWire(parsedL2)
    points = getIntersections(wire1, wire2)
    sumDist = []
    for point in points:
        d1 = getDistanceToPointOnWire(wire1, point)
        d2 = getDistanceToPointOnWire(wire2, point)
        #print("{}: {} + {} = {}".format(point, d1, d2, d1+d2))
        sumDist.append(d1+d2)
    res = min(sumDist)
    print(res)
    return res


if __name__ == '__main__':
    L1,L2 = loadInput()
    runPartOne(L1, L2)
    runPartTwo(L1, L2)