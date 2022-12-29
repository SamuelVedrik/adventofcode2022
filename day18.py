from itertools import combinations, product
import numpy as np

def check_air_pocket(coord, cube_coords):
    closed_sides = 0
    dv = (cube_coords - coord)
    
    closed_sides += ((dv[:, 0] >= 1) & (dv[:, 1] == 0) & (dv[:, 2] == 0)).any()
    closed_sides += ((dv[:, 0] == 0) & (dv[:, 1] >= 1) & (dv[:, 2] == 0)).any()
    closed_sides += ((dv[:, 0] == 0) & (dv[:, 1] == 0) & (dv[:, 2] >= 1)).any()
    
    closed_sides += ((dv[:, 0] <= -1) & (dv[:, 1] == 0) & (dv[:, 2] == 0)).any()
    closed_sides += ((dv[:, 0] == 0) & (dv[:, 1] <= -1) & (dv[:, 2] == 0)).any()
    closed_sides += ((dv[:, 0] == 0) & (dv[:, 1] == 0) & (dv[:, 2] <= -1)).any()
    
    
    return closed_sides == 6
    

def parse_inputs(inputs):
    cubes = []
    for item in inputs:
        coords = np.array(list(map(int, item.split(","))))
        cubes.append(coords)
    return np.stack(cubes)
    
def part1(inputs):
    
    cubes = parse_inputs(inputs)
    sa = 0
    for cube in cubes:
        dv = (cubes - cube)
        sides = 6
        
        sides -= ((dv[:, 0] == 1) & (dv[:, 1] == 0) & (dv[:, 2] == 0)).any()
        sides -= ((dv[:, 0] == 0) & (dv[:, 1] == 1) & (dv[:, 2] == 0)).any()
        sides -= ((dv[:, 0] == 0) & (dv[:, 1] == 0) & (dv[:, 2] == 1)).any()
        
        sides -= ((dv[:, 0] == -1) & (dv[:, 1] == 0) & (dv[:, 2] == 0)).any()
        sides -= ((dv[:, 0] == 0) & (dv[:, 1] == -1) & (dv[:, 2] == 0)).any()
        sides -= ((dv[:, 0] == 0) & (dv[:, 1] == 0) & (dv[:, 2] == -1)).any()
        sa += sides
    
    print(sa)
    
def get_raw_neighbors(current):
    x, y, z = current
    neighbors = [
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1)
    ]
    return neighbors
    
    
def get_neighbors(current, visited, grid_set, cube_set): 
    candidate_neighbors = get_raw_neighbors(current)
    neighbors = []
    for candidate in candidate_neighbors:
        if (current != candidate) and (candidate not in visited) and (candidate not in cube_set) and (candidate in grid_set):
            neighbors.append(candidate)
    
    return neighbors
        
def explore_graph(grid_set, cube_set, initial):
    
    visited = set()
    to_visit = [] # stack
    current = initial
    to_visit.append(current)
    
    while to_visit:
        current = to_visit.pop()
        visited.add(current)
        neighbors = get_neighbors(current, visited, grid_set, cube_set)
        for neighbor in neighbors:
            to_visit.append(neighbor)
    
    return visited, grid_set - cube_set - visited
            

if __name__ == "__main__":
    with open("inputs/day18.txt") as f:
        inputs = f.read().splitlines()
    
    cubes = parse_inputs(inputs)
    min_x, min_y, min_z = cubes.min(axis=0)
    max_x, max_y, max_z = cubes.max(axis=0)
    grid = np.meshgrid(np.arange(min_x-1, max_x+2, 1), np.arange(min_y-1, max_y+2, 1), np.arange(min_z-1, max_z+2, 1))
    grid = np.array(grid).reshape(3, -1).T
    
    grid_set = set(map(tuple, grid))
    cube_set = set(map(tuple, cubes))
    initial = tuple(grid[0, :])
    exposed_air, pocket_air = explore_graph(grid_set, cube_set, initial)
    sa = 0
    for cube in cube_set:
        neighbors = get_raw_neighbors(cube)
        sa += len(set(neighbors) - cube_set - pocket_air)
    
    print(sa)
    
    