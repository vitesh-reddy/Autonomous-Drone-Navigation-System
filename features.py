import numpy as np
import math
from config import GRID_SIZE, NUM_BIRDS, PICKUP, DROP
from utils import euclid


def make_feature_vector(state, birds):
    """
    Create feature vector for linear function approximation.
    
    Features (10 dimensions):
    - Position (normalized): x, y
    - Has package: binary
    - Distance to pickup (normalized)
    - Distance to drop (normalized)
    - Bird distances (5 birds, normalized)
    
    Args:
        state: (x, y, has_package)
        birds: List of bird positions
    
    Returns:
        Feature vector as numpy array
    """
    x, y, has_pkg = state
    
    # Normalize position to [0, 1]
    fx = x / (GRID_SIZE - 1)
    fy = y / (GRID_SIZE - 1)
    f_has = float(has_pkg)

    # Normalize distances by max grid diagonal
    max_dist = math.hypot(GRID_SIZE - 1, GRID_SIZE - 1)
    pdist = euclid((x, y), PICKUP) / max_dist
    ddist = euclid((x, y), DROP) / max_dist

    # Bird distances
    bird_dists = []
    for b in birds:
        bird_dists.append(euclid((x, y), b) / max_dist)

    # Pad with max distance if fewer birds than NUM_BIRDS
    while len(bird_dists) < NUM_BIRDS:
        bird_dists.append(1.0)

    # Combine all features
    feat = [fx, fy, f_has, pdist, ddist] + bird_dists[:NUM_BIRDS]
    return np.array(feat, dtype=np.float32)
