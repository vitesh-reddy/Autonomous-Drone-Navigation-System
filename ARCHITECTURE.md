# Project Architecture

This document describes the architectural design and module interactions.

---

## Overview

The IAS project follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────┐
│         main.py                     │
│   (Orchestration & Control)         │
└────────┬────────────────────────────┘
         │
    ┌────┴────────────────────────────┬──────────────────┬─────────────────┐
    │                                 │                  │                 │
    ▼                                 ▼                  ▼                 ▼
┌──────────────┐            ┌──────────────────┐  ┌────────────┐  ┌──────────────┐
│  algorithms/ │            │ visualization.py │  │ plotting.py│  │ environment.py
│ - sarsa.py   │            │ (Pygame Views)   │  │(Matplotlib)│  │ (Simulation)
│ - sarsa_...  │            └──────────────────┘  └────────────┘  └───────┬──────┘
│ - lfa_sarsa  │                                                           │
└──────┬───────┘                                                           │
       │                                             ┌─────────────────────┘
       │                                             │
       ▼                                             ▼
    ┌──────────────┐                         ┌──────────────┐
    │ config.py    │                         │ utils.py     │
    │ (Constants)  │                         │ (Helpers)    │
    └──────────────┘                         └──────────────┘
                                                     ▲
                                                     │
                                            ┌────────┴─────────┐
                                            │                  │
                                         features.py      environment.py
                                        (LFA Feature       (State/Reward)
                                         Vectors)
```

---

## Module Responsibilities

### `main.py` - Orchestrator
**Role**: Central control point

- Imports all algorithm training functions
- Calls algorithms sequentially
- Triggers plotting functions
- Manages visualization pipeline
- Provides user feedback and progress indication

**Key Functions**:
- `main()` - Coordinates entire workflow

---

### `config.py` - Single Source of Truth
**Role**: Configuration management

- Defines all constants and hyperparameters
- Centralized for easy tuning
- No business logic—only data

**Dependencies**: None (imported by all modules)

---

### `environment.py` - Simulation Engine
**Role**: Grid world management

- **`bird_reset()`** - Initialize moving obstacles
- **`move_birds()`** - Update bird positions with physics
- **`step_with_reflex()`** - Execute agent actions
  - Applies action
  - Checks collisions
  - Applies reflex shielding
  - Updates bird positions
  - Returns reward

**Dependencies**:
- `config.py` - for constants
- `utils.py` - for math helpers

---

### `utils.py` - Mathematical Utilities
**Role**: Pure utility functions

- **`in_bounds()`** - Boundary checking
- **`euclid()`** - Distance calculation
- **`is_diagonal()`** - Action classification
- **`next_xy_from_action()`** - Position delta computation

**Dependencies**:
- `config.py` - for GRID_SIZE

---

### `features.py` - Feature Engineering
**Role**: State representation for LFA

- **`make_feature_vector()`** - Converts state to 10D vector
  - Position normalization
  - Goal distances
  - Bird distances
  - Package status

**Used by**: LFA-SARSA algorithm only

**Dependencies**:
- `config.py` - GRID_SIZE, PICKUP, DROP, NUM_BIRDS
- `utils.py` - euclid()

---

### `algorithms/` - Learning Algorithms
**Role**: Training logic

#### `algorithms/sarsa.py`
- Tabular Q-learning with SARSA update
- On-policy learning
- Functions:
  - `choose_action_eps_greedy_tab()` - Action selection
  - `epsilon_schedule()` - Decay schedule
  - `sarsa_reflex_train()` - Main training loop

#### `algorithms/sarsa_lambda.py`
- SARSA with eligibility traces
- Enables multi-step credit assignment
- Functions: Same as SARSA + eligibility trace management

#### `algorithms/lfa_sarsa.py`
- SARSA with linear function approximation
- Generalizes across state space
- Weight updates instead of Q-table updates
- Uses `make_feature_vector()` from `features.py`

**Common Pattern**:
```
Initialize parameters
For each episode:
  Reset environment
  For each step:
    1. Observe state
    2. Choose action (ε-greedy)
    3. Execute action (with reflex)
    4. Update value function
    5. Check terminal
Return: (records, rewards, lengths, epsilons)
```

**Dependencies**:
- `config.py` - learning parameters, episode config
- `environment.py` - step_with_reflex()
- `features.py` - (LFA only) make_feature_vector()

---

### `visualization.py` - Pygame Renderer
**Role**: Interactive trajectory playback

- **`visualize_records()`** - Animate agent paths
  - Loads image assets
  - Renders each step
  - Shows danger zones
  - Color-codes reflex actions
  - Real-time statistics overlay

**Input**: Records from training (trajectories + metadata)

**Dependencies**:
- `config.py` - grid dimensions, locations
- `utils.py` - euclid() for distance display

---

### `plotting.py` - Matplotlib Visualization
**Role**: Statistical analysis plots

- **`plot_three_subplots()`** - Individual algorithm metrics
  - Episode returns
  - Epsilon decay
  - Episode lengths

- **`plot_comparison()`** - Multi-algorithm comparison
  - Overlaid metrics
  - Legend and colors

**Input**: Training history tuples

**Dependencies**:
- `matplotlib` (external)

---

## Data Flow

### Training Loop
```
main.py
  ↓
algorithms/*_train()
  ├─ environment.bird_reset()
  ├─ for each episode:
  │   ├─ environment.step_with_reflex()
  │   │   ├─ utils.next_xy_from_action()
  │   │   ├─ utils.euclid() [for reflex]
  │   │   ├─ environment.move_birds()
  │   │   └─ returns: next_state, reward, done, ...
  │   └─ Update Q-values/weights
  └─ returns: (records, rewards, lengths, epsilons)
```

### Visualization Pipeline
```
main.py
  ├─ plotting.plot_three_subplots(data)
  │   └─ matplotlib display
  ├─ plotting.plot_comparison([data1, data2, data3])
  │   └─ matplotlib display
  └─ visualization.visualize_records(records)
      ├─ pygame.init()
      ├─ for each record step:
      │   ├─ render background
      │   ├─ render birds
      │   ├─ render items
      │   ├─ render danger zone (utils.euclid)
      │   └─ display step
      └─ pygame.quit()
```

---

## Extension Points

### Adding a New Algorithm

1. Create `algorithms/new_algo.py`
2. Implement `new_algo_reflex_train()` function
3. Return: `(records, rewards, lengths, epsilons)`
4. Import in `main.py`
5. Add to training loop

Example template:
```python
# algorithms/new_algo.py
from config import ACTIONS, EPISODES, MAX_STEPS, ALPHA, GAMMA
from environment import bird_reset, step_with_reflex

def new_algo_reflex_train():
    records = []
    ep_rewards = []
    
    for ep in range(1, EPISODES + 1):
        birds, dirs, types = bird_reset()
        state = (1, 1, 0)
        # Training logic...
        # Must include reflex handling
    
    return records, ep_rewards, ep_lens, epsilons
```

### Adding Custom Metrics

Modify `plotting.py` to add new subplot types:
```python
def plot_custom_metric(hist, label):
    _, rewards, lengths, epsilons = hist
    # Custom plotting logic
```

### Changing Reward Structure

Edit `config.py` rewards, no code changes needed elsewhere.

---

## Key Design Decisions

1. **Single-file config**: Easy to modify parameters globally
2. **Modular algorithms**: Each can be developed/tested independently
3. **Unified interface**: All algorithms return same format
4. **Separate concerns**: U/I (visualization), logic (algorithms), simulation (environment)
5. **Pure functions where possible**: utils.py has no side effects
6. **Reflex as universal wrapper**: Gets applied in environment.step_with_reflex()

---

## Performance Characteristics

| Module | Time Cost | Notes |
|--------|-----------|-------|
| SARSA | ~30-60s | Simplest, fastest |
| SARSA(λ) | ~35-70s | Slightly slower (eligibility trace ops) |
| LFA-SARSA | ~40-80s | Slowest (feature vector computation) |
| Visualization | ~2-5s | Per episode, depending on path length |
| Plotting | ~5-10s | Depends on matplotlib backend |

Total runtime: ~3-5 minutes on average machine.

---

## Thread Safety

Current implementation is single-threaded. For parallel training:
- Each algorithm call is independent
- Could use `multiprocessing` to train simultaneously
- Visualization must remain sequential (pygame limitation)

---
