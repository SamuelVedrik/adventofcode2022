loses = [("A", "Z"), ("B", "X"), ("C", "Y")]
wins = [("A", "Y"), ("B", "Z"), ("C", "X")]
draws = [("A", "X"), ("B", "Y"), ("C",  "Z")]
point_map = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

loses_map = {"A": "Z", "B": "X", "C": "Y"}
wins_map = {"A": "Y", "B": "Z", "C": "X"}
draws_map = {"A": "X", "B": "Y", "C": "Z"}

point_result_map = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}

def num_points(pairs):
    left, right = pairs
    if pairs in loses:
        win_points = 0
    elif pairs in draws:
        win_points = 3
    elif pairs in wins:
        win_points = 6
    else:
        raise ValueError
    return point_map[right] + win_points

def num_points_part2(pairs):
    left, right = pairs
    if right == "X":
        chosen = loses_map[left]
    elif right == "Y":
        chosen = draws_map[left]
    elif right == "Z": 
        chosen = wins_map[left]
    else:
        raise ValueError

    return point_result_map[right] + point_map[chosen]
    

if __name__ == "__main__":
    
    with open("inputs/day2.txt") as f:
        inputs = f.read().splitlines()
    
    inputs = [tuple(item.split(" ")) for item in inputs]
    
    print(sum(num_points(item) for item in inputs))
    print(sum(num_points_part2(item) for item in inputs))
    
    