# Configuration Guide

This guide explains all configurable parameters in `config.py`.

---

## Grid & Display Settings

```python
GRID_SIZE = 10          # Grid dimensions (10×10)
CELL = 60               # Pixel size per cell
WINDOW_W = 600          # Window width (calculated)
WINDOW_H = 640          # Window height (calculated)
INFO_BAR = 40           # Info display height
```

**When to modify:**
- Larger grid: increase `GRID_SIZE` (e.g., 15 for 15×15)
- Smaller display: decrease `CELL`

---

## Environment Locations

```python
PICKUP = (8, 4)         # Pickup location (row, col)
DROP = (1, 9)           # Drop location (row, col)
```

**When to modify:**
- Change task difficulty by moving locations farther/closer

---

## Actions Available

```python
ACTIONS = ['up', 'down', 'left', 'right',
           'up_left', 'up_right', 'down_left', 'down_right',
           'pickup', 'drop']
```

All 10 actions are available to the agent.

---

## Reward Structure

```python
STEP_COST = -1.0        # Cost per movement step
DIAG_COST = -1.5        # Additional cost for diagonal movement
WALL_PEN = -5.0         # Penalty for hitting wall/bird
PICKUP_REW = 20.0       # Reward for picking up package
DROP_REW = 40.0         # Reward for dropping package
```

**When to modify:**
- Increase `DROP_REW` to encourage faster task completion
- Increase `STEP_COST` to encourage efficiency
- Decrease `DIAG_COST` to allow more diagonal movement

**Example - Harder task:**
```python
STEP_COST = -2.0
DIAG_COST = -2.5
DROP_REW = 50.0
```

---

## Training Configuration

```python
EPISODES = 2000         # Number of training episodes
MAX_STEPS = 120         # Max steps per episode
```

**When to modify:**
- More episodes for better convergence (e.g., 5000)
- Fewer episodes for faster testing (e.g., 500)
- Larger grid = need more steps

---

## Bird Configuration

```python
NUM_BIRDS = 5              # Number of moving obstacles
MOVE_PROB = 0.5            # Probability bird moves per step
BIRD_RANDOM_DRIFT_PROB = 0.10   # Probability of random direction
BIRD_VEL_CHOICES = [-1, 0, 1]   # Bird velocity options
```

**When to modify:**
- More birds = harder task (e.g., 10)
- `MOVE_PROB = 1.0` = always moving (harder)
- `MOVE_PROB = 0.2` = mostly stationary (easier)

---

## Safety Mechanisms

```python
DANGER_RADIUS_CELLS = 1    # Reflex safety radius
REFLEX_ENABLED = True      # Enable/disable safety shielding
```

**When to modify:**
- `DANGER_RADIUS_CELLS = 2` for wider safety zone
- `REFLEX_ENABLED = False` to train without safety (risky)

---

## Visualization

```python
VIS_EPISODES = [1, 800, EPISODES]  # Which episodes to replay
```

**When to modify:**
- `[1, 500, 1000, 2000]` to see more snapshots
- `[EPISODES]` to see only final episode

---

## Learning Parameters

```python
ALPHA = 0.1             # Learning rate (0.0 - 1.0)
GAMMA = 0.9             # Discount factor (0.0 - 1.0)
LAMBDA = 0.8            # Eligibility trace decay (0.0 - 1.0)
```

**Guidelines:**
- **ALPHA**: 
  - Higher (0.3-0.5) = faster learning, more unstable
  - Lower (0.01-0.05) = slower learning, more stable
  
- **GAMMA**:
  - Higher (0.95-0.99) = values long-term rewards more
  - Lower (0.5-0.9) = focuses on immediate rewards
  
- **LAMBDA** (SARSA(λ) only):
  - Closer to 1.0 = longer eligibility traces
  - Closer to 0.0 = shorter traces (closer to standard SARSA)

---

## Random Seed

```python
RSEED = None            # Random seed (None = no fixed seed)
```

**When to modify:**
- `RSEED = 42` for reproducible results
- `RSEED = None` for different birds each run

---

## Example Configurations

### 🎓 Learning/Testing
```python
EPISODES = 100
MAX_STEPS = 50
ALPHA = 0.2
NUM_BIRDS = 2
RSEED = 42
```

### 🏆 Full Training
```python
EPISODES = 5000
MAX_STEPS = 150
ALPHA = 0.1
NUM_BIRDS = 8
DANGER_RADIUS_CELLS = 2
```

### 🚀 Quick Demo
```python
EPISODES = 500
MAX_STEPS = 100
NUM_BIRDS = 3
```

### 🤖 No Safety (Research)
```python
REFLEX_ENABLED = False
NUM_BIRDS = 10
EPISODES = 3000
```

---

## Tips for Better Learning

1. **For stable learning:**
   - Lower `ALPHA` (e.g., 0.05)
   - Higher `EPISODES` (e.g., 3000+)

2. **For exploring more:**
   - Epsilon schedule already decays: no changes needed

3. **For harder tasks:**
   - Increase `NUM_BIRDS`
   - Increase `STEP_COST`
   - Decrease `PICKUP_REW` / `DROP_REW`

4. **For faster training:**
   - Reduce `EPISODES`
   - Increase `ALPHA`
   - Reduce `GRID_SIZE` or `NUM_BIRDS`

---
