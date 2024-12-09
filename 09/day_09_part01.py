import sys
import re
from pprint import pprint

verbose = len(sys.argv) <= 1 or sys.argv[1] != 'real'
def vprint(*values: object, end='\n'):
    if verbose:
        print(*values, end=end)

def disk_layout(file_blocks, free_space):
    layout = []
    for i in range(len(file_blocks)):
        for _ in range(file_blocks[i]):
            layout.append(str(i))
        if len(free_space) > i:
            for _ in range(free_space[i]):
                layout.append('.')
    return layout
                
def read_and_parse_file(input_file):
    with open(input_file, encoding='utf-8') as f:
        s = f.read()
        file_blocks = [int(s[i]) for i in range(len(s)) if not i % 2 and not s[i] == '\n']
        free_space = [int(s[i]) for i in range(len(s)) if i % 2 and not s[i] == '\n']
        return file_blocks, free_space

def find_last_num_at_index(ar, rstart):
    for i in range(rstart, 0, -1):
        if ar[i] != '.':
            return i
    return -1

answer = 0
file_blocks, free_space = read_and_parse_file(f'{"test_" if verbose else ""}input.txt')
a = disk_layout(file_blocks, free_space)
    
ridx = len(a)-1
i = -1
while a.index('.') <= find_last_num_at_index(a, ridx):
    i += 1
    if a[i] == '.':
        pos_r = find_last_num_at_index(a, ridx)
        if (pos_r >= 0):
            t = a[pos_r]
            a[pos_r] = a[i]
            a[i] = t
            ridx = pos_r

for i in range(len(a)-1):
    if a[i] == '.':
        break
    answer += (i * int(a[i]))
         
print(answer)
        
