# 
# --- Day 2: 1202 Program Alarm ---
#
# --- Day 5: Sunny with a Chance of Asteroids ---
#
# --- Day 7: Amplification Circuit ---
#
# --- Day 9: Sensor Boost ---
# 
import itertools
from unittest.mock import patch
import queue
from collections import defaultdict

def loadintCode(fname='input'):
    with open(fname, 'r') as f:
        l = list(f.read().split(','))
        p = [int(x) for x in l]
        return p

def printIndexValue(L, pos=0):
    longest = len(str(max(L)))
    print("[",end='')
    for idx, val in enumerate(L):
        print("{:{width}d},".format(val, width=longest+1),end='')
    print("]")
    indices = list(range(len(L)))
    indices[pos] = "^"*(longest+1)
    print("(",end='')
    for idx in indices:
        print("{:^{width}s},".format(str(idx), width=longest+1),end='')
    print(")")

def ADD(vals):
    if len(vals) != 2: raise TypeError
    a,b = vals
    return a+b

def MUL(vals):
    if len(vals) != 2: raise TypeError
    a,b = vals
    return a*b

def INP(vals, interactive=True, value=0):
    if not interactive: 
        #print("simulate input value: {}".format(value))
        return value
    else: 
        print("Enter input: ")
        value = int(input())
        return value

def OUT(vals, interactive=True):
    if len(vals) != 1: raise TypeError
    if not interactive:
        return  vals[0]
    else:
        print("Output is: {}".format(vals[0]))

def JPT(vals):
    if vals[0] != 0: 
        return True
    else:
        return False

def JPF(vals):
    if vals[0] == 0:
        return True
    else: 
        return False

def LES(vals):
    if vals[0] < vals[1]:
        return 1
    else:
        return 0

def EQL(vals):
    if vals[0] == vals[1]:
        return 1
    else:
        return 0

def ADJ(vals):
    return vals[0]

def END():
    #print("END")
    return "END"

instrSet = {
    # code: (FUNCTION, #ofParams, Outputs, jumps)
    1:  (ADD, 3, True,  False),
    2:  (MUL, 3, True,  False),
    3:  (INP, 1, True,  False),
    4:  (OUT, 1, False, False),
    5:  (JPT, 2, False, True),
    6:  (JPF, 2, False, True),
    7:  (LES, 3, True,  False),
    8:  (EQL, 3, True,  False),
    9:  (ADJ, 1, False, False),
    99: (END, 0, False, True)
}

def decode(val):
    if val in instrSet.keys():
        # valid op code
        return instrSet[val]
    else:
        return None

def runCode(intInput, debug=False, interactive=True, _in=None):
    ignore = 0
    idx = 0
    output = []
    #for idx, val in enumerate(intInput):
    while(idx <= len(intInput)):
        val = intInput[idx]
        if ignore > 0:
            ignore -= 1
            idx += 1
            continue
        if debug: printIndexValue(intInput, idx)
        cmd = val%100
        op, numVar, writes, jumps = decode(cmd)
        if op == END:
            op()
            if interactive == True:
                return intInput
            else:
                return output
        modes = val//100
        mod= []
        while (modes > 0):
            tmp = modes%10
            if tmp not in [0, 1]: raise TypeError
            mod.append(tmp)
            modes = modes//10
        # now run op(vars)
        vars = []
        for i in range(numVar):
            try:
                m = mod[i]
            except IndexError:
                m = 0
            if m == 0:
                vars.append(intInput[intInput[idx+1+i]])
            elif m == 1:
                vars.append(intInput[idx+1+i])
            else: 
                raise RuntimeError
        if writes:
            # an opcode that writes to last parameter
            if op == INP and interactive == False:
                intInput[intInput[idx+numVar]] = op(vars[:-1], interactive=False, value=_in.pop(0))
            else:
                intInput[intInput[idx+numVar]] = op(vars[:-1])
        elif jumps:
            #print("JUMP")
            if op(vars[:-1]):
                idx = vars[-1]
                continue
        else:
            if op == OUT and interactive == False:
                output.append(op(vars, interactive=False))
            else:
                op(vars)
        ignore = numVar
        idx += 1

# day7
def run_Prog_non_interactive(_prog, _in):
    out = runCode(_prog, debug=False, interactive=False, _in=_in)
    return out[-1]


def optimize(prog):
    maxThrust = 0
    phaseSeq = []
    resultList = []
    for perm in list(itertools.permutations([0, 1, 2, 3, 4])): 
        #print(perm)
        out1 = run_Prog_non_interactive(prog, [perm[0], 0])
        out2 = run_Prog_non_interactive(prog, [perm[1], out1])
        out3 = run_Prog_non_interactive(prog, [perm[2], out2])
        out4 = run_Prog_non_interactive(prog, [perm[3], out3])
        out5 = run_Prog_non_interactive(prog, [perm[4], out4])
        resultList.append((perm, out5))
    #print(resultList)
    bla = max(resultList, key=lambda x: x[1])
    #print(bla)
    phaseSeq, maxThrust = bla
    print(maxThrust)
    print(phaseSeq)
    return maxThrust, list(phaseSeq) 

class Amp():
    def __init__(self, prog):
        self.prog          = prog.copy()
        self.inp           = queue.Queue()
        self.output        = 0
        self.input_counter = 0
        self.halted        = False
        self.finisehd      = False
        self.idx           = 0

    def run(self, debug=False, interactive=False):
        ignore = 0
        output = []
        while not self.finisehd:
            val = self.prog[self.idx]
            if ignore > 0:
                ignore -= 1
                self.idx += 1
                continue
            #if debug: printIndexValue(self.prog, self.idx)
            cmd = val%100
            op, numVar, writes, jumps = decode(cmd)
            if op == END:
                op()
                #print("END END END")
                if debug: print(output)
                self.finisehd = True
                if interactive == True:
                    return self.prog
                else:
                    if debug: print(output)
                    return output
            modes = val//100
            mod= []
            while (modes > 0):
                tmp = modes%10
                if tmp not in [0, 1]: raise TypeError
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
                else: 
                    raise RuntimeError
            if writes:
                # an opcode that writes to last parameter
                if op == INP and interactive == False:
                    if self.inp.empty():
                        #print("empty")
                        return output
                    self.prog[self.prog[self.idx+numVar]] = op(vars[:-1], interactive=False, value=self.inp.get(block=False))
                else:
                    self.prog[self.prog[self.idx+numVar]] = op(vars[:-1])
            elif jumps:
                #print("JUMP")
                if op(vars[:-1]):
                    self.idx = vars[-1]
                    continue
            else:
                if op == OUT and interactive == False:
                    output.append(op(vars, interactive=False))
                    if debug: print(output)
                    #self.halted = True
                    self.idx += 0
                    #return output[-1] 
                else:
                    op(vars)
            ignore = numVar
            self.idx += 1


def runAmps(prog, phases):
    # initialize amps
    amp1 = Amp(prog)
    amp2 = Amp(prog)
    amp3 = Amp(prog)
    amp4 = Amp(prog)
    amp5 = Amp(prog)
    #print(phases)
    amp1.inp.put(phases[0])
    amp2.inp.put(phases[1])
    amp3.inp.put(phases[2])
    amp4.inp.put(phases[3])
    amp5.inp.put(phases[4])

    # provide start command
    amp1.inp.put(0)

    loops = 0
    while (not amp5.finisehd):
        #print("loop: {} amp: 1".format(loops))
        out1 = amp1.run(debug=False)
        #print(out1)
        amp2.inp.put(out1[-1])
        #print("loop: {} amp: 2".format(loops))
        out2 = amp2.run(debug=False)
        amp3.inp.put(out2[-1])
        #print("loop: {} amp: 3".format(loops))
        out3 = amp3.run(debug=False)
        amp4.inp.put(out3[-1])
        #print("loop: {} amp: 4".format(loops))
        out4 = amp4.run(debug=False)
        amp5.inp.put(out4[-1])
        #print("loop: {} amp: 5".format(loops))
        out5 = amp5.run(debug=False)
        amp1.inp.put(out5[-1])
        loops += 1
    return out5


def optimize2(prog):
    maxThrust = 0
    phaseSeq = []
    resultList = []
    for perm in list(itertools.permutations([5, 6, 7, 8, 9])): 
        out = runAmps(prog, perm)
        resultList.append((perm, out[-1]))
    #print(resultList)
    bla = max(resultList, key=lambda x: x[1])
    #print(bla)
    phaseSeq, maxThrust = bla
    print(maxThrust)
    print(phaseSeq)
    return maxThrust, list(phaseSeq) 
        

class Boost():
    def __init__(self, _prog):
        self.prog = defaultdict(int)
    
        for i in range(len(_prog)):
            self.prog[i] = int(_prog[i])
        self.inp           = queue.Queue()
        self.output        = 0
        self.input_counter = 0
        self.halted        = False
        self.finisehd      = False
        self.idx           = 0
        self.base          = 0

    def run(self, debug=False, interactive=False):
        ignore = 0
        output = []
        while not self.finisehd:
            val = self.prog[self.idx]
            if ignore > 0:
                ignore -= 1
                self.idx += 1
                continue
            #if debug: printIndexValue(self.prog, self.idx)
            cmd = val%100
            op, numVar, writes, jumps = decode(cmd)
            if op == END:
                op()
                #print("END END END")
                if debug: print(output)
                self.finisehd = True
                if interactive == True:
                    return self.prog
                else:
                    if debug: print(output)
                    return output
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
            if op == ADJ:
                # adjust the base by the value of the parameter 
                self.base = self.base + vars[0]
            elif writes:
                # an opcode that writes to last parameter
                if op == INP and interactive == False:
                    if self.inp.empty():
                        #print("empty")
                        return output
                    #if debug: print("{} {}".format(numVar, vars))
                    if m == 0:
                        self.prog[self.prog[self.idx+1]] = op(vars[:-1], interactive=False, value=self.inp.get(block=False))
                    elif m == 2:
                        self.prog[self.base + self.prog[self.idx+1]] = op(vars[:-1], interactive=False, value=self.inp.get(block=False))
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
                if op == OUT and interactive == False:
                    output.append(op(vars, interactive=False))
                    if debug: print(output)
                    #self.halted = True
                    self.idx += 0
                    #return output[-1] 
                else:
                    op(vars)
            ignore = numVar
            self.idx += 1



def runPartOne():
    progin = loadintCode('input_day9')
    booster = Boost(progin)
    booster.inp.put(1)
    _out = booster.run(debug=True, interactive=False)
    print(_out)
    
def runPartTwo():
    progin = loadintCode('input_day9')
    booster = Boost(progin)
    booster.inp.put(2)
    _out = booster.run(debug=True, interactive=False)
    print(_out)
    
def run_small_test_1():
    # _in = 7
    # _exp = 999
    # _prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    # amp = Amp(_prog)
    # amp.inp.put(_in)
    # _out = amp.run( debug=True)
    # print(_out)
    # print()
    print("*************")
    print()
    progD = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    maxThrust, phaseSeq = optimize2(progD)

def run_small_test():
    _prog = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    booster = Boost(_prog)
    #booster.inp.put(_in)
    _out = booster.run(debug=False, interactive=False)
    print(_out)
    

if __name__ == '__main__':
    runPartOne()
    #run_small_test()
    runPartTwo()