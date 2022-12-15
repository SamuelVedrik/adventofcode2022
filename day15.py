from parse import compile
from itertools import combinations
from collections import defaultdict
from tqdm import tqdm

def parse_inputs(inputs):
    sensors = []
    beacons = []
    parse_string = "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}"
    parser = compile(parse_string)
    for item in inputs:
        result = parser.parse(item)
        sensors.append(complex(result[0], result[1]))
        beacons.append(complex(result[2], result[3]))
    
    return sensors, beacons

def overlaps(range1, range2):
    ll, lr = range1
    rl, rr = range2
    return (rl <= lr+1 and ll < rr) or (ll <= rr+1 and rl < lr)

def dfs(visited, adjacency, connected, item):
    
    visited[item] = True
    connected.append(item)
    
    for neighbor in adjacency[item]:
        if not visited[neighbor]:
            dfs(visited, adjacency, connected, neighbor)

def get_connected_ranges(ranges):
    
    adjacency = defaultdict(list)
    for range1, range2 in combinations(ranges, 2):
        if overlaps(range1, range2):
            adjacency[range1].append(range2)
            adjacency[range2].append(range1)

    visited = defaultdict(lambda: False)
    connected_ranges = []
    for range_ in ranges:
        if not visited[range_]:
            connected = []
            dfs(visited, adjacency, connected, range_)
            left = min(item[0] for item in connected)
            right = max(item[1] for item in connected)
            connected_ranges.append((left, right))
    
    return connected_ranges
    
            
    
def get_impossible_at_y(sensors: list[complex], beacons: list[complex], y: int):
    
    ranges = []
    for sensor, beacon in zip(sensors, beacons):
        vector = (sensor - beacon)
        magnitude = abs(vector.real) + abs(vector.imag)
        around = magnitude - abs(sensor.imag - y)
        if around >= 0:
            ranges.append((sensor.real - around, sensor.real + around))
    
    connected_ranges = get_connected_ranges(ranges)
    return connected_ranges

if __name__ == "__main__":
    with open("inputs/day15.txt") as f:
        inputs = f.read().splitlines()
    
    sensors, beacons = parse_inputs(inputs)
    impossible_ranges = get_impossible_at_y(sensors, beacons, y=2000000)
    print(sum(r-l for l, r in impossible_ranges))
    for i in tqdm(range(4000000)):
        impossible_ranges = get_impossible_at_y(sensors, beacons, y=i)
        if len(impossible_ranges) > 1:
            ranges = sorted(impossible_ranges, key=lambda x: x[0])
            print(((ranges[0][1] + 1) * 4000000) + i)
            