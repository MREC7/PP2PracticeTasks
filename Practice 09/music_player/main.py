import pygame
from player import MusicPlayer
pygame.init()
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont("Arial", 24)
player = MusicPlayer("music")
clock = pygame.time.Clock()
running = True
def draw():
    screen.fill((20, 20, 20))
    track_text = font.render(
        f"Track: {player.get_current_track_name()}",
        True,
        (255, 255, 255)
    )
    state_text = font.render(
        f"State: {player.state}",
        True,
        (180, 180, 180)
    )
    progress_text = font.render(
        f"Time: {player.get_progress()} sec",
        True,
        (100, 200, 255)
    )
    screen.blit(track_text, (20, 40))
    screen.blit(state_text, (20, 80))
    screen.blit(progress_text, (20, 120))
    controls = [
        "P - Play",
        "S - Stop",
        "N - Next",
        "B - Previous",
        "Q - Quit"
    ]
    for i, text in enumerate(controls):
        t = font.render(text, True, (200, 200, 200))
        screen.blit(t, (350, 40 + i * 30))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.previous()
            elif event.key == pygame.K_q:
                running = False
    draw()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()