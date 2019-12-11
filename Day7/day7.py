# 
# --- Day 2: 1202 Program Alarm ---
#
# --- Day 5: Sunny with a Chance of Asteroids ---
# 
import itertools
from unittest.mock import patch

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

def END():
    #print("END")
    return "END"

instrSet = {
    # code: (FUNCTION, #ofParams, Outputs, jumps)
    1: (ADD, 3, True, False),
    2: (MUL, 3, True, False),
    3: (INP, 1, True, False),
    4: (OUT, 1, False, False),
    5: (JPT, 2, False, True),
    6: (JPF, 2, False, True),
    7: (LES, 3, True, False),
    8: (EQL, 3, True, False),
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

def optimize2(prog):
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


def runPartOne():
    #optimize([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
    prog = loadintCode('input_day7')
    optimize(prog)
    

if __name__ == '__main__':
    runPartOne()
    #runPartTwo()