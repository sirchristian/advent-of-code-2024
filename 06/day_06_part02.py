import curses
import random
import time

FILE = 'input.txt'
path = []

def read_and_parse_file(input_file = FILE):
    matrix = []
    with open(input_file, encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            matrix.append(list(line.strip()))
            line = f.readline()
        return matrix

def robot_move(stdscr, direction, did_collide, cursor_y, cursor_x):
    #time.sleep(0.001)
    if direction == '^':
        return curses.KEY_RIGHT if did_collide else curses.KEY_UP
    if direction == '>':
        return curses.KEY_DOWN if did_collide else curses.KEY_RIGHT
    if direction == 'v':
        return curses.KEY_LEFT if did_collide else curses.KEY_DOWN
    if direction == '<':
        return curses.KEY_UP if did_collide else curses.KEY_LEFT

# default move function
def get_move(stdscr, direction, did_collide, cursor_y, cursor_x):
    return stdscr.getch()

def generate_board(o_y = None, o_x = None):
    board = read_and_parse_file()
    board_height = len(board) + 1
    board_width = len(board[0]) + 1
    start_pos_y = 0
    start_pos_x = 0
    start_direction_char = '^'
    pad = curses.newpad(board_height, board_width)

    for y in range(board_height - 1):
        for x in range(board_width - 1):            
            board_char = board[y][x]
            if o_y is not None and o_y == y and o_x is not None and o_x == x and board_char in ('.'):
                board_char = 'O'
            if board_char in ('^', 'v', '>', '<'):
                start_pos_y, start_pos_x = y,x
                start_direction_char = board_char
            pad.addch(y, x, board_char)
    return pad, board_height, board_width, start_pos_y, start_pos_x, start_direction_char

def find_last(lst, value):
    for i, v in enumerate(reversed(lst)):
        if v == value:
            return len(lst) - 1 - i
    return -1

def did_path_repeat(cur, path):
    if path.count(cur) < 3:
        return False
    
    first = path.index(cur)
    next = path.index(cur, first+1)
    last = find_last(path, cur)
    second_last = find_last(path[0:last-1], cur)
    if (path[first:next] == path[second_last:last] and 
    first != second_last):
        return True
    return False

def game_loop(stdscr, o_x, o_y, move_func = get_move):
    screen_h, screen_w = stdscr.getmaxyx()
    
    pad, board_height, board_width, start_pos_y, start_pos_x, start_direction_char = generate_board(o_x, o_y)
    direction = start_direction_char

    view_height = min(screen_h, board_height)
    view_width = min(screen_w, board_width)
    
    curses.curs_set(False)

    # Cursor position
    cursor_y, cursor_x = start_pos_y, start_pos_x
    path.append((cursor_y, cursor_x))

    #pad.refresh(0, 0, 0, 0, view_height - 1, view_width - 1)

    # Game loop
    did_collide = False
    did_repeat = False
    new_direction = None

    while True:
        # Move the cursor to its current position
        pad.addch(cursor_y, cursor_x, direction)  # Mark cursor
        #pad.refresh(0, 0, 0, 0, view_height - 1, view_width - 1)

        # Get move
        key = move_func(stdscr, direction, did_collide, cursor_y, cursor_x)

        did_collide = False
        
        new_y, new_x = cursor_y, cursor_x
        exit_board = False
        if key == curses.KEY_UP:
            new_direction = '^'
            new_y -= 1
            if new_y < 0:
                exit_board = True
        elif key == curses.KEY_DOWN:
            new_direction = 'v'
            new_y += 1
            if new_y >= board_height - 1:
                exit_board = True
        elif key == curses.KEY_LEFT:
            new_direction = '<'
            new_x -= 1
            if new_x < 0:
                exit_board = True
        elif key == curses.KEY_RIGHT:
            new_direction = '>'
            new_x += 1
            if new_x >= board_width - 1:
                exit_board = True
        
        if key == ord('q') or exit_board or did_repeat:  # Quit the game
            return did_repeat

        board_symbol = pad.inch(new_y, new_x)
        
        if (new_direction in ('>', '<') and direction in ('<', '>')):
            pad.addch(cursor_y, cursor_x, '-')
        elif (new_direction in ('v', '^') and direction in ('^', 'v')):
            pad.addch(cursor_y, cursor_x, '|')
        elif ((new_direction in ('v', '^') and direction in ('<', '>')) or 
              (new_direction in ('>', '<') and direction in ('^', 'v'))):
            pad.addch(cursor_y, cursor_x, '+')
            
        direction = new_direction
        
        # Cannot go through obstacles
        if board_symbol != ord('#') and board_symbol != ord('O'):
            cursor_y, cursor_x = new_y, new_x
            cur = (cursor_y, cursor_x)
            path.append(cur)
            did_repeat = did_path_repeat(cur, path)
        else:
            did_collide = True
            
# Mmmm, wasted IO....
board = read_and_parse_file()
board_height = len(board) + 1
board_width = len(board[0]) + 1
num = 0
for y in range(board_height - 1):
    for x in range(board_width - 1):  
        path = []
        if curses.wrapper(game_loop, y, x, robot_move):
            num += 1
print(num)

