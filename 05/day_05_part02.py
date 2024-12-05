from functools import cmp_to_key
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


def check_page_rules(rules_after, rules_before, update):
    page_order_okay = True
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
            
    return page_order_okay

def find_first_match_index(list1, list2):
    for index, item in enumerate(list1):
        if item in list2:
            return index
    return -1


def page_cmp(page1, page2):
    if page1 in rules_after.keys() and page2 in rules_after[page1]:
        return -1
    if page1 in rules_before.keys() and page2 in rules_before[page1]:
        return 1
    return 0
    

update_num = 0
updated_updates = []

for update in updates:
    update_num += 1
    
    updated_update = []
    vprint(f'CHECKING update #{update_num} : {update}')
    
    page_order_okay = check_page_rules(rules_after, rules_before, update)
    
    if not page_order_okay:
        vprint(f' :: #{update_num}: needs adjustment')
        updated_update = sorted(update, key=cmp_to_key(page_cmp))
        updated_updates.append(updated_update)
        vprint(f' : UPDATED PAGES - {updated_update} - testing...{check_page_rules(rules_after, rules_before, updated_update)}')        
    
    vprint(f'DONE #{update_num}: is {"VALID" if page_order_okay else "BAD"}')

answer = 0
for updated_update in updated_updates:
    answer += updated_update[len(updated_update) // 2]

print(answer)