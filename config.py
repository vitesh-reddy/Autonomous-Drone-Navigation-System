# =========================
# CONFIGURATION
# =========================

# Grid and Display Settings
GRID_SIZE = 30
CELL = 25
WINDOW_W = GRID_SIZE * CELL
INFO_BAR = 40
WINDOW_H = WINDOW_W + INFO_BAR

# Locations
PICKUPS = [(5, 5), (25, 10), (6, 22), (18, 15)]
DROPS = [(2, 28), (28, 5), (23, 25), (10, 26)]

# Actions
ACTIONS = [
    'up', 'down', 'left', 'right',
    'up_left', 'up_right', 'down_left', 'down_right',
    'pickup', 'drop'
]

# Reward Structure
STEP_COST = -1.0
DIAG_COST = -1.5
WALL_PEN = -5.0
PICKUP_REW = 20.0
DROP_REW = 40.0

# Training Configuration
EPISODES = 2000
MAX_STEPS = 120

# Bird Configuration
NUM_BIRDS = 50
MOVE_PROB = 0.5
BIRD_RANDOM_DRIFT_PROB = 0.10
BIRD_VEL_CHOICES = [-1, 0, 1]

# Safety Mechanisms
DANGER_RADIUS_CELLS = 1
REFLEX_ENABLED = True

# Visualization
VIS_EPISODES = [1, 800, EPISODES]

# Learning Parameters
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
LAMBDA = 0.8  # For SARSA(lambda)

# Random Seed
RSEED = None
