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


sim_score = 0
for x in range(0, length):
    local_score = list_01[x] * list_02.count(list_01[x])
    sim_score = sim_score + local_score
    print(f'Sim Score: {list_01[x]} appears {list_02.count(list_01[x])} times in 2nd list for a score of {local_score}')

print(sim_score)
