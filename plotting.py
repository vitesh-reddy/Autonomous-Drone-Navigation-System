import matplotlib.pyplot as plt


def plot_three_subplots(hist, label, color=None):
    """
    Plot three subplots showing training metrics.
    
    Subplots:
    1. Episode returns over time
    2. Epsilon schedule
    3. Episode lengths
    
    Args:
        hist: Tuple of (records, rewards, lengths, epsilons)
        label: Algorithm name for title
        color: Optional color for plot lines
    """
    _, rewards, lengths, epsilons = hist

    default_map = {
        "SARSA + Reflex": "tab:blue",
        "SARSA": "tab:blue",
        "SARSA(lambda) + Reflex": "tab:green",
        "SARSA(lambda)": "tab:green",
        "LFA-SARSA + Reflex": "tab:orange",
        "LFA-SARSA": "tab:orange",
        "LFA SARSA": "tab:orange"
    }

    if color is None:
        color = default_map.get(label, "tab:blue")

    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
    ax0, ax1, ax2 = axes

    # Episode Return
    ax0.plot(rewards, color=color)
    ax0.set_title(f"{label} — Episode Return")
    ax0.set_ylabel("Return")
    ax0.grid(True)

    # Epsilon Schedule
    ax1.plot(epsilons, color=color)
    ax1.set_title(f"{label} — Epsilon Schedule (1/sqrt(k))")
    ax1.set_ylabel("Epsilon")
    ax1.grid(True)

    # Episode Lengths
    ax2.plot(lengths, color=color)
    ax2.set_title(f"{label} — Episode Lengths")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Steps")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


def plot_comparison(algorithms_hist, labels, colors=None):
    """
    Compare multiple algorithms on the same plot.
    
    Args:
        algorithms_hist: List of (records, rewards, lengths, epsilons) tuples
        labels: List of algorithm names
        colors: Optional list of colors for each algorithm
    """
    if colors is None:
        colors = ["tab:blue", "tab:green", "tab:orange", "tab:red", "tab:purple"]

    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    ax0, ax1, ax2 = axes

    for (_, rewards, lengths, epsilons), label, color in zip(algorithms_hist, labels, colors):
        ax0.plot(rewards, label=label, color=color, alpha=0.7)
        ax1.plot(epsilons, label=label, color=color, alpha=0.7)
        ax2.plot(lengths, label=label, color=color, alpha=0.7)

    ax0.set_title("Episode Returns Comparison")
    ax0.set_ylabel("Return")
    ax0.legend()
    ax0.grid(True)

    ax1.set_title("Epsilon Schedules")
    ax1.set_ylabel("Epsilon")
    ax1.legend()
    ax1.grid(True)

    ax2.set_title("Episode Lengths Comparison")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Steps")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
