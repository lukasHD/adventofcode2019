# https://adventofcode.com/2019/day/5
# 
# --- Day 2: 1202 Program Alarm ---
#
# --- Day 5: Sunny with a Chance of Asteroids ---
# 

def readOpCode(op):
    if op == 1:
        print("add")
        return 
    elif op == 2:
        print("mul")
    elif op == 99:
        print("break")

intInput = [1,9,10,3,2,3,11,0,99,30,40,50]

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

def END():
    print("END")
    return "END"

instrSet = {
    1: (ADD, 3, True),
    2: (MUL, 3, True),
    3: (INP, 1, True),
    4: (OUT, 1, False),
    99: (END, 0, False)
}

def decode(val):
    if val in instrSet.keys():
        # valid op code
        return instrSet[val]
    else:
        return None

def runCode(intInput, debug=True):
    ignore = 0
    for idx, val in enumerate(intInput):
        if ignore > 0:
            ignore -= 1
            continue
        if debug: printIndexValue(intInput, idx)
        cmd = val%100
        op, numVar, writes = decode(cmd)
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
        else:
            op(vars)
        ignore = numVar

def runIntcode(intInput, debug=True):
    ignore = 0
    for idx, val in enumerate(intInput):
        if ignore > 0:
            ignore -= 1
            continue
        #print("index is %d and value is %s" % (idx, val))
        #print("Index: {}".format(idx))
        #print(intInput)
        if debug: print("")
        if debug: printIndexValue(intInput, idx)
        #readOpCode(val)
        if val == 1:
            if debug: print("add({}, {}, {})".format(intInput[idx+1], intInput[idx+2], intInput[idx+3]))
            if debug: print("L[{}] = {} + {} = {}".format(intInput[idx+3], intInput[intInput[idx+1]], intInput[intInput[idx+2]], intInput[intInput[idx+1]] + intInput[intInput[idx+2]]))
            intInput[intInput[idx+3]] = intInput[intInput[idx+1]] + intInput[intInput[idx+2]]
            ignore = 3
        elif val == 2:
            if debug: print("mul({}, {}, {})".format(intInput[idx+1], intInput[idx+2], intInput[idx+3]))
            if debug: print("L[{}] = {} * {} = {}".format(intInput[idx+3], intInput[intInput[idx+1]], intInput[intInput[idx+2]], intInput[intInput[idx+1]] * intInput[intInput[idx+2]]))
            intInput[intInput[idx+3]] = intInput[intInput[idx+1]] * intInput[intInput[idx+2]]
            ignore = 3
        elif val == 99:
            if debug: print("break")
            return(intInput)

def runDay2PartOne():
    intInput2 = [1,1,1,4,99,5,6,0,99]
    runCode(intInput2)
    intCode = loadintCode('input_day2')
    print(intCode)
    intCode[1] = 12
    intCode[2] = 2
    print(intCode)
    print("**************************************************")
    runCode(intCode)
    print("result should be:")
    print([30,1,1,4,2,5,6,0,99])

def runDay2PartTwo():
    for noun in range(100):
        for verb in range(100):
            print("noun: {:3d} verb: {:3d}".format(noun, verb), end='')
            intCode = loadintCode('input_day2')
            intCode[1] = noun
            intCode[2] = verb
            result = runIntcode(intCode, False)
            print("  {}".format(result[0]))
            if result[0] == 19690720:
                return 100*noun + verb

def runPartOne():
    runCode([1002,4,3,4,33])
    runCode([3,0,4,0,99])
    intCode = loadintCode('input')
    runCode(intCode, debug=False)

if __name__ == '__main__':
    #runDay2PartOne()
    #runDay2PartTwo()
    runPartOne()