# https://adventofcode.com/2019/day/2
# 
# --- Day 2: 1202 Program Alarm ---
#
#
# 

def readOpCode(op):
    if op == 1:
        print("add")
    else if op == 2:
        print("mul")
    else if op == 99:
        print("break")

intInput = [1,9,10,3,2,3,11,0,99,30,40,50]

for idx, val in enumerate(intInput):
  print("index is %d and value is %s" % (idx, val))