import numpy as np
import heapq
from collections import defaultdict
from tqdm import tqdm

alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_map = {char: i for i, char in enumerate(alphabet)}
alphabet_map["S"] = -1
alphabet_map["E"] = 26

def parse_inputs(inputs):
    result = [[alphabet_map[char] for char in item] for item in inputs]
    result = np.array(result)
    start = np.nonzero(result == -1)
    end = np.nonzero(result == 26)
    result = np.clip(result, 0, 25)
    return result, tuple(np.transpose(start).flatten()), tuple(np.transpose(end).flatten())

def parse_inputs_2(inputs):
    result = [[alphabet_map[char] for char in item] for item in inputs]
    result = np.array(result)
    
    end = tuple(np.transpose(np.nonzero(result == 26)).flatten())
    result[result == 26] = 25
    
    result[result == -1] = 0
    starts = np.transpose(np.nonzero(result == 0))
    starts_tuple = [tuple(starts[i, :]) for i in range(starts.shape[0])]
    
    return result, starts_tuple, end
    
            
def get_adj(i, j, grid): 
    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    valid_neighbors = []
    for (ni, nj) in neighbors:
        if (0 <= ni < grid.shape[0]) and (0 <= nj < grid.shape[1]) and (grid[ni, nj] <= grid[i, j] + 1):
            valid_neighbors.append((ni, nj))

    return valid_neighbors

def min_cost_bfs(grid, start, end):
    pqueue = []
    heapq.heappush(pqueue, (0, start, {start}))
    visited_cheapest = defaultdict(lambda: np.inf)
    while pqueue:
        path_length, curr_node, visited = heapq.heappop(pqueue)
        if curr_node == end:
            return path_length
        children = get_adj(*curr_node, grid)
        for child in children:
            new_path_length = path_length + 1
            if child not in visited and visited_cheapest[child] > new_path_length:
                heapq.heappush(pqueue, (new_path_length, child, visited | {child}))
                visited_cheapest[child] = new_path_length
    
    return np.inf
                
def part1(inputs):
    grid, start, end = parse_inputs(inputs)
    print(min_cost_bfs(grid, start, end))
                
def part2(inputs):
    grid, all_starts, end = parse_inputs_2(inputs)
    min_ = np.inf
    for start in tqdm(all_starts):
        val = min_cost_bfs(grid, start, end)
        min_ = min(min_, val)
    
    print(min_)
    
if __name__ == "__main__":
    
    with open("inputs/day12.txt") as f:
        inputs = f.read().splitlines()
    
    part1(inputs)
    part2(inputs)
    