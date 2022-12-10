import numpy as np

BLACK = "⬛"
WHITE = "⬜"

def create_cycles(inputs):
    cycles = [1]
    for item in inputs:
        cycles.append(cycles[-1])
        if item != "noop":
            val = int(item.split(" ")[1])
            cycles.append(cycles[-1] + val)
    return cycles
            
def render_monitor(monitor):
    for i in range(6):
        print("".join(monitor[(i*40):((i+1)*40)]))

if __name__ == "__main__":
    with open("inputs/day10.txt") as f:
        inputs = f.read().splitlines()
    
    cycle_list = create_cycles(inputs)
    
    items = [20, 60, 100, 140, 180, 220]
    signal_strength = 0
    for item in items:
        signal_strength += (cycle_list[item-1] * item)
    print(signal_strength)
    
    monitor = [BLACK] * 240
    for i in range(240):
        middle_sprite_pos = cycle_list[i]
        row_pos = i % 40
        if middle_sprite_pos-1 <= row_pos <= middle_sprite_pos +1:
            monitor[i] = WHITE
    render_monitor(monitor)
    