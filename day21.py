from copy import deepcopy
from sympy import symbols, solve


def parse_inputs(inputs):
    result = []
    for item in inputs:
        monkey, operation = item.split(": ")
        result.append((monkey, operation))

    return result

def parse_inputs_p2(inputs):
    result = []
    for item in inputs:
        monkey, operation = item.split(": ")
        if monkey != "humn":
            result.append((monkey, operation))
    
    return result


def get_value(values, lop, rop, op):
    match op:
        case "/":
            return values[lop] / values[rop]
        case "*":
            return values[lop] * values[rop]
        case "-":
            return values[lop] - values[rop]
        case "+":
            return values[lop] + values[rop]
    
def parse_operation(monkey, operation, values):
    operations = operation.split(" ")
    if len(operations) == 1:
        values[monkey] = int(operation)
        return True
    else:
        lop, op, rop = operations
        if lop not in values or rop not in values:
            return False
        values[monkey] = get_value(values, lop, rop, op)
        return True

def parse_operation_p2(monkey, operation, values):
    """
    return 0 if fail
    return 1 if success
    return 2 if monkey is root and fail
    return 3 if monkey is root and success 
    """
    operations = operation.split(" ")
    if len(operations) == 1:
        values[monkey] = int(operation)
        return True
    else:
        lop, op, rop = operations
        if lop not in values or rop not in values:
            return False
        if monkey != "root":
            values[monkey] = get_value(values, lop, rop, op)
            return True
        if monkey == "root":
            print(values[lop])
            print(values[rop])
            return solve(values[lop] - values[rop])
    
    raise ValueError


def part1(inputs):
    monkey_operations = parse_inputs(inputs)
    instructions_queue = deepcopy(monkey_operations)
    values = {}
    while len(instructions_queue) != 0:
        current_unperformed = []
        for monkey, operation in instructions_queue:
            success = parse_operation(monkey, operation, values)
            if not success:
                current_unperformed.append((monkey, operation))
        instructions_queue = current_unperformed
    
    print(values["root"])
    
    
def parse_instructions(instructions_queue, values):
    while len(instructions_queue) != 0:
        current_unperformed = []
        for monkey, operation in instructions_queue:
            success = parse_operation_p2(monkey, operation, values)
            if isinstance(success, bool) and not success:
                current_unperformed.append((monkey, operation))
            elif isinstance(success, list):
                return success
        instructions_queue = current_unperformed
    
if __name__ == "__main__":
    with open("inputs/day21.txt") as f:
        inputs = f.read().splitlines()
    monkey_operations = parse_inputs_p2(inputs)
    instructions_queue = deepcopy(monkey_operations)
    values = {"humn": symbols('x')}
    print(parse_instructions(instructions_queue, values))
    