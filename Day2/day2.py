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

def runIntcode(intInput):
    for idx, val in enumerate(intInput):
        #print("index is %d and value is %s" % (idx, val))
        print("Index: {}".format(idx))
        print(intInput)
        #readOpCode(val)
        if val == 1:
            print("add({}, {}, {})".format(intInput[idx+1], intInput[idx+2], intInput[idx+3]))
            print("L[{}] = {} + {} = {}".format(intInput[idx+3], intInput[intInput[idx+1]], intInput[intInput[idx+2]], intInput[intInput[idx+1]] + intInput[intInput[idx+2]]))
            intInput[intInput[idx+3]] = intInput[intInput[idx+1]] + intInput[intInput[idx+2]]
        elif val == 2:
            print("mul({}, {}, {})".format(intInput[idx+1], intInput[idx+2], intInput[idx+3]))
            print("L[{}] = {} * {} = {}".format(intInput[idx+3], intInput[intInput[idx+1]], intInput[intInput[idx+2]], intInput[intInput[idx+1]] * intInput[intInput[idx+2]]))
            intInput[intInput[idx+3]] = intInput[intInput[idx+1]] * intInput[intInput[idx+2]]
        elif val == 99:
            print("break")
            return(intInput)
            break

