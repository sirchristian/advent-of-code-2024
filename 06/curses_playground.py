import curses
import random
import time

# Constants for the game board size
BOARD_WIDTH = 25
BOARD_HEIGHT = 25

def robot_move(stdscr, direction, did_collide, cursor_y, cursor_x):
    time.sleep(0.1)
    if direction == '^':
        return curses.KEY_RIGHT if did_collide else curses.KEY_UP
    if direction == '>':
        return curses.KEY_DOWN if did_collide else curses.KEY_RIGHT
    if direction == 'v':
        return curses.KEY_LEFT if did_collide else curses.KEY_DOWN
    if direction == '<':
        return curses.KEY_UP if did_collide else curses.KEY_RIGHT

# default move function
def get_move(stdscr, direction, did_collide, cursor_y, cursor_x):
    return stdscr.getch()

def generate_board(pad):
    # Place random obstacles ('#' characters) on the board
    NUM_OBSTACLES = 45
    for _ in range(NUM_OBSTACLES):
        rand_y = random.randint(0, BOARD_HEIGHT - 1)
        rand_x = random.randint(0, BOARD_WIDTH - 1)
        pad.addch(rand_y, rand_x, '#')

def game_loop(stdscr, start_pos_y, start_pos_x, start_direction_char, move_func = get_move):
    num_dots_eaten = 0
    direction = start_direction_char
    screen_h, screen_w = stdscr.getmaxyx()
    view_height = min(screen_h, BOARD_HEIGHT)
    view_width = min(screen_w, BOARD_WIDTH)
    pad = curses.newpad(BOARD_HEIGHT, BOARD_WIDTH)
    curses.curs_set(False)

    # Fill the board
    for y in range(BOARD_HEIGHT - 1):
        for x in range(BOARD_WIDTH - 1):
            pad.addch(y, x, '.')

    generate_board(pad)

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
            if new_y <= 0:
                exit_board = True
            direction = '^'
            new_y -= 1
        elif key == curses.KEY_DOWN:
            if new_y >= BOARD_HEIGHT - 1:
                exit_board = True
            direction = 'v'
            new_y += 1
        elif key == curses.KEY_LEFT:
            if new_x <= 0:
                exit_board = True
            direction = '<'
            new_x -= 1
        elif key == curses.KEY_RIGHT:
            if new_x >= BOARD_WIDTH - 1:
                exit_board = True
            direction = '>'
            new_x += 1
        
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
            
score = curses.wrapper(game_loop, 9, 11, '^', robot_move)
print(score)

