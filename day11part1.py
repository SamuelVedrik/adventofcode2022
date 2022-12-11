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

def build_test(divisible):
    return lambda x: (x % divisible == 0)

class Monkey:
    
    def __init__(self, id: int):
        self.objects = []
        self.id = id
        self.num_inspected = 0

    def load_monkey(self, initial: list, operation: callable, test: callable, true_throw: Monkey, false_throw: Monkey):
        self.objects = initial
        self.operation = operation
        self.test = test
        self.true_throw = true_throw
        self.false_throw = false_throw
    
    def round(self):
        for item in self.objects:
            self.num_inspected += 1
            worry_level = self.worry_level(item)
            if self.test(worry_level):
                self.true_throw.throw(worry_level)
            else:
                self.false_throw.throw(worry_level)
        self.objects = []
    
    def worry_level(self, item):
        return self.operation(item)

    def throw(self, item):
        self.objects.append(item)
        
def build_monkeys(monkeys: list[Monkey], inputs):
    
    parse_string = 'Monkey {id}:\n  Starting items: {items}\n  Operation: new = old {op} {val}\n  Test: divisible by {div:d}\n    If true: throw to monkey {true_throw:d}\n    If false: throw to monkey {false_throw:d}'
    parser = compile(parse_string)
    for i, item in enumerate(inputs):
        result = parser.parse(item)
        initial = list(map(int, result["items"].split(", ")))
        operation = build_operation(result["op"], result["val"])
        test = build_test(result["div"])
        true_throw = monkeys[result["true_throw"]]
        false_throw = monkeys[result["false_throw"]]
        monkeys[i].load_monkey(initial, operation, test, true_throw, false_throw)
        
         
if __name__ == "__main__":
    with open("inputs/day11.txt") as f:
        inputs = f.read().split("\n\n")
    
    monkeys = [Monkey(i) for i in range(len(inputs))]
    build_monkeys(monkeys, inputs)
    for _ in tqdm(range(5)):
        for monkey in monkeys:
            monkey.round()
    
    scores = sorted([monkey.num_inspected for monkey in monkeys])
    print(scores)
    # print(scores[-2] * scores[-1])
    
