from parse import compile
import heapq
from copy import deepcopy
from collections import defaultdict
from itertools import permutations, combinations
from tqdm import tqdm
from frozendict import frozendict
from functools import lru_cache

def parse_inputs(inputs):
    graph = {}
    flow_rates = {}
    parser = compile("Valve {} has flow rate={:d}; tunnels lead to valves {}")
    for item in inputs:
        item = item.replace("valve ", "valves ")
        item = item.replace("tunnel ", "tunnels ")
        item = item.replace("leads ", "lead ")
        valve, flow_rate, neighbors = parser.parse(item)
        neighbors = neighbors.split(", ")
        graph[valve] = neighbors
        flow_rates[valve] = flow_rate
    
    return graph, flow_rates

def get_shortest_path(graph, start, target):
    heap = []
    heapq.heappush(heap, (0, start, [start]))
    visited_cheapest = defaultdict(lambda: float('inf'))
    while heap:
        path_length, curr_node, path = heapq.heappop(heap)
        if curr_node == target:
            return path_length, tuple(path)
        children = graph[curr_node]
        for child in children:
            new_path_length = path_length + 1
            if child not in path and visited_cheapest[child] > new_path_length:
                heapq.heappush(heap, (new_path_length, child, path + [child]))
                visited_cheapest[child] = new_path_length
    
    return None

def simplify_graph(graph, flow_rates):
    new_graph = {}
    nodes_to_visit = [node for node in flow_rates if flow_rates[node] > 0]
    for nodeA, nodeB in permutations(nodes_to_visit + ["AA"], 2):
        new_graph[nodeA, nodeB] = get_shortest_path(graph, nodeA, nodeB)
    return new_graph, nodes_to_visit
    
def get_pressure(route, new_graph, flow_rates, max_time=26):
    valve_dict = {} # key: valve value: how many minutes open
    current = 0
    for start, target in zip(route, route[1:]):
        current = current + new_graph[start, target][0] + 1
        valve_dict[target] = current
    
    total_pressure = 0
    for valve, min_on in valve_dict.items():
        total_pressure += max((max_time-min_on) * flow_rates[valve], 0)
    
    return total_pressure


def get_pressure_with_dict(route, new_graph, flow_rates, max_time=30):
    valve_dict = {} # key: valve value: how many minutes open
    current = 0
    for start, target in zip(route, route[1:]):
        current = current + new_graph[start, target][0] + 1
        valve_dict[target] = current
    
    total_pressure = 0
    for valve, min_on in valve_dict.items():
        total_pressure += max((max_time-min_on) * flow_rates[valve], 0)
    
    return total_pressure, valve_dict


def get_best(current_route, new_graph, flow_rates, nodes_to_visit, cache, pbar, max_time):
    
    key = frozenset(current_route[:-1]), current_route[-1], frozenset(nodes_to_visit)
    if key in cache:
        return cache[key]
    
    pbar.update(1)
    if len(current_route) == len(nodes_to_visit) + 1:
        cache[key] = tuple([current_route[-1]])
        return tuple([current_route[-1]])
    
    best = None
    max_pressure = 0
    for other in nodes_to_visit:
        if other not in current_route:
            candidate_extension = tuple(list(current_route)+[other])
            best_route_extension = get_best(candidate_extension, new_graph, flow_rates, nodes_to_visit, cache, pbar, max_time)
            best_route = tuple(list(current_route) + list(best_route_extension))
            pressure = get_pressure(best_route, new_graph, flow_rates, max_time)
            if pressure > max_pressure:
                max_pressure = pressure
                best = tuple([current_route[-1]] + list(best_route_extension))
                
    cache[key] = best
    return best
    
def part1(inputs):
    graph, flow_rates = parse_inputs(inputs)
    new_graph, nodes_to_visit = simplify_graph(graph, flow_rates)
    
    cache = {}
    pbar = tqdm()
    best_route = get_best(("AA", ), new_graph, flow_rates, nodes_to_visit, cache, pbar, max_time=30)
    print(best_route)
    print(get_pressure(best_route, new_graph, flow_rates, max_time=30))
    
if __name__ == "__main__":
    with open("inputs/day16.txt") as f:
        inputs = f.read().splitlines()
    
    graph, flow_rates = parse_inputs(inputs)
    new_graph, nodes_to_visit = simplify_graph(graph, flow_rates)
    nodes_to_visit = set(nodes_to_visit)
    
    cache = {}
    pbar = tqdm()
    
    best_pressure = 0
    best_elephant = None
    best_mine = None
    
    min_jobs = 6
    
    for length in range(min_jobs, len(nodes_to_visit)+1-min_jobs):
        for comb in combinations(nodes_to_visit, length):
            elephant_job = set(comb)
            my_job = nodes_to_visit - elephant_job
            elephant_route = get_best(("AA", ), new_graph, flow_rates, elephant_job, cache, pbar, max_time=26)
            my_route = get_best(("AA", ), new_graph, flow_rates, my_job, cache, pbar, max_time=26)
            pressure = get_pressure(elephant_route, new_graph, flow_rates, max_time=26) + get_pressure(my_route, new_graph, flow_rates, max_time=26)
            if pressure > best_pressure:
                best_pressure = pressure
                best_elephant = elephant_route
                best_mine = my_route
                
    print("\n", best_pressure)
    print(best_elephant)
    print(best_mine)