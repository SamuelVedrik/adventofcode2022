import numpy as np
# -2, -1, 0, 1, 2, 3, 4, 5
char_map = "=-012345"

def convert_from_SNAFU(item: str):
    decimal_value = 0
    for i, char in enumerate(item[::-1]):
        decimal_value += ((char_map.index(char)-2) * 5**i)
    return decimal_value

def convert_to_SNAFU(item):
    base_5 = np.base_repr(item, base=5)
    snafu = list(base_5)
    i = len(base_5)-1
    while i >= 0:
        match snafu[i]:
            case "0", "1", "2":
                pass
            case "3":
                # adding 1 to the bit on the left
                snafu[i-1] = char_map[char_map.index(snafu[i-1]) + 1]
                snafu[i] = "="
            case "4":
                snafu[i-1] = char_map[char_map.index(snafu[i-1]) + 1]
                snafu[i] = "-"
            case "5":
                snafu[i-1] = char_map[char_map.index(snafu[i-1]) + 1]
                snafu[i] = "0"
        i -= 1
    return "".join(snafu)

if __name__ == "__main__":
    with open("inputs/day25.txt") as f:
        inputs = f.read().splitlines()
    
    total_fuel = sum(convert_from_SNAFU(item) for item in inputs)
    print(convert_to_SNAFU(total_fuel))
    