FILE = "input.txt"

def read_and_parse_file(input_file=FILE):
    with open(input_file, encoding="utf-8") as f:
        return [s for s in f.readline().split(' ')]

def blink(stones):
    result = []
    for stone in stones:
        if stone == '0':
            result.append('1')
        elif len(stone) % 2 == 0:
            halfway = len(stone) // 2
            result.append(str(int(stone[0:halfway])))
            result.append(str(int(stone[halfway:])))
        else:
            result.append(str(int(stone) * 2024))
    return result

stones = read_and_parse_file()
for i in range(25):
    stones = blink(stones)
    
    print(f'Blink {i+1}: {stones if i <= 10 else len(stones)}')

print('-----')
print(len(stones))