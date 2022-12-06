
if __name__ == "__main__":
    with open("inputs/day6.txt") as f:
        inputs = f.read().strip()
    num_unique = 14
    for i in range(len(inputs)):
        if len(set(inputs[i:i+14])) == num_unique:
            print(i + num_unique)
            break