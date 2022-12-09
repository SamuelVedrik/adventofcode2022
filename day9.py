from collections import defaultdict

def parse_inputs(inputs):
    instructions = []
    for item in inputs:
        direction, count = item.split(" ")
        instructions.extend([direction] * int(count))
    
    return instructions

def sign(x: int):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1
    
def touching(head, tail):
    headx, heady = head
    tailx, taily = tail
    dx = headx - tailx
    dy = heady - taily
    return (dx == 0 and dy == 0) or (abs(dx) == 1 and dy == 0) or (dx == 0 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 1)
    

def get_new_tail(head, tail):
    if touching(head, tail):
        return tail
    
    headx, heady = head
    tailx, taily = tail
    dx = headx - tailx
    dy = heady - taily
    return tail[0] + sign(dx), tail[1] + sign(dy)

    # # new pos if only 2 away
    # if (abs(dx) == 2 and dy == 0) or (dx == 0 and abs(dy) == 2):
    #     # only (-2, 0), (2, 0), (0, 2), (0, -2) possible, so this covers those cases 
    #     return tail[0] + (dx//2), tail[1] + (dy//2)
    # # move diagonal
    # else:
    #     if abs(dx < )
    
def move_head(head, instruction):
    if instruction == "R":
        return head[0] + 1, head[1]
    elif instruction == "L":
        return head[0] - 1, head[1]
    elif instruction == "U":
        return head[0] , head[1] + 1
    elif instruction == "D":
        return head[0] , head[1] - 1
    else: 
        raise ValueError

def part1(inputs):
    instructions = parse_inputs(inputs)
    # x, y coordinates
    head = (0, 0)
    tail = (0, 0)
    places_visited = set()
    
    for instruction in instructions:
        head = move_head(head, instruction)
        tail = get_new_tail(head, tail)
        places_visited.add(tail)
    
    # print(places_visited)
    print(len(places_visited))
    
def part2(inputs):
    instructions = parse_inputs(inputs)
    # H, 1, 2, 3 ... 9
    rope = [(0, 0)] * 10
    visited = set()
    
    for instruction in instructions:
        rope[0] = move_head(rope[0], instruction)
        for i, tail in enumerate(rope[1:]):
            index = i + 1
            rope[index] = get_new_tail(rope[index-1], tail)
        visited.add(rope[-1])
    
    print(len(visited))
    

if __name__ == "__main__":
    
    with open("inputs/day9.txt") as f:
        inputs = f.read().splitlines()
    
    part1(inputs)
    part2(inputs)