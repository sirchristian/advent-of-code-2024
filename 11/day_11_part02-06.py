FILE = "input.txt"

def read_and_parse_file(input_file=FILE):
    with open(input_file, encoding="utf-8") as f:
        return {int(s): 1 for s in f.readline().split(' ')}

def record_stone(result, num, count):
    if num in result:
        result[num] += count
    else: 
        result[num] = count
        
def num_digits(n):
    x = 1
    while n / 10 >= 1:
        x += 1
        n = n // 10
    return x 
       
def blink(stones):
    result = {}
    for stone in stones:
        if stone == 0:
            record_stone(result, 1, stones[stone])
            continue
        n = num_digits(stone)
        if n % 2 == 0:
            halfway = n // 2
            s = str(stone)
            one, two = int(s[0:halfway]), int(s[halfway:])
            record_stone(result, one, stones[stone])
            record_stone(result, two, stones[stone])
        else:
            record_stone(result, stone * 2024, stones[stone])
    return result

stones = read_and_parse_file()
print(stones)
all_d = stones
for i in range(75):
    stones = blink(stones)
    
    print(f'Blink {i+1}: {stones if i <= 10 else len(stones)}')

print('-----')
print(len(stones))
answer = 0
for s in stones:
    answer = answer + stones[s]
print(answer)