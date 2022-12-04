
def check_full_overlap(left_range, right_range):
    ll, lr = list(map(int, left_range.split("-")))
    rl, rr = list(map(int, right_range.split("-")))
    return ll <= rl and lr >= rr
    
def check_not_overlap(left_range, right_range):
    ll, lr = list(map(int, left_range.split("-")))
    rl, rr = list(map(int, right_range.split("-")))
    return (lr < rl and ll < rr)

def part1(inputs):
    num_complete_overlap = 0
    for item in inputs:
        left, right = item.split(",")
        if check_full_overlap(left, right) or check_full_overlap(right, left):
            num_complete_overlap += 1
            
    return num_complete_overlap

def part2(inputs):
    num_overlap = 0
    for item in inputs:
        left, right = item.split(",")
        if not(check_not_overlap(left, right) or check_not_overlap(right, left)):
            num_overlap += 1

    return num_overlap

if __name__ == "__main__":
    
    with open("inputs/day4.txt") as f:
        inputs = f.read().splitlines()
    
    print(part1(inputs))
    print(part2(inputs))
        