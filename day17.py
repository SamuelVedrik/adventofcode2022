import numpy as np
from tqdm import tqdm

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def can_push_left(self, same_level_rocks: list["Rock"]):
        will_hit_wall = self.x == 0
        will_hit_other = any(rock.x == self.x - 1 for rock in same_level_rocks)
        return not (will_hit_wall or will_hit_other)

    def can_push_right(self, same_level_rocks: list["Rock"]):
        will_hit_wall = self.x == 6
        will_hit_other = any(rock.x == self.x + 1 for rock in same_level_rocks)
        return not (will_hit_wall or will_hit_other)

    def can_drop(self, below_level_rocks: list["Rock"]):
        will_hit_floor = self.y == 0
        will_hit_other = any(rock.x == self.x for rock in below_level_rocks)
        return not (will_hit_floor or will_hit_other)

    def push_left(self):
        self.x -= 1

    def push_right(self):
        self.x += 1

    def drop(self):
        self.y -= 1

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class FrozenRock:

    def __init__(self):
        self.rocks_floor = []

    def get_rock_at_level(self, y: int):
        return [rock for rock in self.rocks_floor if rock.y == y]

    def add_rocks(self, rocks: list[Rock]):
        self.rocks_floor.extend(rocks)
        # only store rocks that make up the floor
        floor_level = min(max([rock.y for rock in self.rocks_floor if rock.x == x], default=0) for x in range(7))
        new_rocks = [rock for rock in self.rocks_floor if rock.y >= floor_level]
        self.rocks_floor = new_rocks

    def get_highest_rock(self):
        if len(self.rocks_floor) == 0:
            return -1
        return max(rock.y for rock in self.rocks_floor)
    
    def get_normalized(self, rocks: list[Rock]):
        lowest_floor = min(rock.y for rock in rocks)
        normalized = [Rock(rock.x, rock.y-lowest_floor) for rock in rocks]
        return normalized
    
    def get_state(self):
        return frozenset(self.get_normalized(self.rocks_floor))
    
    def print_rock_state(self):
        normalized = self.get_normalized(self.rocks_floor)
        max_shape = max(rock.y for rock in normalized) + 1
        shape = np.full(shape=(max_shape, 7), fill_value="⬜️")
        for rock in normalized:
            shape[max_shape-rock.y-1, rock.x] = "⬛️"
        state ="\n".join(["".join(row) for row in shape])
        print(state)



class RockFormation:
    def __init__(self, rocks: list[Rock]):
        self.rocks = rocks

    def push_left(self, frozen_rock: FrozenRock):
        can_push_left = True
        for rock in self.rocks:
            if not rock.can_push_left(frozen_rock.get_rock_at_level(rock.y)):
                can_push_left = False
                break

        if can_push_left:
            for rock in self.rocks:
                rock.push_left()
        return can_push_left

    def push_right(self, frozen_rock: FrozenRock):
        can_push_right = True
        for rock in self.rocks:
            if not rock.can_push_right(frozen_rock.get_rock_at_level(rock.y)):
                can_push_right = False
                break

        if can_push_right:
            for rock in self.rocks:
                rock.push_right()
        return can_push_right

    def drop(self, frozen_rock: FrozenRock):
        can_drop = True
        for rock in self.rocks:
            if not rock.can_drop(frozen_rock.get_rock_at_level(rock.y - 1)):
                can_drop = False
                break

        if can_drop:
            for rock in self.rocks:
                rock.drop()
        return can_drop
    
    def __repr__(self):
        return "|".join(str(rock) for rock in self.rocks)


def spawn_dash(top_rock: int):
    y_level = top_rock + 4
    return RockFormation(
        [
            Rock(2, y_level),
            Rock(3, y_level),
            Rock(4, y_level),
            Rock(5, y_level),
        ]
    )


def spawn_plus(top_rock):
    y_level = top_rock + 4
    return RockFormation(
        [
            Rock(3, y_level),
            Rock(2, y_level + 1),
            Rock(3, y_level + 1),
            Rock(4, y_level + 1),
            Rock(3, y_level + 2),
        ]
    )


def spawn_backwards_L(top_rock):
    y_level = top_rock + 4
    return RockFormation([
        Rock(2, y_level),
        Rock(3, y_level),
        Rock(4, y_level),
        Rock(4, y_level+1),
        Rock(4, y_level+2),
        ]
        )

def spawn_vert_line(top_rock):
    y_level = top_rock + 4
    return RockFormation(
        [
            Rock(2, y_level),
            Rock(2, y_level+1),
            Rock(2, y_level+2),
            Rock(2, y_level+3)
        ]
    )

def spawn_square(top_rock):
    y_level = top_rock + 4
    return RockFormation(
        [
            Rock(2, y_level),
            Rock(3, y_level),
            Rock(2, y_level+1),
            Rock(3, y_level+1)
        ]
    )

def simulate(curr_num_rocks, curr_spawn_idx, curr_instruction_idx, frozen_rock, instructions):
    spawn_order = [spawn_dash, spawn_plus, spawn_backwards_L, spawn_vert_line, spawn_square]

    spawn_f = spawn_order[curr_spawn_idx]
    rock_form = spawn_f(frozen_rock.get_highest_rock())
    stopped = False
    while not stopped:
        instruction = instructions[curr_instruction_idx]
        if instruction == "<":
            rock_form.push_left(frozen_rock)
        elif instruction == ">":
            rock_form.push_right(frozen_rock)
        curr_instruction_idx += 1
        curr_instruction_idx = curr_instruction_idx % len(instructions)
        stopped = not rock_form.drop(frozen_rock)
    frozen_rock.add_rocks(rock_form.rocks)
    curr_num_rocks += 1
    curr_spawn_idx = curr_num_rocks % len(spawn_order)

    return curr_num_rocks, curr_spawn_idx, curr_instruction_idx 


if __name__ == "__main__":

    with open("./inputs/day17.txt") as f:
        instructions = f.read()
    
    # TO_SPAWN = 2022
    TO_SPAWN = 1000000000000
    seen_states = {}
    curr_num_rocks = 0
    curr_spawn_idx = 0
    curr_instruction_idx = 0
    cycle_found = False
    frozen_rock = FrozenRock()
    delta = 0
    with tqdm() as pbar:
        while curr_num_rocks < TO_SPAWN:
            curr_num_rocks, curr_spawn_idx, curr_instruction_idx = simulate(curr_num_rocks, curr_spawn_idx, curr_instruction_idx, frozen_rock, instructions)
            if cycle_found:
                continue

            curr_state = frozen_rock.get_state(), curr_spawn_idx, curr_instruction_idx
            if curr_state not in seen_states.keys():
                seen_states[curr_state] = curr_num_rocks, frozen_rock.get_highest_rock()
            else:
                # jump forward
                prev_seen, prev_top = seen_states[curr_state]
                cycle_length = curr_num_rocks - prev_seen
                jumps, to_simulate = divmod(TO_SPAWN-curr_num_rocks, cycle_length)
                delta = (frozen_rock.get_highest_rock() - prev_top) * jumps
                curr_num_rocks = TO_SPAWN - to_simulate
                cycle_found = True
            pbar.update(1)
    
    print(curr_num_rocks)
    print(seen_states[curr_state])        
    print(frozen_rock.get_highest_rock() + 1 + delta)



