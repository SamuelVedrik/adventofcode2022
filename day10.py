import numpy as np

BLACK = "⬛"
WHITE = "⬜"
def create_range_dict(inputs):
    X = 1
    curr_start = 1
    curr_end = 1
    # [i, j) = this value
    range_dict = {}
    for item in inputs:
        if item == "noop":
            curr_end += 1
        else:
            val = int(item.split(" ")[1])
            curr_end += 2
            range_dict[curr_start, curr_end] = X
            curr_start = curr_end
            X += val
    # If no addx at end, helps with that
    range_dict[curr_start, 300] = X
        
    return range_dict

def part1(range_dict):
    items = [20, 60, 100, 140, 180, 220]
    signal_strength = 0
    for item in items:
        for (l, r), val in range_dict.items():
            if l <= item < r:
                signal_strength += (item * val)
                # print(item, val)
                break
    print(signal_strength)
    
def convert_range_to_cycle(range_dict):
    cycle = {}
    for (l, r), val in range_dict.items():
        for i in range(l, r):
            cycle[i] = val
    
    return cycle

def render_monitor(monitor):
    for i in range(6):
        print("".join(monitor[(i*40):((i+1)*40)]))

if __name__ == "__main__":
    with open("inputs/day10.txt") as f:
        inputs = f.read().splitlines()
    
    range_dict = create_range_dict(inputs)
    part1(range_dict)
    cycle_dict = convert_range_to_cycle(range_dict)
    monitor = [BLACK] * 240
    for i in range(240):
        middle_sprite_pos = cycle_dict[i+1]
        row_pos = i % 40
        if middle_sprite_pos-1 <= row_pos <= middle_sprite_pos +1:
            monitor[i] = WHITE
    render_monitor(monitor)
    