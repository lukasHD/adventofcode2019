# day3 

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

def manhattanDistance(t, s=(0,0)):
    return abs(t[0] - s[0]) + abs(t[1] - s[1])

def runPartOne(L1, L2):
    parsedL1 = parseInput(L1)
    parsedL2 = parseInput(L2)
    return 0

def runPartTwo(L1, L2):
    return 0

if __name__ == '__main__':
    L1,L2 = loadInput()
    runPartOne(L1, L2)
    #runPartTwo(L1, L2)