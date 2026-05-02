import random
import math
import numpy as np
from collections import defaultdict
from config import ACTIONS, EPISODES, MAX_STEPS, ALPHA, GAMMA, LAMBDA, VIS_EPISODES
from environment import bird_reset, step_with_reflex


def choose_action_eps_greedy_tab(state, Q, epsilon):
    """Epsilon-greedy action selection for tabular Q-learning."""
    if np.random.random() < epsilon:
        return random.choice(ACTIONS)
    
    best_a, best_v = None, -1e18
    for a in ACTIONS:
        v = Q.get((state, a), 0.0)
        if v > best_v:
            best_v, best_a = v, a
    return best_a


def epsilon_schedule(ep):
    """Epsilon decay schedule: 1/sqrt(episode)."""
    return 1.0 / math.sqrt(ep)


def sarsa_lambda_reflex_train():
    """
    Train SARSA(lambda) with eligibility traces and reflex shielding.
    
    Returns:
        records: List of trajectory records for visualization
        ep_rewards: Episode returns
        ep_lens: Episode lengths
        epsilons: Epsilon values per episode
    """
    Q = {}
    records = []

    ep_rewards = []
    ep_lens = []
    epsilons = []

    for ep in range(1, EPISODES + 1):
        eps = epsilon_schedule(ep)
        birds, dirs, types = bird_reset()

        # Eligibility traces
        E = defaultdict(float)

        state = (1, 1, 0)
        total = 0.0
        path = [state]
        birds_traj = [list(birds)]
        reflex_flags = [False]
        actions_taken = ['START']
        rewards_taken = [0.0]

        a = choose_action_eps_greedy_tab(state, Q, eps)
        for _ in range(MAX_STEPS):
            s_next, r, done, birds, dirs, reflex_used, executed_action = step_with_reflex(state, a, birds, dirs)

            # SARSA(lambda) Update
            q_sa = Q.get((state, a), 0.0)

            if done:
                q_sna = 0.0
                delta = r + GAMMA * q_sna - q_sa
                a_next = 'TERMINAL'
            else:
                a_next = choose_action_eps_greedy_tab(s_next, Q, eps)
                q_sna = Q.get((s_next, a_next), 0.0)
                delta = r + GAMMA * q_sna - q_sa

            # Accumulate eligibility
            E[(state, a)] += 1.0

            # Update all Q values and decay eligibilities
            for (s_a), e_val in list(E.items()):
                Q[s_a] = Q.get(s_a, 0.0) + ALPHA * delta * e_val
                E[s_a] = GAMMA * LAMBDA * e_val
                if E[s_a] < 1e-6:
                    del E[s_a]

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
        best_a, best_v = None, -1e18
        for a in ACTIONS:
            v = Q.get((state, a), 0.0)
            if v > best_v:
                best_v, best_a = v, a
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
