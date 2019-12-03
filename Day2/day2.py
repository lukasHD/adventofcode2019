# https://adventofcode.com/2019/day/2
# 
# --- Day 2: 1202 Program Alarm ---
#
#
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

def runPartOne():
    intInput2 = [1,1,1,4,99,5,6,0,99]
    runIntcode(intInput2)
    intCode = loadintCode()
    print(intCode)
    intCode[1] = 12
    intCode[2] = 2
    print(intCode)
    print("**************************************************")
    runIntcode(intCode)
    print("result should be:")
    print([30,1,1,4,2,5,6,0,99])

def runPartTwo():
    for noun in range(100):
        for verb in range(100):
            print("noun: {:3d} verb: {:3d}".format(noun, verb), end='')
            intCode = loadintCode()
            intCode[1] = noun
            intCode[2] = verb
            result = runIntcode(intCode, False)
            print("  {}".format(result[0]))
            if result[0] == 19690720:
                return 100*noun + verb



if __name__ == '__main__':
    runPartTwo()