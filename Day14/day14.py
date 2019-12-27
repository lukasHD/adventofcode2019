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

    def produce(self, target, quantity, rest):
        if rest == None:
            rest = defaultdict(int)

        print("want to produce {} {}".format(quantity, target))

        for key in self.reactions:
            if key[1] == target:
                print("For {} {} I need: {}".format(key[0], key[1], self.reactions[key]))
                # claculate how many of those I need
                multiple = quantity // key[0]
                if quantity % key[0] != 0:
                    multiple += 1
                overproduced = multiple * key[0] - quantity
                print("Therefore produce '{} {}' {} times and keep {} pieces".format(key[0], key[1], multiple, overproduced))
                cost = 0
                #depth = 0
                for source in self.reactions[key]:
                    if source[1] == "ORE":
                        return source[0]
                    bla = self.produce(source[1], source[0] * multiple, rest)
                    #print(bla)
                    cost += bla
                return cost
        print(cost)
                

def load(string):
    #print(string)
    resourceTree = Resources()
    for line in string.split('\n'):
        print(line)
        reaction = line.split(' => ')
        print(reaction)
        needed = reaction[0].split(', ')
        sources = [(int(x.split()[0]), x.split()[1]) for x in needed]
        product = tuple((int(reaction[1].strip().split(' ')[0]), reaction[1].strip().split(' ')[1]))
        print("generate {} from {}".format(product, sources))
        resourceTree.add(product, sources)
    resourceTree.showReactions()
    return resourceTree

def getOreForFuel(mapping):
    return 10

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