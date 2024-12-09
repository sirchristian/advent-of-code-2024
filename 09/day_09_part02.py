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

def find_free_space(a, len_file):
    free_space = 0
    for i in range(len(a)-1):
        if a[i] == '.':
            free_space += 1
        elif free_space >= len_file:
            return i-free_space
        else:
            free_space = 0
    return -1

answer = 0
file_blocks, free_space = read_and_parse_file(f'{"test_" if verbose else ""}input.txt')

a = disk_layout(file_blocks, free_space)
c = a[-1]
file = [c]
files_copied = []
print(f"start len = {len(a)}")
vprint("".join(a))
for i in range(len(a)-2, 0, -1):
    if a[i] == c:
        file.append(a[i])
        continue
    else:
        c = a[i]
        if (file[0] != '.'):
            idx = find_free_space(a, len(file))
            if idx > 0 and idx+len(file)-1 <= i and file[0] not in files_copied:
                a[idx:idx+len(file)] = file
                a[i+1:i+1+len(file)] = ['.'] * len(file)
                vprint("".join(a))
                files_copied.append(file[0])
        file = [c]

print(f"end len = {len(a)}")

# Compute Checksum
for i in range(len(a)-1):
    if a[i] == '.':
        continue
    answer += (i * int(a[i]))
         
print(answer)