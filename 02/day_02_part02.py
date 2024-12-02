import re
VERBOSE = False
FILE = 'input.txt'

def read_and_parse_file(input_file = FILE):
    reports= []
    with open(input_file, encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            levels = re.split(r'\W+', line.strip())
            reports.append([int(n) for n in levels])
            line = f.readline()
    return reports

def verbose_print(s):
    if VERBOSE:
        print(s)

def evaluate_report_safety(levels, report_display, tab=''):
    safe = True
    prev_level = levels[0]
    direction = None
    for level in levels[1:]:
        if not safe:
            return False
        
        if direction is None:
            direction = 'increasing' if prev_level < level else 'decreasing' if prev_level > level else None
            if direction is None:
                verbose_print(f"{tab}Report {report_display} is unsafe because direction changed between {prev_level} and {level}")
                safe = False
                
        dist = level - prev_level
        if dist == 0:
            verbose_print(f"{tab}Report {report_display} is unsafe because dist between {prev_level} and {level} is 0")
            safe = False
        elif abs(dist) > 3:
            verbose_print(f"{tab}Report {report_display} is unsafe because dist between {prev_level} and {level} is >3")
            safe = False
        elif direction == 'increasing' and dist < 0:
            verbose_print(f"{tab}Report {report_display} is unsafe because {prev_level} and {level} are decreasing but direction was increasing")
            safe = False
        elif direction == 'decreasing' and dist > 0:
            verbose_print(f"{tab}Report {report_display} is unsafe because {prev_level} and {level} are increasing but direction was decreasing")
            safe = False
        prev_level = level

    verbose_print(f'{tab}Report {report_display} has {len(levels)} levels: {levels}. And is {"safe" if safe else "unsafe"}')
    return safe


def get_number_of_safe_levels(reports):
    length = len(reports)
    num_safe_levels = 0
    for x in range(0, length):
        levels = reports[x]
        verbose_print(f"Checking report #{x+1}...")
        if evaluate_report_safety(levels, f"#{x+1}-{levels}", "\t"):
            num_safe_levels += 1
        else:
            verbose_print(f"\tChecking subset | {levels}")
            num_safe_subset = 0
            for i in range(1, len(levels)+1):
                level_minus_one = levels[:i-1] + levels[i:]
                if evaluate_report_safety(level_minus_one, f"#{x+1}.{i}-{level_minus_one}", "\t\t"):
                    num_safe_subset += 1
            if num_safe_subset >= 1:
                verbose_print(f"\tReport #{x+1} is safe because removing one level makes it safe")
                num_safe_levels += 1
                
    return num_safe_levels

reports = read_and_parse_file()
print(get_number_of_safe_levels(reports))