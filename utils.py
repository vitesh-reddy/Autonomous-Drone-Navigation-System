import math
from config import GRID_SIZE, ACTIONS

def in_bounds(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE

def euclid(a, b):
    ax, ay = a
    bx, by = b
    return math.hypot(ax - bx, ay - by)

def is_diagonal(action):
    return action in ['up_left', 'up_right', 'down_left', 'down_right']

def next_xy_from_action(x, y, action):
    nx, ny = x, y
    if action == 'up':
        ny += 1
    elif action == 'down':
        ny -= 1
    elif action == 'left':
        nx -= 1
    elif action == 'right':
        nx += 1
    elif action == 'up_left':
        nx -= 1
        ny += 1
    elif action == 'up_right':
        nx += 1
        ny += 1
    elif action == 'down_left':
        nx -= 1
        ny -= 1
    elif action == 'down_right':
        nx += 1
        ny -= 1
    return nx, ny
