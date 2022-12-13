
def parse_inputs(inputs):
    pairs = []
    for item in inputs:
        left, right = item.split("\n")
        # very bad coding practice but I am lazy, deal with it
        left = eval(left)
        right = eval(right)
        pairs.append((left, right))
    
    return pairs

def check_in_order(left, right):
    """
    Returns 1 if in order, 0 if needs to continue checking, -1 if wrong order
    """
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif left == right:
            return 0
        else:
            return -1 
    
    if isinstance(left, int) and isinstance(right, list):
        return check_in_order([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return check_in_order(left, [right])
        
    # both are list        
    for i in range(len(left)):
        # right runs out of items first
        if i >= len(right):
            return -1

        test = check_in_order(left[i], right[i])
        if test == 1:
            return 1
        if test == -1:
            return -1
    
    # left runs out of items first
    if len(left) < len(right):
        return 1
    else:
        assert len(left) == len(right)
        return 0
        
def part1(inputs):
    pairs = parse_inputs(inputs)
    sum_ = 0
    correct = []
    for i, (left, right) in enumerate(pairs):
        if check_in_order(left, right) == 1:
            sum_ += (i+1)
            correct.append(i+1)
    
    print(correct)
    print(sum_)
            

def sort_pairs(pairs):
    if len(pairs) == 0:
        return []
    if len(pairs) == 1:
        return pairs
    
    anchor = pairs[0]
    left = []
    right = []
    for item in pairs[1:]:
        order = check_in_order(item, anchor)
        if order == 1:
            left.append(item)
        else:
            right.append(item)
    
    return sort_pairs(left) + [anchor] + sort_pairs(right)
            
    
if __name__ == "__main__":
    with open('inputs/day13.txt') as f:
        inputs = f.read().split("\n\n")
    pairs = parse_inputs(inputs)
    all_packets = []
    for left, right in pairs:
        all_packets.append(left)
        all_packets.append(right)
    all_packets.append([[2]])
    all_packets.append([[6]])
    
    sorted_packets = sort_pairs(all_packets)
    index_2 = sorted_packets.index([[2]]) + 1
    index_6 = sorted_packets.index([[6]]) + 1
    print(index_2 * index_6)