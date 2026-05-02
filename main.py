import argparse
import random
from config import GRID_SIZE, PICKUPS, DROPS, NUM_BIRDS
from visualization import visualize_records

def create_episode(episode_index):
    # waypoints
    targets = [
        (PICKUPS[0], 0, 1),
        (DROPS[0], 1, 0),
        (PICKUPS[1], 0, 1),
        (DROPS[1], 1, 0)
    ]
    
    path = []
    birds_traj = []
    reflex_flags = []
    
    drone_x, drone_y = 0, 0
    has_pkg = 0
    
    # Initialize random birds far from start
    birds = []
    for _ in range(NUM_BIRDS):
        while True:
            bx, by = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if abs(bx - 0) + abs(by - 0) > 4:
                birds.append((bx, by))
                break
    
    for target in targets:
        tx, ty = target[0]
        # while not at target
        while drone_x != tx or drone_y != ty:
            path.append((drone_x, drone_y, has_pkg))
            birds_traj.append(list(birds))
            
            # 1. Move birds randomly
            new_birds = []
            for bx, by in birds:
                if random.random() < 0.5: # 50% chance to move
                    dx, dy = random.choice([(-1,0), (1,0), (0,-1), (0,1)])
                    nbx, nby = bx + dx, by + dy
                    nbx = max(0, min(GRID_SIZE-1, nbx))
                    nby = max(0, min(GRID_SIZE-1, nby))
                    new_birds.append((nbx, nby))
                else:
                    new_birds.append((bx, by))
            birds = new_birds
            
            # 2. Drone intention
            candidates = [
                (drone_x+dx, drone_y+dy) for dx, dy in 
                [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1), (0,0)]
            ]
            valid_candidates = []
            
            for cx, cy in candidates:
                if 0 <= cx < GRID_SIZE and 0 <= cy < GRID_SIZE:
                    # check distance to all birds - ensure safe
                    safe = True
                    for bx, by in birds:
                        # Chebyshev distance <= 1 is danger zone
                        if abs(cx - bx) <= 1 and abs(cy - by) <= 1:
                            safe = False
                            break
                    if safe:
                        valid_candidates.append((cx, cy))
            
            used_reflex = False
            if not valid_candidates:
                # No safe moves, must stay put and possibly get hit, but we prefer 0,0 relative
                next_x, next_y = drone_x, drone_y
                used_reflex = True
            else:
                # Normal target following if target is safe
                ideal_candidates = []
                base_dist = abs(tx - drone_x) + abs(ty - drone_y)
                
                # Check if greedy straight move is in valid_candidates
                best_cand = None
                best_dist = 9999
                for c in valid_candidates:
                    dist = abs(tx - c[0]) + abs(ty - c[1])
                    if dist < best_dist:
                        best_dist = dist
                        best_cand = c
                        
                next_x, next_y = best_cand
                
                # if best move isn't closing distance, it's dodging
                if best_dist >= base_dist and (next_x != drone_x or next_y != drone_y):
                    used_reflex = True

            drone_x, drone_y = next_x, next_y
            reflex_flags.append(used_reflex)

        # Reached target event
        has_pkg = target[2]
        path.append((drone_x, drone_y, has_pkg))
        birds_traj.append(list(birds))
        reflex_flags.append(False)
    
    return {
        "path": path,
        "birds_traj": birds_traj,
        "total_reward": 100.0,
        "episode": episode_index,
        "epsilon": 0.0,
        "bird_types": [random.choice([0, 1]) for _ in range(NUM_BIRDS)],
        "reflex_flags": reflex_flags,
        "actions": [''] * len(path),
        "immediate_rewards": [0.0] * len(path)
    }

def main(show_stats=False, show_replay=True, replay_speed=15):
    print("=" * 60)
    print("IAS: Dynamic Hardcoded Dodge Demo")
    print("=" * 60)
    print("Generating dynamic episodes...")
    
    rec1 = create_episode(1)
    rec2 = create_episode(2)
    
    records = [rec1, rec2]

    if show_replay:
        print("\nReplaying Hardcoded Trajectories (Pygame Visualization)")
        visualize_records(records, window_title="Dynamic Dodging Agent", speed=replay_speed)

    print("\n✓ Project Visualization Complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IAS Project: Mock Simulation")
    parser.add_argument("--stats", action="store_true", help="Ignored")
    parser.add_argument("--no-replay", action="store_true", help="Skip visualization")
    parser.add_argument("--speed", type=int, default=20, help="Playback speed in FPS")
    args = parser.parse_args()
    
    main(show_stats=args.stats, show_replay=not args.no_replay, replay_speed=args.speed)
