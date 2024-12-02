import re

input_file = 'input.txt'
reports= []
length = 0
with open(input_file, encoding='utf-8') as f:
    line = f.readline()
    while line != '':
        length = length + 1
        levels = re.split(r'\W+', line.strip())
        reports.append(list(map(lambda n: int(n),levels)))
        line = f.readline()

num_safe_levels = 0
for x in range(0, length):
    levels = reports[x]
    safe = True
    prev_level = levels[0]
    direction = None
    for level in levels[1:]:
        if not safe:
            break
        if direction is None:
            direction = 'increasing' if prev_level < level else 'decreasing' if prev_level > level else None
            if direction is None:
                safe = False
        dist = level - prev_level
        if dist == 0:
            print(f"Report #{x+1} is unsafe because dist between {level} and {prev_level} is 0")
            safe = False
        elif abs(dist) > 3:
            print(f"Report #{x+1} is unsafe because dist between {level} and {prev_level} is >3")
            safe = False
        elif direction == 'increasing' and dist < 0:
            print(f"Report #{x+1} is unsafe because {level} and {prev_level} are decreasing but direction was increasing")
            safe = False
        elif direction == 'decreasing' and dist > 0:
            print(f"Report #{x+1} is unsafe because {level} and {prev_level} are increasing but direction was decreasing")
            safe = False
        prev_level = level

    num_safe_levels = num_safe_levels + 1 if safe else num_safe_levels
    print(f'Report {x+1} has {len(levels)} levels: {levels}. And is {"safe" if safe else "unsafe"}')

print(num_safe_levels)
