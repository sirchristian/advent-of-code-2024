import re

input_file = 'input.txt'
list_01 = []
list_02 = []
length = 0
with open(input_file, encoding='utf-8') as f:
    line = f.readline()
    while line != '':
        length = length + 1
        split = re.split(r'\W+', line)
        list_01.append(int(split[0]))
        list_02.append(int(split[1]))
        line = f.readline()

list_01.sort()
list_02.sort()

distance = 0
for x in range(0, length):
    local_dist = abs(list_01[x] - list_02[x])
    distance = distance + local_dist
    print(f'Distance between {list_01[x]} and {list_02[x]} is {local_dist}')

print(distance)
