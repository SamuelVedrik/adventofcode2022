
class Node:
    
    def __init__(self, name, parent=None, size=None):
        self.children = []
        self.size = size
        if parent is None:
            self.parent = self
        else:
            self.parent = parent
        self.name = name
    
    def calculate_size(self):
        if self.size is not None:
            return self.size
        else:
            self.size = sum(child.calculate_size() for child in self.children)
            return self.size
    
    def get_child(self, child_name):
        for child in self.children:
            if child.name == child_name:
                return child
        
        raise ValueError("Cannot find child!")
    
    def __repr__(self):
        return f"File name: {self.name}"
    
    def __hash__(self):
        return hash(self.name)


def parse_inputs(inputs):
    root_node = Node(name="/")
    curr_pointer = root_node
    i = 0
    while i < len(inputs):
        commands = inputs[i].split(" ")
        if commands[0] == "$" and commands[1] == "cd":
            if commands[2] == "/":
                curr_pointer = root_node
            elif commands[2] == "..":
                curr_pointer = curr_pointer.parent
            else:
                curr_pointer = curr_pointer.get_child(commands[2])
            i += 1
        if commands[0] == "$" and commands[1] == "ls":
            children = []
            i += 1
            while inputs[i][0] != "$":
                size, file_name = inputs[i].split(" ")
                if size.isnumeric():
                    children.append(Node(name = file_name, size=int(size), parent=curr_pointer))
                else:
                    children.append(Node(name=file_name, parent=curr_pointer))
                i += 1
                if i == len(inputs):
                    break
            curr_pointer.children = children
            
    return root_node

def part1(inputs):
    root = parse_inputs(inputs)
    
    total_num = 0
    to_visit = [root]
    while len(to_visit) != 0:
        curr = to_visit.pop()
        size = curr.calculate_size()
        if size <= 100000 and len(curr.children) != 0:
            total_num += size
        to_visit.extend(curr.children)
    
    print(total_num)
    
def part2(inputs):
    
    root = parse_inputs(inputs)
    limit = 30000000 - (70000000 - root.calculate_size())
    big_enough = []
    to_visit = [root]
    while len(to_visit) != 0:
        curr = to_visit.pop()
        size = curr.calculate_size()
        if size >= limit and len(curr.children) != 0:
            big_enough.append((size))
        to_visit.extend(curr.children)
    
    print(min(big_enough))
    

if __name__ == "__main__":
    with open("inputs/day7.txt") as f:
        inputs = f.read().splitlines()
    
    part1(inputs)
    part2(inputs)
        

        
    