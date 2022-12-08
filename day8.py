import numpy as np

def check_visible(inputs, i, j):
    curr = inputs[i, j]
    left = inputs[i, :j]
    right = inputs[i, j+1:]
    top = inputs[:i, j]
    bottom = inputs[i+1:, j]
    
    return all(left < curr) or all(right < curr) or all(top < curr) or all(bottom < curr)

def get_scenic_score(inputs, i, j):
    curr = inputs[i, j]
    left = inputs[i, :j]
    right = inputs[i, j+1:]
    top = inputs[:i, j]
    bottom = inputs[i+1:, j]
    
    # Finds first index that is True (has to be reserved since we are parsing from right to left)
    if any(left >= curr):
        left_score = (left >= curr)[::-1].argmax() + 1
    else:
        left_score = j
    if any(right >= curr):
        right_score = (right >= curr).argmax() + 1
    else:
        right_score = inputs.shape[1] - j - 1
    
    if any(top >= curr):
        top_score = (top >= curr)[::-1].argmax() + 1
    else:
        top_score = i
    
    if any(bottom >= curr):
        bottom_score = (bottom >= curr).argmax() + 1   
    else:
        bottom_score = inputs.shape[0] - i -1
        
    return left_score *right_score * top_score * bottom_score

def part1(inputs):
        
    num_visible = 0
    for i in range(1, inputs.shape[0]-1):
        for j in range(1, inputs.shape[1]-1):
            num_visible += int(check_visible(inputs, i, j))
    
    edge = (inputs.shape[0] * inputs.shape[1]) - ((inputs.shape[0] -2) * (inputs.shape[1] - 2))
    print(num_visible + edge)

def part2(inputs):
    max_ = 0
    for i in range(1, inputs.shape[0]-1):
        for j in range(1, inputs.shape[1]-1):
            score = get_scenic_score(inputs, i, j)
            max_ = max(max_, score)
    print(max_)

if __name__ == "__main__":
    with open("inputs/day8.txt") as f:
        inputs = f.read().splitlines()
        inputs = [list(map(int, item)) for item in inputs]
        inputs = np.array(inputs)
    
    part1(inputs)
    part2(inputs)