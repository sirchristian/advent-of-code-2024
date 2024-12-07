import operator
from itertools import product, combinations_with_replacement, permutations


FILE = "input.txt"


def read_and_parse_file(input_file=FILE):
    with open(input_file, encoding="utf-8") as f:
        return [
            (int(parts[0]), [int(n) for n in parts[1].strip().split(" ")])
            for parts in [entry.split(":") for entry in [line for line in f.readlines()]]
        ]

def get_op_combinations(ops, len):
    return list(set([x for x in permutations(ops, len)] + 
                    [x for x in combinations_with_replacement(ops, len)] + 
                    [x for x in product(ops,repeat=len)]))

execute = {
    "*": operator.mul, 
    "+": operator.add, 
    "||": operator.concat
}
    
calibrations = read_and_parse_file()
answer = 0
ops = ["*", "+", "||"]
x = 0

def do_calc(result, op, n):
    if op == "||":
        return int(str(result) + str(n))
    return execute[op](result, n)

for calibration in calibrations:
    target = calibration[0]
    for p in get_op_combinations(ops, len(calibration[1]) - 1): 
        result = calibration[1][0]
        for i in range(len(calibration[1]) - 1):
            op = p[i]
            n = calibration[1][i+1]
            result = do_calc(result, op, n)
        if (result == target):
            answer += result
            break

print(answer)
            