# --- Day 10: Monitoring Station ---

def read_file(name):
    with open(f"files/input{name}") as f:
        content = f.readlines()
    return [x.strip() for x in content]

def run_small_test():
    print("small test")
    return 0

if __name__ == '__main__':
    #runPartOne()
    run_small_test()
    #runPartTwo()