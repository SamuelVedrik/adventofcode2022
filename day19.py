from parse import compile
from dataclasses import dataclass, field
from tqdm import tqdm
from functools import lru_cache

NUM_MINUTES = 32

@dataclass(unsafe_hash=True)
class OreState:
    minute: int = field(hash=True)
    num_ore_robots: int = field(hash=True)
    num_clay_robots: int = field(hash=True)
    num_obsidian_robots: int = field(hash=True)
    num_geode_robots: int = field(hash=False)
    
    num_ore: int = field(hash=True)
    num_clay: int = field(hash=True)
    num_obsidian: int = field(hash=True)
    num_geodes: int = field(hash=False)
        
    def collect(self):
        
        new_state = OreState(
            minute = self.minute + 1,
            num_ore_robots = self.num_ore_robots,
            num_clay_robots = self.num_clay_robots,
            num_obsidian_robots = self.num_obsidian_robots,
            num_geode_robots = self.num_geode_robots,
            num_ore = self.num_ore + self.num_ore_robots,
            num_clay = self.num_clay + self.num_clay_robots,
            num_obsidian = self.num_obsidian + self.num_obsidian_robots,
            num_geodes = self.num_geodes + self.num_geode_robots,
        )
        
        return new_state

    def buy_ore_robot(self, ore_cost):
        
        if self.num_ore >= ore_cost:
            new_state = OreState(
                minute = self.minute + 1,
                num_ore_robots = self.num_ore_robots+1,
                num_clay_robots = self.num_clay_robots,
                num_obsidian_robots = self.num_obsidian_robots,
                num_geode_robots = self.num_geode_robots,
                num_ore = self.num_ore + self.num_ore_robots - ore_cost,
                num_clay = self.num_clay + self.num_clay_robots,
                num_obsidian = self.num_obsidian + self.num_obsidian_robots,
                num_geodes = self.num_geodes + self.num_geode_robots,
            )
            
            return new_state
        else:
            return None
    
    def buy_clay_robot(self, ore_cost):
        
        if self.num_ore >= ore_cost:
            new_state = OreState(
                minute = self.minute + 1,
                num_ore_robots = self.num_ore_robots,
                num_clay_robots = self.num_clay_robots+1,
                num_obsidian_robots = self.num_obsidian_robots,
                num_geode_robots = self.num_geode_robots,
                num_ore = self.num_ore + self.num_ore_robots - ore_cost,
                num_clay = self.num_clay + self.num_clay_robots,
                num_obsidian = self.num_obsidian + self.num_obsidian_robots,
                num_geodes = self.num_geodes + self.num_geode_robots,
            )
            
            return new_state
        else:
            return None
    
    def buy_obs_robot(self, ore_cost, clay_cost):
        
        if self.num_ore >= ore_cost and self.num_clay >= clay_cost:
            new_state = OreState(
                minute = self.minute + 1,
                num_ore_robots = self.num_ore_robots,
                num_clay_robots = self.num_clay_robots,
                num_obsidian_robots = self.num_obsidian_robots+1,
                num_geode_robots = self.num_geode_robots,
                num_ore = self.num_ore + self.num_ore_robots - ore_cost,
                num_clay = self.num_clay + self.num_clay_robots - clay_cost,
                num_obsidian = self.num_obsidian + self.num_obsidian_robots,
                num_geodes = self.num_geodes + self.num_geode_robots,
            )
            
            return new_state
        else:
            return None
        
    def buy_geode_robot(self, ore_cost, obs_cost):
        
        if self.num_ore >= ore_cost and self.num_obsidian >= obs_cost:
            new_state = OreState(
                minute = self.minute + 1,
                num_ore_robots = self.num_ore_robots,
                num_clay_robots = self.num_clay_robots,
                num_obsidian_robots = self.num_obsidian_robots,
                num_geode_robots = self.num_geode_robots+1,
                num_ore = self.num_ore + self.num_ore_robots - ore_cost,
                num_clay = self.num_clay + self.num_clay_robots,
                num_obsidian = self.num_obsidian + self.num_obsidian_robots - obs_cost,
                num_geodes = self.num_geodes + self.num_geode_robots,
            )
            
            return new_state
        else:
            return None
        
    def upperbound_geodes(self):
        
        from_current = self.num_geode_robots * (NUM_MINUTES - self.minute)
        from_future = sum(i for i in range(1, (NUM_MINUTES - self.minute)))
        return self.num_geodes + from_future + from_current
    
        
def get_next(ore_state: OreState, ore_cost, clay_cost, obs_cost, geode_cost):
    all_actions = [
        ore_state.collect(), 
        ore_state.buy_ore_robot(ore_cost), 
        ore_state.buy_clay_robot(clay_cost), 
        ore_state.buy_obs_robot(*obs_cost), 
        ore_state.buy_geode_robot(*geode_cost),
    ] 
    
    valid_actions = [action for action in all_actions if action and action.minute <= NUM_MINUTES]
    return valid_actions

# INSIGHTS: 
# If you have enough to buy a robot and you don't buy immediately, it's never going to be optimal to buy it later.(?)


def dfs(ore_cost, clay_cost, obs_cost, geode_cost):
    stack = []
    initial = OreState(
            minute=0,
            num_ore_robots=1,
            num_clay_robots=0,
            num_obsidian_robots=0,
            num_geode_robots=0,
            num_ore=0,
            num_clay=0,
            num_obsidian=0,
            num_geodes=0
    )
    stack.append(initial)
    best_state = None
    best_geodes = 0
    seen = set()
    with tqdm() as pbar:
        while stack:
            pbar.update(1)
            curr = stack.pop()
            if curr.minute == NUM_MINUTES and curr.num_geodes > best_geodes:
                best_geodes = curr.num_geodes
                best_state = curr
                    
            next_states = get_next(curr, ore_cost, clay_cost, obs_cost, geode_cost)
            for next_ in next_states:
                if next_.upperbound_geodes() >= best_geodes and hash(next_) not in seen:
                    stack.append(next_)
                    seen.add(hash(next_))
    
    return best_state, best_geodes
            

def get_best_from_state(ore_state: OreState, ore_cost, clay_cost, obs_cost, geode_cost, pbar, cache):
    
    if hash(ore_state) in cache:
        return cache[hash(ore_state)]
    
    if ore_state.minute == NUM_MINUTES:
        cache[hash(ore_state)] = ore_state, ore_state.num_geodes
        return ore_state, ore_state.num_geodes
    
    other_actions = get_next(ore_state,  ore_cost, clay_cost, obs_cost, geode_cost)
    best_state = None
    best_geodes = 0
    for action in other_actions:
        best_from_here, num_geodes = get_best_from_state(action, ore_cost, clay_cost, obs_cost, geode_cost, pbar, cache)
        if num_geodes > best_geodes:
            best_state = best_from_here
            best_geodes = num_geodes

    pbar.update(1)
    cache[hash(ore_state)] = best_state, best_geodes
    return best_state, best_geodes

def parse_input(inputs):
    blueprints = []
    parser = compile("Blueprint {}: Each ore robot costs {:d} ore. Each clay robot costs {:d} ore. Each obsidian robot costs {:d} ore and {:d} clay. Each geode robot costs {:d} ore and {:d} obsidian.")
    for item in inputs:
        results = parser.parse(item)
        blueprints.append((results[1], results[2], (results[3], results[4]), (results[5], results[6])))

    return blueprints
if __name__ == "__main__":
    with open("inputs/day19.txt") as f:
        inputs = f.read().splitlines()
    
    blueprints = parse_input(inputs)
    
    # P1 (NUM_MINUTES = 24)
    # total = 0
    # for i, blueprint in enumerate(blueprints):
    #     best_state, num_geodes = dfs(*blueprint)
    #     print(best_state, num_geodes)
    #     total += ((i+1) * num_geodes)
    # print(total)
    
    #P2 (NUM_MINUTES = 32)
    result = 1
    for blueprint in blueprints[:3]:
        best_state, num_geodes = dfs(*blueprint)
        result *= num_geodes
    print(result)
    