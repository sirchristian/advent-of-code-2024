import re
FILE = 'input.txt'

def read_file(input_file = FILE):
    with open(input_file, encoding='utf-8') as f:
        return f.read()

def mul(a, b):
    return a * b

mul_pattern = re.compile(r'mul\(\d{0,3},\d{0,3}\)')

input = read_file()
muls = []
until_dont_pattern = re.compile(r'(?P<muls>.*?)(don\'t\(\))(?P<rest>.*)', re.M | re.S)
until_do_pattern = re.compile(r'.*?(do\(\))(?P<rest>.*)', re.M | re.S)

capture_rest = True
while input:
    search_until_dont = until_dont_pattern.search(input)
    if search_until_dont:
        g = search_until_dont.groupdict()
        if capture_rest:
            muls = muls + [f for f in mul_pattern.findall(g['muls'])]
        input = g['rest']
        capture_rest = False
    else:
        if capture_rest:
            muls = muls + [f for f in mul_pattern.findall(input)]
        break
    
    search_until_do = until_do_pattern.search(input)
    if search_until_do:
        capture_rest = True
        g = search_until_do.groupdict()
        input = g['rest']

local_vals = {}
answer = sum(exec('x = ' + m, {'mul': mul}, local_vals) or local_vals['x'] for m in muls)
print(answer)