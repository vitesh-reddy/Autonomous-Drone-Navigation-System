import random
import math
import numpy as np
from config import ACTIONS, EPISODES, MAX_STEPS, ALPHA, GAMMA, VIS_EPISODES, NUM_BIRDS
from environment import bird_reset, step_with_reflex
from features import make_feature_vector


def epsilon_schedule(ep):
    """Epsilon decay schedule: 1/sqrt(episode)."""
    return 1.0 / math.sqrt(ep)


def lfa_sarsa_reflex_train():
    """
    Train SARSA with Linear Function Approximation and reflex shielding.
    
    Uses feature vectors and weight updates for generalization.
    
    Returns:
        records: List of trajectory records for visualization
        ep_rewards: Episode returns
        ep_lens: Episode lengths
        epsilons: Epsilon values per episode
    """
    feat_dim = 5 + NUM_BIRDS
    W = {a: np.zeros(feat_dim, dtype=np.float32) for a in ACTIONS}
    records = []

    ep_rewards = []
    ep_lens = []
    epsilons = []

    for ep in range(1, EPISODES + 1):
        eps = epsilon_schedule(ep)
        birds, dirs, types = bird_reset()

        state = (1, 1, 0)
        total = 0.0
        path = [state]
        birds_traj = [list(birds)]
        reflex_flags = [False]
        actions_taken = ['START']
        rewards_taken = [0.0]

        feats = make_feature_vector(state, birds)
        
        # Epsilon-greedy action selection
        if np.random.random() < eps:
            a = random.choice(ACTIONS)
        else:
            vals = {a: float(W[a].dot(feats)) for a in ACTIONS}
            a = max(vals, key=vals.get)

        for _ in range(MAX_STEPS):
            # Get Q(S, A)
            q_sa = float(W[a].dot(feats))
            s_next, r, done, birds, dirs, reflex_used, executed_action = step_with_reflex(state, a, birds, dirs)

            # Determine Q(S', A')
            if done:
                q_sna = 0.0
                a_next = 'TERMINAL'
            else:
                feats_next = make_feature_vector(s_next, birds)
                if np.random.random() < eps:
                    a_next = random.choice(ACTIONS)
                else:
                    vals_next = {a2: float(W[a2].dot(feats_next)) for a2 in ACTIONS}
                    a_next = max(vals_next, key=vals_next.get)
                q_sna = float(W[a_next].dot(feats_next))

            # SARSA weight update (LFA)
            td = r + GAMMA * q_sna - q_sa
            W[a] += ALPHA * td * feats

            total += r
            path.append(s_next)
            birds_traj.append(list(birds))
            reflex_flags.append(reflex_used)
            actions_taken.append(executed_action)
            rewards_taken.append(r)

            state = s_next
            if done:
                break
            else:
                feats = feats_next
                a = a_next

        ep_rewards.append(total)
        ep_lens.append(len(path) - 1)
        epsilons.append(eps)

        if ep in VIS_EPISODES:
            records.append({
                "episode": ep,
                "path": path,
                "birds_traj": birds_traj,
                "total_reward": total,
                "epsilon": eps,
                "bird_types": types,
                "reflex_flags": reflex_flags,
                "actions": actions_taken,
                "immediate_rewards": rewards_taken
            })

    # Final greedy rollout
    birds, dirs, types = bird_reset()
    state = (1, 1, 0)
    total = 0.0
    path = [state]
    birds_traj = [list(birds)]
    reflex_flags = [False]
    actions_taken = ['START']
    rewards_taken = [0.0]

    while len(path) < MAX_STEPS + 1:
        feats = make_feature_vector(state, birds)
        vals = {a: float(W[a].dot(feats)) for a in ACTIONS}
        best_a = max(vals, key=vals.get)
        s_next, r, done, birds, dirs, reflex_used, executed_action = step_with_reflex(state, best_a, birds, dirs)
        total += r
        path.append(s_next)
        birds_traj.append(list(birds))
        reflex_flags.append(reflex_used)
        actions_taken.append(executed_action)
        rewards_taken.append(r)
        state = s_next
        if done:
            break

    records.append({
        "episode": "Greedy",
        "path": path,
        "birds_traj": birds_traj,
        "total_reward": total,
        "epsilon": 0.0,
        "bird_types": types,
        "reflex_flags": reflex_flags,
        "actions": actions_taken,
        "immediate_rewards": rewards_taken
    })

    return records, ep_rewards, ep_lens, epsilons
