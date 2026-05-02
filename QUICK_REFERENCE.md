# Quick Reference Card

## File Structure at a Glance

```
IAS Project/
├── main.py                    ← START HERE (entry point)
├── config.py                  ← Change parameters
├── algorithms/
│   ├── sarsa.py              ← SARSA algorithm
│   ├── sarsa_lambda.py        ← SARSA(λ) algorithm  
│   └── lfa_sarsa.py           ← LFA-SARSA algorithm
├── environment.py             ← Grid world simulator
├── utils.py                   ← Math utilities
├── features.py                ← LFA feature vectors
├── visualization.py           ← Pygame display
├── plotting.py                ← Matplotlib graphs
├── run.bat / run.sh           ← Click to run
├── README.md                  ← Project overview
├── ARCHITECTURE.md            ← System design
├── CONFIGURATION_GUIDE.md     ← Parameter tuning
└── assets/                    ← Image files here
```

---

## Running the Project

### Windows
```bash
Double-click: run.bat
```

### Mac/Linux
```bash
bash run.sh
```

### Any System
```bash
python main.py
```

---

## Configuration Cheat Sheet

### Making Training Faster
```python
# In config.py:
EPISODES = 100        # Down from 2000
GRID_SIZE = 5         # Smaller grid
NUM_BIRDS = 1         # Fewer obstacles
```

### Making Task Harder
```python
# In config.py:
NUM_BIRDS = 10
STEP_COST = -3.0
DANGER_RADIUS_CELLS = 2
BIRD_RANDOM_DRIFT_PROB = 0.5
```

### Better Learning
```python
# In config.py:
ALPHA = 0.05          # Slower, more stable
EPISODES = 5000       # More training
GAMMA = 0.95          # Values long-term rewards
```

---

## Module Quick Docs

**config.py** - Constants only
```python
from config import GRID_SIZE, EPISODES, NUM_BIRDS, ALPHA
```

**environment.py** - Simulation
```python
from environment import bird_reset, step_with_reflex
birds, dirs, types = bird_reset()
next_state, reward, done, birds, dirs, reflex_used, action = step_with_reflex(state, action, birds, dirs)
```

**algorithms/\* - Training**
```python
from algorithms import sarsa_reflex_train
records, ep_rewards, ep_lens, epsilons = sarsa_reflex_train()
```

**visualization.py** - Display**
```python
from visualization import visualize_records
visualize_records(records, title="My Algorithm")
```

**plotting.py** - Graphs**
```python
from plotting import plot_three_subplots, plot_comparison
plot_three_subplots((records, rewards, lengths, epsilons), "Algorithm Name")
```

---

## Expected Outputs

After running `python main.py`, you'll see:

1. **Training Progress** (console)
   ```
   Training SARSA + Reflex...
   Done SARSA.
   Training SARSA(lambda) + Reflex...
   Done SARSA(lambda).
   ...
   ```

2. **Performance Plots** (matplotlib windows)
   - 4 windows total
   - Each shows: returns, epsilon decay, episode lengths
   - Can save/zoom/interact

3. **Visualizations** (pygame windows)
   - Agent trajectory playback
   - Shows drone, birds, items
   - Orange trails = reflex safety action
   - Gray trails = normal action

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named pygame" | `pip install pygame` |
| "No module named numpy" | `pip install numpy` |
| Image loading error | Place PNG files in `assets/` folder |
| Slow training | Reduce EPISODES in config.py |
| Pygame window blank | Check grid.png is 600x600 pixels |

---

## Adding a New Algorithm

1. Create `algorithms/my_algo.py`

2. Add function:
```python
def my_algo_reflex_train():
    records = []
    ep_rewards = []
    
    for ep in range(1, EPISODES + 1):
        # Training code here
        # Must call step_with_reflex() for actions
        pass
    
    return records, ep_rewards, ep_lens, epsilons
```

3. Import in `main.py`:
```python
from algorithms import sarsa_reflex_train, my_algo_reflex_train
```

4. Call in `main()`:
```python
rec = my_algo_reflex_train()
plot_three_subplots(rec, "My Algorithm")
```

---

## Key Hyperparameters

| Name | Default | Range | Effect |
|------|---------|-------|--------|
| EPISODES | 2000 | 100-10000 | Training duration |
| ALPHA | 0.1 | 0.01-0.5 | Learning speed |
| GAMMA | 0.9 | 0.5-0.99 | Future value weight |
| NUM_BIRDS | 5 | 1-15 | Task difficulty |
| DANGER_RADIUS_CELLS | 1 | 0-3 | Safety zone size |
| STEP_COST | -1.0 | -5 to 0 | Efficiency penalty |

---

## File Sizes (Approximate)

| File | Lines | Purpose |
|------|-------|---------|
| config.py | 55 | Constants |
| utils.py | 35 | Helpers |
| features.py | 45 | LFA features |
| sarsa.py | 120 | Algorithm |
| sarsa_lambda.py | 135 | Algorithm |
| lfa_sarsa.py | 140 | Algorithm |
| environment.py | 150 | Simulation |
| visualization.py | 140 | Display |
| plotting.py | 90 | Graphs |
| main.py | 70 | Control |
| **Total** | **920** | **Code** |

---

## Performance Targets

| Metric | Typical Value |
|--------|---------------|
| Training time | 3-5 minutes |
| Episodes to convergence | 500-1500 |
| Max episode steps | ~30-60 (with reflex) |
| Memory usage | <500 MB |
| Disk space needed | ~20 MB |

---

## Common Experiments

### Compare Algorithms
Already done by `main.py`! Check the comparison plot.

### Study Effect of Birds
```python
# Run with: NUM_BIRDS = 1, 5, 10
# Compare ep_rewards curves
```

### Reflex Impact
```python
# In environment.py, temporarily set:
REFLEX_ENABLED = False
# Compare trajectories with vs without
```

### Learning Rate Effect
```python
# Run with: ALPHA = 0.01, 0.05, 0.1, 0.2
# Compare convergence speed
```

---

## Useful Matplotlib Commands

When plots pop up:

| Button | Action |
|--------|--------|
| 🏠 | Reset view |
| ◀ ▶ | Pan left/right |
| 🔍 | Zoom tool |
| 💾 | Save plot as PNG |

---

## Environment Details

**State Space**:
- Position: 10×10 = 100 positions
- Package: 2 states (picked up or not)
- Total: 200 states (100 × 2)

**Action Space**: 10 actions
- 8 movements: up, down, left, right, diagonals
- 2 actions: pickup, drop

**Observation**: Full state (position + package status)

**Reward Signal**: Immediate reward per step

---

## Feature Vector (LFA)

```
[x_norm, y_norm, has_package, dist_to_pickup, dist_to_drop, 
 bird1_dist, bird2_dist, bird3_dist, bird4_dist, bird5_dist]
```

All normalized to [0, 1] range.

---

## Common Questions

**Q: Why is training slow?**
A: Accuracy > speed. More episodes = better learning. Reduce EPISODES to test faster.

**Q: Do I need the GPU?**
A: No, CPU only. No neural networks here!

**Q: Can I add more algorithms?**
A: Yes! Follow the template in algorithms/sarsa.py

**Q: Where are my results saved?**
A: Plots display in matplotlib windows. Use "Save" button to keep them.

**Q: How do I pause visualization?**
A: Close the pygame window to skip to next trajectory.

**Q: Can I modify rewards?**
A: Yes! Edit config.py - no code changes needed.

---

## Advanced: Custom Training Loop

```python
from algorithms import sarsa_reflex_train
from plotting import plot_three_subplots

# Train with custom config
records, rewards, lengths, epsilons = sarsa_reflex_train()

# Analyze
avg_reward = sum(rewards[-100:]) / 100  # Last 100 episodes
print(f"Average reward: {avg_reward:.2f}")

# Plot
plot_three_subplots(
    (records, rewards, lengths, epsilons),
    "My Custom SARSA"
)
```

---

## Data Structures

**Episode Record**:
```python
{
    "episode": int or "Greedy",
    "path": [(x, y, has_pkg), ...],  # State trajectory
    "birds_traj": [[(bx, by), ...], ...],  # Bird positions per step
    "total_reward": float,
    "epsilon": float,
    "bird_types": [0 or 1, ...],  # For rendering
    "reflex_flags": [True/False, ...],  # Which steps used safety
    "actions": ['START', 'up', ...],  # Action taken per step
    "immediate_rewards": [0.0, ...],  # Reward per step
}
```

---

## Success Indicators

Your project is working if:

✅ Training completes without errors
✅ Matplotlib windows appear with 3 plots each
✅ Pygame window shows drone navigating grid
✅ Orange trails appear (reflex actions)
✅ Final "Greedy" rollout shown in visualization
✅ Comparison plot shows three curves

---

**Last Updated**: IAS Project Refactoring v1.0  
**Status**: Production Ready ✅
