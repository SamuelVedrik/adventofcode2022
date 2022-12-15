def parse_inputs(inputs):
    rocks = set()
    lowest_x = float("inf")
    highest_y = 0
    for item in inputs:
        rocks_str = item.split(" -> ")
        for left, right in zip(rocks_str, rocks_str[1:]):
            ll, lr = list(map(int, left.split(",")))
            rl, rr = list(map(int, right.split(",")))
            left = complex(ll, lr)
            right = complex(rl, rr)
            vector = right - left
            # since only on axes, this works to calculate magnitude + unit vector
            magnitude = abs(vector)
            unit = vector / magnitude
            for i in range(int(magnitude)+1):
                new_vector = left + (i * unit)
                rocks.add(new_vector)
                highest_y = max(highest_y, new_vector.imag)
                lowest_x = min(lowest_x, new_vector.real)
    
    return rocks, int(highest_y), int(lowest_x)
            
            
def get_first_contact(rocks: set, sand: set, last_rock: int):
    
    obstacles = rocks.union(sand)
    curr = 500
    for _ in range(last_rock):
        # check if can move into one below
        if curr + 1j not in obstacles:
            curr = curr + 1j
        # check if can move left diagonal
        elif curr + (-1+1j) not in obstacles:
            curr = curr + (-1+1j)
        # check if can move right diagonal
        elif curr + (1+1j) not in obstacles:
            curr = curr + (1+1j)
        # 
        else:
            return curr

    # we are past last Y now
    return None

            
def get_first_contact_p2(rocks: set, sand: set, last_rock: int):
    
    obstacles = rocks.union(sand)
    curr = 500
    for _ in range(last_rock):
        # check if can move into one below
        if curr + 1j not in obstacles:
            curr = curr + 1j
        # check if can move left diagonal
        elif curr + (-1+1j) not in obstacles:
            curr = curr + (-1+1j)
        # check if can move right diagonal
        elif curr + (1+1j) not in obstacles:
            curr = curr + (1+1j)
        # 
        else:
            return curr

    # we are past last Y now
    return curr
    
def part1(inputs):
    rocks, highest_y, _ = parse_inputs(inputs)
    sand = set()
    while True:
        drop = get_first_contact(rocks, sand, highest_y)
        if drop is not None:
            sand.add(drop)
        else:
            break
    
    print(len(sand))
    
if __name__ == "__main__":
    with open("inputs/day14.txt") as f:
        inputs = f.read().splitlines()
    
    rocks, highest_y, lowest_x = parse_inputs(inputs)
    
    sand = set()
    while True:
        drop = get_first_contact_p2(rocks, sand, highest_y+1)
        if drop == 500:
            break
        sand.add(drop)

    print(len(sand) + 1)
    