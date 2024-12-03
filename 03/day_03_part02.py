import re
FILE = 'input.txt'

def read_file(input_file = FILE):
    with open(input_file, encoding='utf-8') as f:
        return f.read()

def mul(a, b):
    return a * b

pattern = re.compile(r'mul\(\d{0,3},\d{0,3}\)')

input = read_file()

local_vals = {}
answer = sum(exec('x = ' + f, {'mul': mul}, local_vals) or local_vals['x'] for f in [f for f in pattern.findall(input)])
print(answer)