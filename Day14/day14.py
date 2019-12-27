# --- Day 14: Space Stoichiometry ---

from collections import defaultdict

class Resources:

    def __init__(self):
        self.reactions = defaultdict(int)
    
    def add(self, product, sources):
        self.reactions[product] = sources

    def showReactions(self):
        for key, values in self.reactions.items():
            print("{} made from {}".format(key,values))

    def produce(self, target, quantity, rest, depth=0):
        if rest == None:
            rest = defaultdict(int)

        intendation = '____'*depth

        for key in self.reactions:
            if key[1] == target:
                print("{}want to produce {} {} and already have {} {}".format(intendation, quantity, target, rest[target], target))
                print("{}can do {} {} using: {} ".format(intendation, key[0], key[1], self.reactions[key]))
                
                if not (quantity - rest[target]) % key[0]:
                    rest[target] = 0
                    a = (quantity - rest[target]) // key[0]
                    print("{}glatt rest[{}]=0  a = {}".format(intendation, target, a))
                else:
                    a = ((quantity - rest[target]) // key[0]) + 1
                    rest[target] = key[0] - ((quantity - rest[target]) % key[0])
                    print("{}krumm rest[{}]={}  a = {}".format(intendation, target, rest[target], a))

                #print(a)
                if a == 0:
                    return 0, rest
                # multiple = quantity // key[0]
                # if quantity % key[0] != 0:
                #     multiple += 1
                # overproduced = multiple * key[0] - quantity
                
                print("{}Therefore produce '{} {}' {} times and keep {} pieces".format(intendation, key[0], key[1], a, rest[target]))
                #rest[key[1]] += overproduced
                cost = 0
                #depth = 0
                for source in self.reactions[key]:
                    if source[1] == "ORE":
                        print("{}Found {} ORE".format(intendation, source[0]*a))
                        return source[0]*a, rest
                    bla, rest = self.produce(source[1], source[0] * a, rest, depth=depth+1)
                    #print(bla)
                    cost += bla
                return cost, rest
        print(cost)
                

def load(string):
    #print(string)
    resourceTree = Resources()
    for line in string.split('\n'):
        #print(line)
        reaction = line.split(' => ')
        #print(reaction)
        needed = reaction[0].split(', ')
        sources = [(int(x.split()[0]), x.split()[1]) for x in needed]
        product = tuple((int(reaction[1].strip().split(' ')[0]), reaction[1].strip().split(' ')[1]))
        #print("generate {} from {}".format(product, sources))
        resourceTree.add(product, sources)
    resourceTree.showReactions()
    return resourceTree

def getOreForFuel(inp):
    myTree = load(inp)
    aa = myTree.produce("FUEL", 1, None)
    return aa[0]

def run_small_test():
    print("small Test 1")
    print("############")
    inpA = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""
    myTree = load(inpA)
    aa = myTree.produce("FUEL", 1, None)
    print(aa)
    # myTree.produce("A", 15)

def runPartOne():
    print("run Part One")
    print("############")
    with open('input', 'r') as f:
        inp = f.read()
    myTree = load(inp)
    aa = myTree.produce("FUEL", 1, None)
    print(aa)

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