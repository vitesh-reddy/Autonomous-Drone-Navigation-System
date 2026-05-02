# Intelligent Autonomous Systems (IAS) Project

Safe drone navigation in a dynamic grid world using reinforcement learning.

This project models a drone that must navigate from a start position to pickup and drop locations while avoiding moving bird obstacles. The learning code compares three RL approaches, all built around the same environment and a reflex safety layer.

## Project Idea

The goal is to learn a policy that can complete a pickup-and-delivery task efficiently and safely.

The agent must:

1. Move through a 2D grid.
2. Pick up a package at a pickup location.
3. Deliver it to a drop location.
4. Avoid collisions with moving birds.

To make the task realistic, the environment is stochastic. Birds move over time, and the agent may need to change course even when the learned policy suggests a risky move. That is handled by reflex shielding.

## Core Algorithms

The repository implements three reinforcement learning methods:

### SARSA
Tabular on-policy temporal-difference learning.

### SARSA(lambda)
SARSA with eligibility traces for better credit assignment across multiple steps.

### LFA-SARSA
SARSA with linear function approximation, which replaces the Q-table with a weight vector and feature-based state representation.

All three variants use:

- Epsilon-greedy exploration.
- The same environment dynamics.
- The same reward structure.
- The same reflex safety mechanism.

## Environment

The world is a square grid controlled from `config.py`.

Current default settings:

- Grid size: 30 x 30
- Cell size: 25 px
- Pickup locations: 2
- Drop locations: 2
- Moving birds: 50
- Episode length limit: 120 steps

The drone state is represented as:

```text
(x, y, has_package)
```

Where:

- `x`, `y` are the drone coordinates on the grid.
- `has_package` is `0` when the drone is empty and `1` when it is carrying a package.

Birds have their own positions and velocity directions. They may move each step, drift randomly, and bounce off boundaries.

## Actions

The action space has 10 actions:

- `up`
- `down`
- `left`
- `right`
- `up_left`
- `up_right`
- `down_left`
- `down_right`
- `pickup`
- `drop`

The first 8 actions are movement actions. `pickup` and `drop` are task actions.

## Reward Design

The reward function is designed to encourage successful delivery while penalizing inefficient or unsafe behavior.

Current rewards from `config.py`:

- Step cost: `-1.0`
- Diagonal move cost: `-1.5`
- Wall or invalid-action penalty: `-5.0`
- Pickup reward: `+20.0`
- Drop reward: `+40.0`

Interpretation:

- Every time step is costly, so the agent should finish quickly.
- Diagonal movement is slightly more expensive than orthogonal movement.
- Invalid pickups/drops and boundary collisions are penalized.
- Successful package pickup and delivery are rewarded.
- A successful drop ends the episode.

## Safety Layer: Reflex Shielding

The environment includes a reflex safety mechanism that acts before an unsafe movement is executed.

How it works:

1. The agent proposes an action.
2. If the action is a movement action, the environment checks the intended next position.
3. If the intended position is too close to any bird within the danger radius, the reflex layer searches for a safer alternative.
4. The safest alternative is chosen based on distance from birds, with a small penalty for diagonal moves.

Current safety settings:

- Danger radius: 1 cell
- Reflex enabled: `True`

This is useful because it lets the learning algorithm focus on task completion while the safety layer prevents avoidable risky moves.

## State Representation

### Tabular State

For SARSA and SARSA(lambda), the state used by the Q-table is:

```text
(x, y, has_package)
```

This is the minimal state needed to describe the agent's task progress.

### Feature-Based State

For LFA-SARSA, the state is mapped into a feature vector produced by `features.py`.

The feature vector includes:

- Normalized `x` position.
- Normalized `y` position.
- Package status.
- Distance to the pickup location.
- Distance to the drop location.
- Distances to each bird.

The total feature length is `5 + NUM_BIRDS`, so with 50 birds the vector has 55 dimensions.

## Learning Details

Common learning settings:

- Learning rate: `alpha = 0.1`
- Discount factor: `gamma = 0.9`
- Eligibility trace decay: `lambda = 0.8`
- Episodes: `2000`
- Epsilon schedule: `epsilon = 1 / sqrt(episode)`

Each algorithm trains episode by episode and records:

- Episode returns.
- Episode lengths.
- Epsilon values.
- Trajectory records for visualization.

## Project Modules

### `config.py`
Central place for all environment and learning constants.

### `environment.py`
Contains the simulation logic:

- `bird_reset()` initializes birds, velocities, and bird types.
- `move_birds()` advances the bird positions.
- `step_with_reflex()` applies an action, checks safety, computes reward, and returns the next environment state.

### `utils.py`
Contains math and movement helpers:

- boundary checking
- Euclidean distance
- diagonal-action detection
- action-to-position conversion

### `features.py`
Builds the feature vector used by LFA-SARSA.

### `algorithms/`
Contains the three training implementations:

- `sarsa.py`
- `sarsa_lambda.py`
- `lfa_sarsa.py`

Each trainer returns a tuple shaped like:

```text
(records, episode_rewards, episode_lengths, epsilons)
```

### `plotting.py`
Creates performance plots for training curves.

### `visualization.py`
Replays learned trajectories using pygame and shows:

- Drone position.
- Bird movement.
- Pickup and drop locations.
- Danger radius overlays.
- Reflex-triggered actions highlighted in orange.

## Current Workspace Layout

```text
IAS Project/
├── README.md
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── CONFIGURATION_GUIDE.md
│   └── QUICK_REFERENCE.md
├── config.py
├── environment.py
├── features.py
├── utils.py
├── plotting.py
├── visualization.py
├── main.py
├── algorithms/
│   ├── __init__.py
│   ├── sarsa.py
│   ├── sarsa_lambda.py
│   └── lfa_sarsa.py
├── assets/
└── requirements.txt
```

## Documentation

For a cleaner project root, detailed docs are grouped in `docs/`:

- `docs/README.md` - navigation index for all docs
- `docs/ARCHITECTURE.md` - system design and module interactions
- `docs/CONFIGURATION_GUIDE.md` - all tuning parameters
- `docs/QUICK_REFERENCE.md` - quick commands and troubleshooting

## How to Run

Install dependencies first:

```bash
pip install -r requirements.txt
```

If you want to run the current demo entrypoint:

```bash
python main.py
```

Note: the modular RL algorithms live under `algorithms/`, while `main.py` in this workspace currently runs a visualization demo. If you want the repo to execute the full training pipeline from the README directly, the next step is to wire those training functions into a dedicated driver script.

## Expected Outputs

The RL pipeline is designed to produce:

1. Training logs in the console.
2. Reward, epsilon, and length plots.
3. Pygame replay windows showing drone trajectories.
4. A comparison of SARSA, SARSA(lambda), and LFA-SARSA.

## Why This Project Is Useful

This project demonstrates several important ideas in intelligent autonomous systems:

- Safe RL in a dynamic environment.
- Tabular versus function-approximation learning.
- Eligibility traces for temporal credit assignment.
- State design for navigation problems.
- Reward shaping for task completion and safety.
- Visualization-driven analysis of learned behavior.

## Customization

You can change the behavior of the system by editing `config.py`.

Examples:

```python
EPISODES = 5000
NUM_BIRDS = 10
GRID_SIZE = 15
ALPHA = 0.05
DANGER_RADIUS_CELLS = 2
```

## Dependencies

- `numpy`
- `pygame`
- `matplotlib`

## Author

Student ID: `S20230030399`
