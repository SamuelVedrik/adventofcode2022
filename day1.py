import numpy as np

def part1():
    with open("inputs/day1.txt") as f:
        inputs = f.read()
        inputs = inputs.split("\n\n")
    max_ = 0
    for input_ in inputs:
        input_ = list(map(int, input_.split("\n")))
        max_ = max(max_, sum(input_))
    print(max_)

def part2():
    with open("inputs/day1.txt") as f:
        inputs = f.read()
        inputs = inputs.split("\n\n")
    per_elf = np.array([sum(list(map(int, input_.split("\n")))) for input_ in inputs])
    print(np.sort(per_elf)[-3:].sum())
    
    
if __name__ == "__main__":
    part2()
    
    
    
    