FILE = 'input.txt'

def read_and_parse_file(input_file = FILE):
    matrix = []
    with open(input_file, encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            matrix.append(list(line.strip()))
            line = f.readline()
        return matrix

def pivot_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    pivoted_matrix = [[0] * rows for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            pivoted_matrix[j][i] = matrix[i][j]

    return pivoted_matrix

def get_all_diagonals(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Create a list to hold all diagonals
    diagonals = []

    # Get diagonals from top-left to bottom-right
    for col in range(cols):
        diagonal = []
        i, j = 0, col
        while i < rows and j < cols:
            diagonal.append(matrix[i][j])
            i += 1
            j += 1
        diagonals.append(diagonal)

    for row in range(1, rows):
        diagonal = []
        i, j = row, 0
        while i < rows and j < cols:
            diagonal.append(matrix[i][j])
            i += 1
            j += 1
        diagonals.append(diagonal)

    # Get diagonals from top-right to bottom-left
    for col in range(cols-1, -1, -1):
        diagonal = []
        i, j = 0, col
        while i < rows and j >= 0:
            diagonal.append(matrix[i][j])
            i += 1
            j -= 1
        diagonals.append(diagonal)

    for row in range(1, rows):
        diagonal = []
        i, j = row, cols-1
        while i < rows and j >= 0:
            diagonal.append(matrix[i][j])
            i += 1
            j -= 1
        diagonals.append(diagonal)

    return diagonals

def find_word(word, line, current_idx):
    for i in range(len(word)):
        if (i + current_idx) >= len(line):
            return False
        if word[i] != line[i+current_idx]:
            return False
    return True

def find_word_backwards(word, line, current_idx):
    for i in range(len(word)):
        if (current_idx - i) < 0 or (current_idx - i) >= len(line):
            return False
        if word[i] != line[current_idx-i]:
            return False
    return True
    
def find_xmas(lines):
    count = 0
    for line in lines:
        for i in range(len(line)):
            if find_word('XMAS', line, i):
                count += 1
        for i in range(len(line), 0, -1):
            if find_word_backwards('XMAS', line, i):
                count += 1
    return count
            
    
matrix = [[1,  2,  3,  4,  5], 
         [6,  7,  8,  9,  10], 
         [11, 12, 13, 14, 15], 
         [16, 17, 18, 19, 20],
         [21, 22, 23, 24, 25], 
         [26, 27, 28, 29, 30]]

matrix = read_and_parse_file()

count_rows = find_xmas(matrix)
print(f"found {count_rows} on the rows")

diags = get_all_diagonals(matrix)
count_diags = find_xmas(diags)
print(f"found {count_diags} on the diag")

pivot = pivot_matrix(matrix)
count_cols = find_xmas(pivot)
print(f"found {count_cols} on the cols")

print(count_cols + count_diags + count_rows)