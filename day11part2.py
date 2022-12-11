from __future__ import annotations
from parse import compile
from tqdm import tqdm

def build_operation(op, val):
    if op == "*":
        if val == "old":
            return lambda x: x * x
        else:
            return lambda x: x * int(val)
    if op == "+":
        if val == "old":
            return lambda x: x + x
        else:
            return lambda x: x + int(val)
    raise ValueError

class Item:
    
    def __init__(self, original_value):
        self.original_value = original_value
    
    def load_item(self, test_values):
        self.test_values = test_values
        self.values = [self.original_value % test_val for test_val in self.test_values]

    def apply_operation(self, operation):
        self.values = [operation(val) for val in self.values]
    
    def reset_worry_level(self):
        self.values = [worry % test_val for worry, test_val in zip(self.values, self.test_values)]

class Monkey:
    
    def __init__(self, id: int):
        self.objects = []
        self.id = id
        self.num_inspected = 0

    def load_monkey(self, initial: list, operation: callable, test_value: int, true_throw: Monkey, false_throw: Monkey):
        self.objects = initial
        self.operation = operation
        self.test_value = test_value
        self.true_throw = true_throw
        self.false_throw = false_throw
    
    def test(self, item):
        return item.values[self.id] == 0
    
    def round(self):
        for item in self.objects:
            self.num_inspected += 1
            self.set_worry_level(item)
            if self.test(item):
                self.true_throw.throw(item)
            else:
                self.false_throw.throw(item)
        self.objects = []
    
    def set_worry_level(self, item):
        item.apply_operation(self.operation)
        item.reset_worry_level()
        

    def throw(self, item):
        self.objects.append(item)
        
def build_items(initial):
    return [Item(value) for value in initial]
        
def build_monkeys(monkeys: list[Monkey], inputs):
    
    parse_string = 'Monkey {id}:\n  Starting items: {items}\n  Operation: new = old {op} {val}\n  Test: divisible by {div:d}\n    If true: throw to monkey {true_throw:d}\n    If false: throw to monkey {false_throw:d}'
    parser = compile(parse_string)
    items = []
    test_values = []
    for i, item in enumerate(inputs):
        result = parser.parse(item)
        initial = build_items(list(map(int, result["items"].split(", "))))
        operation = build_operation(result["op"], result["val"])
        # test = build_test(result["div"])
        test_value = result["div"]
        true_throw = monkeys[result["true_throw"]]
        false_throw = monkeys[result["false_throw"]]
        monkeys[i].load_monkey(initial, operation, test_value, true_throw, false_throw)
        items.extend(initial)
        test_values.append(test_value)
    
    for item in items:
        item.load_item(test_values)
         
if __name__ == "__main__":
    with open("inputs/day11.txt") as f:
        inputs = f.read().split("\n\n")
    
    monkeys = [Monkey(i) for i in range(len(inputs))]
    build_monkeys(monkeys, inputs)
    for _ in tqdm(range(10000)):
        for monkey in monkeys:
            monkey.round()
    
    scores = sorted([monkey.num_inspected for monkey in monkeys])
    print(scores)
    print(scores[-2] * scores[-1])
    
