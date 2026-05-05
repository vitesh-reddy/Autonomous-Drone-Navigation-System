import pygame
import time
from config import GRID_SIZE, CELL, WINDOW_W, WINDOW_H, INFO_BAR, DANGER_RADIUS_CELLS, PICKUPS, DROPS
from utils import euclid


def visualize_records(records, window_title="Drone Replay (Algorithm)", speed=10):
    """
    Visualize agent trajectories using pygame.
    
    Args:
        records: List of episode records containing paths and bird trajectories
        window_title: Title for the pygame window
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(window_title)
    clock = pygame.time.Clock()

    # Load assets (from parent directory)
    try:
        grid_bg = pygame.transform.scale(pygame.image.load("./assets/grid.png").convert(), (WINDOW_W, WINDOW_W))
        drone_img = pygame.transform.scale(pygame.image.load("./assets/drone.png").convert_alpha(), (CELL, CELL))
        drone_box = pygame.transform.scale(pygame.image.load("./assets/drone_box.png").convert_alpha(), (CELL, CELL))
        pickup_im = pygame.transform.scale(pygame.image.load("./assets/pickup.png").convert_alpha(), (CELL, CELL))
        drop_im = pygame.transform.scale(pygame.image.load("./assets/drop.png").convert_alpha(), (CELL, CELL))
        bird_imgs = [
            pygame.transform.scale(pygame.image.load("./assets/bird1.png").convert_alpha(), (CELL, CELL)),
            pygame.transform.scale(pygame.image.load("./assets/bird2.png").convert_alpha(), (CELL, CELL)),
        ]
    except (pygame.error, FileNotFoundError, OSError) as e:
        print(f"\n❌ Error loading Pygame assets:")
        print(f"   {e}")
        print(f"\n   Skipping visualization (training already complete).\n")
        pygame.quit()
        return

    font = pygame.font.SysFont(None, 30)
    danger_surface = pygame.Surface((WINDOW_W, WINDOW_W), pygame.SRCALPHA)

    for rec in records:
        episode_pickups = rec.get("pickups", PICKUPS)
        episode_drops = rec.get("drops", DROPS)
        pickups_visible = [True] * len(episode_pickups)
        drops_visible = [True] * len(episode_drops)
        prev_has = 0

        path = rec["path"]
        birds_traj = rec["birds_traj"]
        total_reward = rec["total_reward"]
        episode = rec["episode"]
        epsilon = rec["epsilon"]
        types = rec["bird_types"]
        reflex_flags = rec.get("reflex_flags", [False] * len(path))
        actions = rec.get("actions", [''] * len(path))
        im_rewards = rec.get("immediate_rewards", [0.0] * len(path))

        for step_idx, state in enumerate(path):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            screen.fill((255, 255, 255))
            screen.blit(grid_bg, (0, INFO_BAR))
            pygame.draw.rect(screen, (230, 230, 230), (0, 0, WINDOW_W, INFO_BAR))

            info = font.render(
                f"{window_title} | Ep: {episode}  R:{total_reward:+.1f}  ε={epsilon:.3f}",
                True,
                (0, 0, 0)
            )
            screen.blit(info, (15, 12))

            # Draw birds
            birds_now = birds_traj[step_idx] if step_idx < len(birds_traj) else birds_traj[-1]
            for i, (bx, by) in enumerate(birds_now):
                sx_b = bx * CELL
                sy_b = WINDOW_W - (by + 1) * CELL + INFO_BAR
                t = types[i % len(types)]
                screen.blit(bird_imgs[t], (sx_b, sy_b))

            # Draw items
            for idx, p in enumerate(episode_pickups):
                if pickups_visible[idx]:
                    px, py = p
                    screen.blit(pickup_im, (px * CELL, WINDOW_W - (py + 1) * CELL + INFO_BAR))
            for idx, p in enumerate(episode_drops):
                if drops_visible[idx]:
                    dx, dy = p
                    screen.blit(drop_im, (dx * CELL, WINDOW_W - (dy + 1) * CELL + INFO_BAR))

            # Draw drone
            x, y, has_pkg = state
            sx = x * CELL
            sy = WINDOW_W - (y + 1) * CELL + INFO_BAR

            # Draw danger zone
            danger_surface.fill((0, 0, 0, 0))
            rad_pix = int(DANGER_RADIUS_CELLS * CELL)
            circle_x = sx + CELL // 2
            circle_y = sy + CELL // 2 - INFO_BAR
            pygame.draw.circle(danger_surface, (200, 0, 0, 60), (circle_x, circle_y), rad_pix, width=0)
            screen.blit(danger_surface, (0, INFO_BAR))

            # Toggle item visibility on pickup/drop
            if prev_has == 0 and has_pkg == 1:
                for idx, p in enumerate(episode_pickups):
                    if (x, y) == p and pickups_visible[idx]:
                        pickups_visible[idx] = False
                        break
            if prev_has == 1 and has_pkg == 0:
                for idx, p in enumerate(episode_drops):
                    if (x, y) == p and drops_visible[idx]:
                        drops_visible[idx] = False
                        break

            # Draw trail
            if step_idx > 0:
                px0, py0, _ = path[step_idx - 1]
                sx0 = px0 * CELL + CELL // 2
                sy0 = WINDOW_W - (py0 + 1) * CELL + INFO_BAR + CELL // 2
                sx1 = sx + CELL // 2
                sy1 = sy + CELL // 2
                if reflex_flags[step_idx]:
                    color = (255, 140, 0)  # Orange for reflex
                    width = 5
                else:
                    color = (160, 160, 160)
                    width = 3
                pygame.draw.line(screen, color, (sx0, sy0), (sx1, sy1), width)

            screen.blit(drone_box if has_pkg else drone_img, (sx, sy))
            pygame.display.flip()
            clock.tick(speed)
            prev_has = has_pkg

        time.sleep(0.9)

    time.sleep(1.0)
    pygame.quit()
