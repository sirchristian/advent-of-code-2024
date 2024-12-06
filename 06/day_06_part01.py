import curses
import random
import time

FILE = 'input.txt'

def read_and_parse_file(input_file = FILE):
    matrix = []
    with open(input_file, encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            matrix.append(list(line.strip()))
            line = f.readline()
        return matrix

def robot_move(stdscr, direction, did_collide, cursor_y, cursor_x):
    time.sleep(0.1)
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

def generate_board():
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
            if board_char in ('^', 'v', '>', '<'):
                start_pos_y, start_pos_x = y,x
                start_direction_char = board_char
            pad.addch(y, x, board_char)
    return pad, board_height, board_width, start_pos_y, start_pos_x, start_direction_char


def game_loop(stdscr, move_func = get_move):
    num_dots_eaten = 1
    screen_h, screen_w = stdscr.getmaxyx()
    
    pad, board_height, board_width, start_pos_y, start_pos_x, start_direction_char = generate_board()
    direction = start_direction_char

    view_height = min(screen_h, board_height)
    view_width = min(screen_w, board_width)
    
    curses.curs_set(False)

    # Cursor position
    cursor_y, cursor_x = start_pos_y, start_pos_x

    pad.refresh(0, 0, 0, 0, view_height - 1, view_width - 1)

    # Game loop
    did_collide = False
    while True:
        # Move the cursor to its current position
        pad.addch(cursor_y, cursor_x, direction)  # Mark cursor
        pad.refresh(0, 0, 0, 0, view_height - 1, view_width - 1)

        # Get move
        key = move_func(stdscr, direction, did_collide, cursor_y, cursor_x)

        did_collide = False
        
        new_y, new_x = cursor_y, cursor_x
        exit_board = False
        if key == curses.KEY_UP:
            direction = '^'
            new_y -= 1
            if new_y < 0:
                exit_board = True
        elif key == curses.KEY_DOWN:
            direction = 'v'
            new_y += 1
            if new_y >= board_height - 1:
                exit_board = True
        elif key == curses.KEY_LEFT:
            direction = '<'
            new_x -= 1
            if new_x < 0:
                exit_board = True
        elif key == curses.KEY_RIGHT:
            direction = '>'
            new_x += 1
            if new_x >= board_width - 1:
                exit_board = True
        
        if key == ord('q') or exit_board:  # Quit the game
            return num_dots_eaten

        board_symbol = pad.inch(new_y, new_x)
        
        if board_symbol == ord('.'):
            num_dots_eaten += 1
        
        # Track our path
        pad.addch(cursor_y, cursor_x, 'X')
        
        # Cannot go through obstacles
        if board_symbol != ord('#'):
            cursor_y, cursor_x = new_y, new_x
        else:
            did_collide = True
            
score = curses.wrapper(game_loop, robot_move)
print(score)