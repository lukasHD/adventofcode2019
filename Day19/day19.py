# --- Day 19: Tractor Beam ---

from collections import defaultdict
import queue
import time 

def loadintCode(fname='input'):
    with open(fname, 'r') as f:
        l = list(f.read().split(','))
        p = [int(x) for x in l]
        return p


class Computer():
    def __init__(self, _prog):
        self.prog = defaultdict(int)
        for i in range(len(_prog)):
            self.prog[i] = int(_prog[i])
        self.inp           = queue.Queue()
        self.output        = queue.Queue()
        self.input_counter = 0
        self.halted        = False
        self.finished      = False
        self.idx           = 0
        self.base          = 0
        self.instrSet = {
            # code: (FUNCTION, #ofParams, Outputs, jumps)
            1:  (self.ADD, 3, True,  False),
            2:  (self.MUL, 3, True,  False),
            3:  (self.INP, 1, True,  False),
            4:  (self.OUT, 1, False, False),
            5:  (self.JPT, 2, False, True),
            6:  (self.JPF, 2, False, True),
            7:  (self.LES, 3, True,  False),
            8:  (self.EQL, 3, True,  False),
            9:  (self.ADJ, 1, False, False),
            99: (self.END, 0, False, True)
        }

    def ADD(self, vals):
        if len(vals) != 2: raise TypeError
        a,b = vals
        return a+b

    def MUL(self, vals):
        if len(vals) != 2: raise TypeError
        a,b = vals
        return a*b

    def INP(self, vals, interactive=True, value=0):
        if not interactive: 
            #print("simulate input value: {}".format(value))
            return value
        else: 
            print("Enter input: ")
            value = int(input())
            return value

    def OUT(self, vals, interactive=True):
        if len(vals) != 1: raise TypeError
        if not interactive:
            return  vals[0]
        else:
            print("Output is: {}".format(vals[0]))

    def JPT(self, vals):
        if vals[0] != 0: 
            return True
        else:
            return False

    def JPF(self, vals):
        if vals[0] == 0:
            return True
        else: 
            return False

    def LES(self, vals):
        if vals[0] < vals[1]:
            return 1
        else:
            return 0

    def EQL(self, vals):
        if vals[0] == vals[1]:
            return 1
        else:
            return 0

    def ADJ(self, vals):
        return vals[0]

    def END(self):
        #print("END")
        return "END"

    def decode(self,val):
        if val in self.instrSet.keys():
            # valid op code
            return self.instrSet[val]
        else:
            return None

    def run(self, debug=False, interactive=False):
        self.ignore = 0
        self.halted = False
        #output = []
        while not (self.finished or self.halted):
            val = self.prog[self.idx]
            if self.ignore > 0:
                self.ignore -= 1
                self.idx += 1
                continue
            #print("idx, val = {}, {}".format(self.idx, val))
            #if debug: printIndexValue(self.prog, self.idx)
            cmd = val%100
            op, numVar, writes, jumps = self.decode(cmd)
            if op == self.END:
                op()
                #print("END END END")
                if debug: print(self.output.queue)
                self.finished = True
                if interactive == True:
                    return self.prog
                else:
                    if debug: print(self.output.queue)
                    return self.output
            modes = val//100
            mod= []
            while (modes > 0):
                tmp = modes%10
                if tmp not in [0, 1, 2]: raise TypeError
                mod.append(tmp)
                modes = modes//10
            vars = []
            for i in range(numVar):
                try:
                    m = mod[i]
                except IndexError:
                    m = 0
                if m == 0:
                    vars.append(self.prog[self.prog[self.idx+1+i]])
                elif m == 1:
                    vars.append(self.prog[self.idx+1+i])
                elif m == 2:
                    vars.append(self.prog[self.base + self.prog[self.idx+1+i]])
                else: 
                    raise RuntimeError
            if op == self.ADJ:
                # adjust the base by the value of the parameter 
                self.base = self.base + vars[0]
            elif writes:
                # an opcode that writes to last parameter
                if op == self.INP and interactive == False:
                    if self.inp.empty():
                        print("empty")
                        return self.output
                    _value = self.inp.get(block=False)
                    #print("InputValue = {}".format(_value))
                    #if debug: print("{} {}".format(numVar, vars))
                    if m == 0:
                        self.prog[self.prog[self.idx+1]] = op(vars[:-1], interactive=False, value=_value)
                    elif m == 2:
                        self.prog[self.base + self.prog[self.idx+1]] = op(vars[:-1], interactive=False, value=_value)
                    else:
                        raise RuntimeError
                else:
                    if m == 0:
                        self.prog[self.prog[self.idx+numVar]] = op(vars[:-1])
                    elif m == 2:
                        self.prog[self.base + self.prog[self.idx+numVar]] = op(vars[:-1])
                    else:
                        raise RuntimeError

            elif jumps:
                #print("JUMP")
                if op(vars[:-1]):
                    self.idx = vars[-1]
                    continue
            else:
                if op == self.OUT and interactive == False:
                    value = op(vars, interactive=False)
                    #print(value)
                    self.output.put(value)

                    if debug: print(self.output.queue)
                    if self.output.qsize() == 3:
                        self.halted = True
                        #self.finished = True
                        #self.ignore = numVar
                        self.idx += 2
                        return self.output
                    self.idx += 0
                    #return output[-1] 
                else:
                    op(vars)
            self.ignore = numVar
            self.idx += 1



def run_small_test():
    print("small Test 1")
    print("############")
    intcode = loadintCode()
    c = Computer(intcode)
    c.inp.put(0)
    c.inp.put(0)
    out = c.run()
    print(list(out.queue))

def runPartOne():
    print("run Part One")
    print("############")
    intcode = loadintCode()
    counter = 0
    for y in range(50):
        for x in range(50):
            c = Computer(intcode)
            c.inp.put(x)
            c.inp.put(y)
            out = c.run()
            result = list(out.queue)[0]
            if result == 0:
                print(".",end='')
            elif result == 1:
                print("#",end='')
                counter += 1
        print()
            #print("[{}, {}] = {}".format(x,y,result))
    print(counter)

def run_small_test2():
    print("small Test 2")
    print("############")
    intcode = loadintCode()
    counter = 0
    buffer = 3
    minX = 0
    maxX = 650
    ship=99
    beam = defaultdict(lambda: defaultdict(int))
    minmax = defaultdict(list)
    for y in range(700,5000):
        numberOfPoints = 0
        prev = 0
        for x in range(600,5000):
            if x < minX -buffer :
                #print(" ",end='')
                continue
            if x > max(15,maxX +buffer):
                #print(" ",end='')
                continue
            if x > minX +buffer and x < maxX -buffer and maxX-minX > 2*buffer:
                #print("+",end='')
                beam[y][x] = 1
                numberOfPoints += 1
                continue
            c = Computer(intcode)
            c.inp.put(x)
            c.inp.put(y)
            out = c.run()
            result = list(out.queue)[0]
            beam[y][x] = result
            if result == 0:
                #print(".",end='')
                if prev == 1:
                    maxX = x-1
                    prev = 0
            elif result == 1:
                #print("#",end='')
                if prev==0:
                    minX = x
                    prev = 1
                counter += 1
                numberOfPoints += 1
        minmax[y] = [numberOfPoints, minX, maxX]
        print("  {}  [{}:{}]    --    {}    --     {}".format(numberOfPoints, minX, maxX, minmax[y-ship], y),end='')
        if numberOfPoints > ship and minmax[y-ship][0] > ship :
            if minmax[y-ship][2] < minX+98:
                print()
                continue
            if not (minmax[y-ship][1] <= minX+ship <=minmax[y-ship][2]):
                print()
                continue
            try:
                #print(list(beam.keys()))
                unl = beam[y][minX]
                unr = beam[y][minX+ship]
                obl = beam[y-ship][minX]
                print( list( beam[y-ship].keys() ) )
                obr = beam[y-ship][minX+ship]
            except KeyError :
                print("aaa")
                #continue
            print("\n    unl f({},{}) = {}".format(minX, y, unl))
            print("    unr f({},{}) = {}".format(minX+ship, y, unr))
            print("    obl f({},{}) = {}".format(minX, y-ship, obl))
            print("    obr f({},{}) = {}".format(minX+ship, y-ship, obr))
            if unl == 0 or unr == 0 or obl == 0 or obr == 0:
                continue
            else:
                print("seems to fit")
                a = 10000*minX+(y-ship)
                print(a)
                break
        
        print()
        # calc min and max x for this row
        if numberOfPoints == 0:
            continue



def runPartTwo():
    print("run Part Two")
    print("############")


if __name__ == '__main__':
    run_small_test()
    #runPartOne()
    run_small_test2()
    runPartTwo()