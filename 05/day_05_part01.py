import re
FILE = 'input.txt'
VERBOSE = False

def vprint(*values: object):
    if VERBOSE:
        print(*values)

def read_and_parse_file(input_file = FILE):
    rules_after = {}
    rules_before = {}
    updates = []
    with open(input_file, encoding='utf-8') as f:
        line = f.readline()
        while line != '\n':
            rule = line.strip().split('|')
            if int(rule[0]) in rules_after.keys():
                rules_after[int(rule[0])].append(int(rule[1]))
            else:
                rules_after[int(rule[0])] = [int(rule[1])]
                
            if int(rule[1]) in rules_before.keys():
                rules_before[int(rule[1])].append(int(rule[0]))
            else:
                rules_before[int(rule[1])] = [int(rule[0])]
                
            line = f.readline()
        line = f.readline()
        while line != '':
            updates.append([int(i) for i in line.strip().split(',')])
            line = f.readline()
        
    return rules_after, rules_before, updates
 

rules_after, rules_before, updates = read_and_parse_file()

vprint(f'Rules after: {rules_after}')
vprint(f'Rules before: {rules_before}')
vprint(f'Updates: {updates}')
vprint('----------')

update_num = 0
middle_nums = []
for update in updates:
    update_num += 1
    page_order_okay = True
    vprint(f'CHECKING update #{update_num} : {update}')
    for page_num in range(len(update)):
        page = update[page_num]
        pages_before = update[:page_num]
        pages_after = update[page_num+1:]
        
        order_good = True
        if page in rules_after.keys(): 
            if all(p in rules_after[page] for p in pages_after):
                vprint(f'  -- {page} is good according to after rules')
            else:
                order_good = False
            
        if page in rules_before.keys(): 
            if all(p in rules_before[page] for p in pages_before):
                vprint(f'  -- {page} is good according to before rules')
            else:
                order_good = False
        
        if not order_good:
            page_order_okay = False
            vprint(f'  -- {page} is BAD according to before and after rules')
            
    if page_order_okay:
        middle_nums.append(update[len(update) // 2])
    vprint(f'DONE #{update_num}: is {"VALID" if page_order_okay else "BAD"}')

vprint(middle_nums)
print(sum(middle_nums))