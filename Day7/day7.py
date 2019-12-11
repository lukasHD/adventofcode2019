# 
# --- Day 2: 1202 Program Alarm ---
#
# --- Day 5: Sunny with a Chance of Asteroids ---
# 

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

def INP(vals, sim=None):
    if sim is not None: 
        print("simulate input value: {}".format(sim))
        return sim
    else: 
        print("Enter input: ")
        sim = int(input())
        return sim

def OUT(vals):
    if len(vals) != 1: raise TypeError
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

def runCode(intInput, debug=False):
    ignore = 0
    idx = 0
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
            return intInput
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
            intInput[intInput[idx+numVar]] = op(vars[:-1])
        elif jumps:
            print("JUMP")
            if op(vars[:-1]):
                idx = vars[-1]
                continue
        else:
            op(vars)
        ignore = numVar
        idx += 1


# day7

def optimize(prog):
    maxThrust = 0
    phaseSeq = []
    for perm in permutations:
        # bla bla bla 
        print(perm)
    return maxThrust, phaseSeq 


def runPartOne():
    prog = loadintCode('input_day7')

if __name__ == '__main__':
    runPartOne()
    #runPartTwo()