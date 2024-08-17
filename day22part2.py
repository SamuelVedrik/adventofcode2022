from typing import Union
import numpy as np

# R, D, L, U in that order
DIRECTIONS = ["R", "D", "L", "U"]

VECTORS = [
    np.array([0, 0, 1]),
    np.array([0, 1, 0]),
    np.array([0, 0, -1]),
    np.array([0, -1, 0])
]

MAP_GRAPH = {
    "0U": "5L",
    "0D": "2U",
    "0L": "3L",
    "0R": "1L",

    "1U": "5D",
    "1D": "2R", 
    "1L": "0R",
    "1R": "4R",

    "2U": "0D",
    "2D": "4U",
    "2L": "3U",
    "2R": "1D",

    "3U": "2L",
    "3D": "5U",
    "3L": "0L", 
    "3R": "4L",

    "4U": "2D",
    "4D": "5R",
    "4L": "3R",
    "4R": "1R",

    "5U": "3D",
    "5D": "1U",
    "5L": "0U",
    "5R": "4D"
}


def parse_map(map_):
    map_ = [list(line.strip()) for line in map_]
    face12 = np.array(map_[:50]) 
    face3 = np.array(map_[50:100])
    face45 = np.array(map_[100:150])
    face6 = np.array(map_[150:])

    np_map = np.zeros(shape=(6, 50, 50))
    np_map[0, :, :] = np.where(face12[:, :50] == ".", 1, 2)
    np_map[1, :, :] = np.where(face12[:, 50:] == ".", 1, 2)
    np_map[2, :, :] = np.where(face3 == ".", 1, 2 )
    np_map[3, :, :] = np.where(face45[:, :50] == ".", 1, 2,)
    np_map[4, :, :] = np.where(face45[:, 50:] == ".", 1, 2)
    np_map[5, :, :] = np.where(face6 == ".", 1, 2)
    return np_map
    

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

def get_r_wraps(position, oriface):

    if oriface == "R":
        return np.array([49-position[1], 49])
    if oriface == "D":
        return np.array([position[2], 49])
    if oriface == "L":
        return np.array([position[1], 49])
    if oriface == "U":
        return np.array([49-position[2], 49])

def get_d_wraps(position, oriface):
    if oriface == "R":
        return np.array([49, position[1]])
    if oriface == "D":
        return np.array([49, 49-position[2]])
    if oriface == "L":
        return np.array([49, 49-position[1]])
    if oriface == "U":
        return np.array([49, position[2]])

def get_l_wraps(position, oriface):
    if oriface == "R":
        return np.array([position[1], 0])
    if oriface == "D":
        return np.array([49-position[2], 0])
    if oriface == "L":
        return np.array([49-position[1], 0])
    if oriface == "U":
        return np.array([position[2], 0])

def get_u_wraps(position, oriface):
    if oriface == "R":
        return np.array([0, 49-position[1]])
    if oriface == "D":
        return np.array([0, position[2]])
    if oriface == "L":
        return np.array([0, position[1]])
    if oriface == "U":
        return np.array([0, 49-position[2]])


def get_wrap(position, direction):
    """
    Returns wrap point
    """
    curr_dir = DIRECTIONS[direction]
    curr_face = str(position[0]) + curr_dir
    target_face = MAP_GRAPH[curr_face]
    target_face_num, target_face_dir = int(target_face[0]), target_face[1]

    if target_face_dir == "R":
        to_wrap = get_r_wraps(position, curr_dir)
    elif target_face_dir == "D":
        to_wrap = get_d_wraps(position, curr_dir)
    elif target_face_dir == "L":
        to_wrap = get_l_wraps(position, curr_dir)
    elif target_face_dir == "U":
        to_wrap = get_u_wraps(position, curr_dir)
    else:
        raise ValueError(f"Unknown Direction {target_face_dir}")
    
    to_wrap = np.r_[target_face_num, to_wrap]
    new_direction = (DIRECTIONS.index(target_face_dir) + 2) % 4
    return to_wrap, new_direction

def get_when_to_wrap(position, direction):

    current_face_num = position[0]
    current_face_dir = DIRECTIONS[direction]

    if current_face_dir == "R":
        return np.array([current_face_num, position[1], 50])
    if current_face_dir == "D":
        return np.array([current_face_num, 50, position[2]])
    if current_face_dir == "L":
        return np.array([current_face_num, position[1], -1])
    if current_face_dir == "U":
        return np.array([current_face_num, -1, position[2]])
    raise ValueError(f"Unknown Direction {current_face_dir}")

def update_curr(map_: np.array, position: np.array, direction: int, instruction: int):
    current = position
    num_moves = 0
    while num_moves < instruction:
        wrap, new_direction = get_wrap(current, direction)
        when_to_wrap = get_when_to_wrap(current, direction)
        destination = current + VECTORS[direction]
        if (destination == when_to_wrap).all():
            destination = wrap
        if map_[destination[0], destination[1], destination[2]] == 2:
            return current, direction
        # only change direction when you actually wrap
        if (destination == wrap).all():
            direction = new_direction 
        current = destination
        num_moves += 1
    return current, direction

def follow_instructions(map_: np.array, instructions: list[Union[str, int]]):
    curr = np.array([0, 0, 0])
    direction = 0
    for instruction in instructions:
        if instruction == "R":
            direction = (direction + 1) % 4
        elif instruction == "L":
            direction = (direction - 1) % 4
        else:
            curr, direction = update_curr(map_, curr, direction, instruction)

    row = curr[1]
    if curr[0] == 2:
        row += 50
    elif curr[0] == 3 or curr[0] == 4:
        row += 100
    elif curr[0] == 5:
        row += 150

    column = curr[2]
    if curr[0] == 0 or curr[0] == 2 or curr[0] == 4:
        column += 50
    if curr[0] == 1:
        column += 100

    return (1000 * (row+1)) + (4 * (column+1)) + direction
    
if __name__ == "__main__":
    
    with open("inputs/day22.txt") as f:
        map_, instructions = f.read().split("\n\n")
        map_ = map_.splitlines()
    
    map_ = parse_map(map_)
    instructions = parse_instructions(instructions)
    print(follow_instructions(map_, instructions))

