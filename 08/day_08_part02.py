import sys
from pprint import pprint

def read_and_parse_file(input_file):
    with open(input_file, encoding='utf-8') as f:
        return [list(c) for c in [line.strip() for line in f.readlines()]]
    
def compute_antinode(x,y,h,w,l):
    dist_x = l[0] - x
    dist_y = l[1] - y
    pos = min((x,y), (l[0], l[1]))
    antinodes = [pos]
    while check_bounds(h,w,pos):
        antinodes.append((pos[0] + dist_x, pos[1] + dist_y))
        pos = (pos[0] + dist_x, pos[1] + dist_y)
    return antinodes

def check_bounds(h,w,n):
    if n[0] < 0 or n[1] < 0:
        return False
    if n[0] >= w:
        return False
    if n[1] >= h:
        return False
    return True

def find_antinode_locations(matrix, freqs, test_mode):
    h = len(matrix)
    w = len(matrix[0])

    if test_mode:
        new_matrix =  [x[:] for x in matrix]

    loc = []
    for freq in freqs:
        locations = [(r,matrix[r].index(freq)) for r in range(len(matrix)) if freq in matrix[r]]
        for l in locations:
            an = [n for n in [compute_antinode(x,y,h,w,l) for (x,y) in locations if (x,y) != l] for n in n]
            an = [n for n in an if check_bounds(h, w, n) and n]
            if test_mode:
                for n in an:
                    new_matrix[n[0]][n[1]] = '#'
            loc += an
    if test_mode:
        pprint(new_matrix)
        
    return loc

test_mode = len(sys.argv) <= 1 or sys.argv[1] != 'real'
matrix = read_and_parse_file(f'{"test_" if test_mode else ""}input.txt')
freqs = list(set([freq for row in matrix for freq in row if freq != '.']))
if test_mode: 
    pprint(freqs)
    print('-------')
loc = find_antinode_locations(matrix, freqs, test_mode)
        
print(len(list(set(loc))))
        
