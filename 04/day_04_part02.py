FILE = 'input.txt'

def read_and_parse_file(input_file = FILE):
    matrix = []
    with open(input_file, encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            matrix.append(list(line.strip()))
            line = f.readline()
        return matrix

matrix = read_and_parse_file()

rows = len(matrix)
cols = len(matrix[0])

def checkAround(x, y, rows, cols, matrix):
    ulx, uly = x-1, y-1
    umx, umy = x-1, y
    urx, ury = x-1, y+1
    lx, ly = x, y-1
    rx, ry = x, y+1
    llx, lly = x+1, y-1
    lmx, lmy = x+1, y
    lrx, lry = x+1, y+1
    allx = [ulx, umx, urx, lx, rx, llx, lmx, lrx]
    ally = [uly, umy, ury, ly, ry, lly, lmy, lry]
    
    if any(xc < 0 for xc in allx):
        return False
    if any(yc < 0 for yc in ally):
        return False
    if any(xc >= rows for xc in allx):
        return False
    if any(yc >= cols for yc in ally):
        return False
    
    if matrix[ulx][uly] == 'M' and matrix[lrx][lry] == 'S' and matrix[urx][ury] == 'M' and matrix[llx][lly] == 'S': 
        return True
    if matrix[ulx][uly] == 'M' and matrix[lrx][lry] == 'S' and matrix[urx][ury] == 'S' and matrix[llx][lly] == 'M': 
        return True

    if matrix[ulx][uly] == 'S' and matrix[lrx][lry] == 'M' and matrix[urx][ury] == 'M' and matrix[llx][lly] == 'S': 
        return True
    if matrix[ulx][uly] == 'S' and matrix[lrx][lry] == 'M' and matrix[urx][ury] == 'S' and matrix[llx][lly] == 'M': 
        return True

    return False
    
numXmas = 0
for i in range(rows):
    for j in range(cols):
        # cannot cross on the edge
        if i == 0 or j == 0 or i >= rows or j >= cols:
            continue
        if matrix[i][j] == 'A' and checkAround(i, j, rows, cols, matrix):
            numXmas += 1
            
print(numXmas)