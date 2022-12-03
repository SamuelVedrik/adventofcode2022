priority = [item for item in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"]

if __name__ == "__main__":
    with open("inputs/day3.txt") as f:
        inputs = f.read().splitlines()
    prio_sum = 0
    for item in inputs:
        left, right = item[:len(item)//2], item[len(item)//2:]
        overlap = set(left).intersection(right).pop()
        prio_sum += priority.index(overlap) + 1
    
    print(prio_sum)
    prio_sum = 0
    for i in range(len(inputs)//3):
        a = inputs[i*3]
        b = inputs[(i*3)+1]
        c = inputs[(i*3)+2]
        overlap = set(a).intersection(set(b)).intersection(set(c)).pop()
        prio_sum += priority.index(overlap) + 1
    
    print(prio_sum)