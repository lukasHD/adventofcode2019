# day6

def readInput(fname=input):
    with open(fname, 'r') as f:
        l = f.readlines()
    r = [x.strip().split(')') for x in l]
    x = {}
    for parent,child in r:
        x[child] = parent
    return x

def countParents(tree, element):
    if element not in list(tree): raise TypeError
    counter = 0
    parent = tree[element]
    parents = []
    while parent in list(tree):
        counter += 1
        parents.append(parent)
        parent = tree[parent]
    if parent == 'COM':
        counter += 1
        parents.append(parent)
    return counter, parents

def getTotalOrbits(fname="input"):
    tree = readInput(fname)
    #print(tree)
    sum = 0
    for start in list(tree):
        cnt, parents = countParents(tree, start)
        #print("{} has {} parents: {}".format(start, cnt, parents))
        sum += cnt
    return sum

def runTestOne():
    tree = readInput("test_input")
    print(tree)
    for start in list(tree):
        #start = 'B'
        cnt, parents = countParents(tree, start)
        print("{} has {} parents: {}".format(start, cnt, parents))
    return 0

def getNumberOfTransfers(fname="input"):
    tree = readInput(fname)
    #print(tree)
    cnt1, YOU = countParents(tree, 'YOU')
    cnt2, SAN = countParents(tree, 'SAN')
    print("{} has {} parents: {}".format("YOU", cnt1, YOU))
    print("{} has {} parents: {}".format("SAN", cnt2, SAN))
    inter = set(YOU).difference(set(SAN)).union(set(SAN).difference(set(YOU)))
    print(inter)
    r = len(inter) #is correct since i need one less but we are missing the first common one
    return r


def runPartOne():
    res = getTotalOrbits()
    print(res)
    return res

def runPartTwo():
    res = getNumberOfTransfers()
    print(res)
    return res

if __name__ == '__main__':
    runTestOne()
    runPartOne()
    
    runPartTwo()