import sys
import re
from pprint import pprint

FILE = "input.txt"

def read_and_parse_file(input_file=FILE):
    with open(input_file, encoding="utf-8") as f:
        return [
            [int(c) if c.isdecimal() else -1 for c in list(c)]
            for c in [line.strip() for line in f.readlines()]
        ]

answer = 0
map = read_and_parse_file()
h = len(map)
w = len(map[0])

def in_range(x,y):
    if x < 0 or x >= w or y < 0 or y >= h:
        return False
    return True 

def next_step(target, x, y):
    if not in_range(x,y):
        return []
    
    if map[x][y] == target:
        if target == 9:
            return [(x,y)]
    
        return next_step(target+1, x+1, y) + \
            next_step(target+1, x-1, y) + \
            next_step(target+1, x, y+1) + \
            next_step(target+1, x, y-1)
            
    return []


for x in range(w):
    for y in range(h):
        answer += len(set(next_step(0,x,y)))

print(answer)
