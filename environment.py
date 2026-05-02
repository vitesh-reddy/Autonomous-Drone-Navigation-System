import numpy as np
import random
import math
from config import (
    GRID_SIZE, NUM_BIRDS, MOVE_PROB, BIRD_RANDOM_DRIFT_PROB, 
    BIRD_VEL_CHOICES, RSEED, PICKUPS, DROPS, STEP_COST, DIAG_COST, 
    WALL_PEN, PICKUP_REW, DROP_REW, MAX_STEPS, DANGER_RADIUS_CELLS, REFLEX_ENABLED
)
from utils import in_bounds, euclid, is_diagonal, next_xy_from_action


def bird_reset():
    """Initialize bird positions, velocities, and types."""
    if RSEED is not None:
        np.random.seed(RSEED + random.randint(0, 1000000))
    
    birds = [
        (np.random.randint(0, GRID_SIZE), np.random.randint(0, GRID_SIZE))
        for _ in range(NUM_BIRDS)
    ]
    dirs = [
        (np.random.choice(BIRD_VEL_CHOICES), np.random.choice(BIRD_VEL_CHOICES))
        for _ in range(NUM_BIRDS)
    ]
    types = [random.choice([0, 1]) for _ in range(NUM_BIRDS)]
    
    return birds, dirs, types


def move_birds(birds, dirs):
    """Update bird positions with movement logic and bouncing."""
    new_birds, new_dirs = [], []
    
    for (x, y), (dx, dy) in zip(birds, dirs):
        if np.random.random() < MOVE_PROB:
            if np.random.random() < BIRD_RANDOM_DRIFT_PROB:
                dx = np.random.choice(BIRD_VEL_CHOICES)
                dy = np.random.choice(BIRD_VEL_CHOICES)
            
            nx, ny = x + dx, y + dy
            
            # Bounce off grid boundaries
            if nx < 0 or nx >= GRID_SIZE:
                dx *= -1
                nx = max(0, min(nx, GRID_SIZE - 1))
            if ny < 0 or ny >= GRID_SIZE:
                dy *= -1
                ny = max(0, min(ny, GRID_SIZE - 1))
            
            x, y = nx, ny
        
        new_birds.append((x, y))
        new_dirs.append((dx, dy))
    
    return new_birds, new_dirs


def step_with_reflex(state, planned_action, birds, dirs):
    """
    Execute one environment step with reflex shielding.
    
    Args:
        state: (x, y, has_package)
        planned_action: Action chosen by the agent
        birds: Current bird positions
        dirs: Current bird velocities
    
    Returns:
        next_state, reward, done, next_birds, next_dirs, reflex_used, executed_action
    """
    x, y, has_pkg = state
    reward = STEP_COST
    done = False
    reflex_used = False
    executed_action = planned_action

    # Reflex shielding: override unsafe movement actions
    if planned_action not in ['pickup', 'drop'] and REFLEX_ENABLED:
        intended = next_xy_from_action(x, y, planned_action)
        intended = intended if in_bounds(*intended) else (x, y)
        too_close = any(euclid(intended, b) <= DANGER_RADIUS_CELLS for b in birds)
        
        if too_close:
            candidates = ['up', 'down', 'left', 'right', 'up_left', 'up_right', 'down_left', 'down_right']
            best_a, best_score = planned_action, -1e18
            
            for a in candidates:
                nx, ny = next_xy_from_action(x, y, a)
                if not in_bounds(nx, ny):
                    continue
                
                min_dist = min(euclid((nx, ny), b) for b in birds) if birds else 999.0
                penalty = 0.05 if is_diagonal(a) else 0.0
                score = min_dist - penalty
                
                if score > best_score:
                    best_score, best_a = score, a
            
            executed_action = best_a
            reflex_used = (executed_action != planned_action)

    nx, ny = x, y

    # Execute action
    if executed_action == 'up':
        ny += 1
    elif executed_action == 'down':
        ny -= 1
    elif executed_action == 'left':
        nx -= 1
    elif executed_action == 'right':
        nx += 1
    elif executed_action == 'up_left':
        nx -= 1
        ny += 1
    elif executed_action == 'up_right':
        nx += 1
        ny += 1
    elif executed_action == 'down_left':
        nx -= 1
        ny -= 1
    elif executed_action == 'down_right':
        nx += 1
        ny -= 1
    elif executed_action == 'pickup':
        if (x, y) in PICKUPS and has_pkg == 0:
            reward = PICKUP_REW
            has_pkg = 1
        else:
            reward = WALL_PEN
    elif executed_action == 'drop':
        if (x, y) in DROPS and has_pkg == 1:
            reward = DROP_REW
            has_pkg = 0
            done = True
        else:
            reward = WALL_PEN

    # Boundary check
    if not in_bounds(nx, ny):
        reward = WALL_PEN
        nx, ny = x, y

    # Bird collision check
    for (bx, by) in birds:
        if (nx, ny) == (bx, by):
            reward = WALL_PEN
            done = True
            nx, ny = x, y
            break

    # Diagonal movement penalty
    if is_diagonal(executed_action) and (nx, ny) != (x, y):
        reward = DIAG_COST

    # Move birds after drone action
    birds2, dirs2 = move_birds(birds, dirs)
    next_state = (int(nx), int(ny), int(has_pkg))
    
    return next_state, float(reward), bool(done), birds2, dirs2, reflex_used, executed_action
