import re
import copy

def get_values(string):
    
    result = re.search(r"move (\d+) from (\d+) to (\d+)", string)
    return list(map(int, result.groups()))
    
def part1(inputs, stacks):
    for item in inputs:
        num_to_move, stack_from, stack_to = get_values(item)
        # 0 indexing
        stack_from -= 1
        stack_to -= 1
        temporary_stack = []
        for _ in range(num_to_move):
            temporary_stack.append(stacks[stack_from].pop(0))
        
        for item in temporary_stack:
            stacks[stack_to].insert(0, item)
    
    return ("".join(stack[0] for stack in stacks))

def part2(inputs, stacks):
        
    for item in inputs:
        num_to_move, stack_from, stack_to = get_values(item)
        # 0 indexing
        stack_from -= 1
        stack_to -= 1
        temporary_stack = []
        for i in range(num_to_move):
            temporary_stack.append(stacks[stack_from].pop(0))
        # reverse insertion order for stacks
        for item in temporary_stack[::-1]:
            stacks[stack_to].insert(0, item)
    
    return ("".join(stack[0] for stack in stacks))
    
if __name__ == "__main__":
    with open("inputs/day5.txt") as f:
        inputs = f.read().splitlines()
    
    stacks = [
        ["W", "R", "T", "G"],
        ["W", "V", "S", "M", "P", "H", "C", "G"],
        ["M", "G", "S", "T", "L", "C"],
        ["F", "R", "W", "M", "D", "H", "J"],
        ["J", "F", "W", "S", "H", "L", "Q", "P"],
        ["S", "M", "F", "N", "D", "J", "P"],
        ["J", "S", "C", "G", "F", "D", "B", "Z"],
        ["B", "T", "R"],
        ["C", "L", "W", "N", "H"] 
    ]
      
    print(part1(inputs, copy.deepcopy(stacks)))
    print(part2(inputs, copy.deepcopy(stacks)))
            