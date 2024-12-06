import curses
import random

# Constants for the game board size
BOARD_WIDTH = 25
BOARD_HEIGHT = 25
NUM_X = 10  # Number of random 'X' characters to place on the board

def game_loop(stdscr, start_pos_y, start_pos_x, start_direction_char):
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

    # Place random obstacles ('#' characters) on the board
    for _ in range(NUM_X):
        rand_y = random.randint(0, BOARD_HEIGHT - 1)
        rand_x = random.randint(0, BOARD_WIDTH - 1)
        pad.addch(rand_y, rand_x, '#')

    # Cursor position
    cursor_y, cursor_x = 0, 0

    pad.refresh(0, 0, 0, 0, view_height - 1, view_width - 1)

    # Game loop
    while True:
        # Move the cursor to its current position
        pad.addch(cursor_y, cursor_x, direction)  # Mark cursor
        pad.refresh(0, 0, 0, 0, view_height - 1, view_width - 1)

        # Wait for user input
        key = stdscr.getch()

        new_y, new_x = cursor_y, cursor_x
        if key == curses.KEY_UP and new_y > 0:
            direction = '^'
            new_y -= 1
        elif key == curses.KEY_DOWN and new_y < BOARD_HEIGHT - 1:
            direction = 'v'
            new_y += 1
        elif key == curses.KEY_LEFT and new_x > 0:
            direction = '<'
            new_x -= 1
        elif key == curses.KEY_RIGHT and new_x < BOARD_WIDTH - 1:
            direction = '>'
            new_x += 1
        elif key == ord('q'):  # Quit the game
            return num_dots_eaten

        board_symbol = pad.inch(new_y, new_x)
        
        if board_symbol == ord('.'):
            num_dots_eaten += 1
        
        # Track our path
        pad.addch(cursor_y, cursor_x, 'X')
        
        # Cannot go through obstacles
        if board_symbol != ord('#'):
            cursor_y, cursor_x = new_y, new_x
            
score = curses.wrapper(game_loop)
print(score)

