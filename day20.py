from copy import deepcopy
from tqdm import tqdm


class IntID:
    
    def __init__(self, id, value):
        self.id = id
        self.value = value
    
    def __eq__(self, other):
        return self.id == other.id and self.value == other.value
    
    def __repr__(self):
        return str(self.value)
    
def part1(inputs):
        
    inputs = [IntID(id, num) for id, num in enumerate(inputs)]
    new_list = deepcopy(inputs)
    
    zero_value = [item for item in inputs if item.value == 0][0]
    
    for item in inputs:
        new_index = (new_list.index(item) + item.value) % (len(inputs)-1)
        new_list.pop(new_list.index(item))
        new_list.insert(new_index, item)
    
    index_of_0 = new_list.index(zero_value)
    index_1000 = new_list[(index_of_0 + 1000) % (len(inputs))]
    index_2000 = new_list[(index_of_0 + 2000) % (len(inputs))]
    index_3000 = new_list[(index_of_0 + 3000) % (len(inputs))]
    
    
    print(index_1000.value, index_2000.value, index_3000.value, index_1000.value + index_2000.value + index_3000.value)


if __name__ == "__main__":
    with open("inputs/day20.txt") as f:
        inputs = f.read().splitlines()
        inputs = list(map(int, inputs))
    
    inputs = [IntID(id, num*811589153) for id, num in enumerate(inputs)]
    new_list = deepcopy(inputs)
    
    zero_value = [item for item in inputs if item.value == 0][0]
    
    with tqdm(total=len(inputs) * 10) as pbar:
        for i in range(10):
            for item in inputs:
                new_index = (new_list.index(item) + item.value) % (len(inputs)-1)
                new_list.pop(new_list.index(item))
                new_list.insert(new_index, item)
                pbar.update(1)
        
    index_of_0 = new_list.index(zero_value)
    index_1000 = new_list[(index_of_0 + 1000) % (len(inputs))]
    index_2000 = new_list[(index_of_0 + 2000) % (len(inputs))]
    index_3000 = new_list[(index_of_0 + 3000) % (len(inputs))]
    
    
    print(index_1000.value, index_2000.value, index_3000.value, index_1000.value + index_2000.value + index_3000.value)