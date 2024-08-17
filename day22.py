import numpy as np

# R, D, L, U in that order
vectors = [
    np.array([0, 1]),
    np.array([1, 0]),
    np.array([0, -1]),
    np.array([-1, 0])
]

def parse_map(map_):
    items = []
    max_len = 0
    for line in map_:
        line = line.replace(" ", "0")
        line = line.replace(".", "1")
        line = line.replace("#", "2")
        max_len = max(max_len, len(line))
        items.append(line)
    
    for i, item in enumerate(items):
        padded = item.ljust(max_len, "0")
        items[i] = np.array(list(map(int, list(padded))))
    
    return np.stack(items)

def parse_instructions(instructions):
    
    instructions_list = []
    idx = 0
    current = ""
    while idx < len(instructions):
        if instructions[idx].isnumeric():
            current += instructions[idx]
        else:
            instructions_list.append(int(current))
            instructions_list.append(instructions[idx])
            current = ""
        idx += 1
    
    if current != "":
        instructions_list.append(int(current))
        
    return instructions_list

def get_wrap(map_, pos, direction):
    # RIGHT
    if direction == 0:
        
        right_most = (map_[pos[0], :] != 0).argmax()
        return np.array([pos[0], right_most])
    # DOWN
    elif direction == 1:
        bottom_most = (map_[:, pos[1]] != 0).argmax()
        return np.array([bottom_most, pos[1]])
    # LEFT
    elif direction == 2:
        left_most = map_.shape[1] - 1 - (map_[pos[0], ::-1] != 0).argmax()
        return np.array([pos[0], left_most])
    # UP
    elif direction == 3:
        top_most =  map_.shape[0] - 1 - (map_[::-1, pos[1]] != 0).argmax()
        return np.array([top_most, pos[1]])
    else:
        raise ValueError(f"Invalid Direction {direction}")
    
def update_curr(map_, pos, direction, instruction):
    wrap = get_wrap(map_, pos, direction)
    when_to_wrap = get_wrap(map_, pos, (direction + 2) % 4) + vectors[direction]
    num_move = 0
    curr = pos
    while num_move < instruction:
        destination = curr + vectors[direction]
        if (destination == (when_to_wrap)).all():
            destination = wrap
        if map_[destination[0], destination[1]] == 2:
            return curr
        curr = destination
        num_move += 1
    return curr
    
def follow_instructions(map_, instructions_):
    initial = np.array([0, (map_[0, :] == 1).argmax()])
    curr = initial
    direction = 0
    for instruction in instructions_:
        if instruction == "R":
            direction = (direction + 1) % 4
        elif instruction == "L":
            direction = (direction - 1) % 4
        else:
            curr = update_curr(map_, curr, direction, instruction)
    
    return (1000 * (curr[0]+1)) + (4 * (curr[1]+1)) + direction
        
    

if __name__ == "__main__":
    
    with open("inputs/day22.txt") as f:
        map_, instructions = f.read().split("\n\n")
        map_ = map_.splitlines()
    
    map_ = parse_map(map_)
    instructions = parse_instructions(instructions)
    print(follow_instructions(map_, instructions))
    
    