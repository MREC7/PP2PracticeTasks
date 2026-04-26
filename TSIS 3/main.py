import pygame, sys, random
from racer import *
from ui import *
from persistence import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 50)
small_font = pygame.font.SysFont("Verdana", 20)

background = pygame.image.load("AnimatedStreet.png")
coin_sound = pygame.mixer.Sound("coinsound.mp3")
crash_sound = pygame.mixer.Sound("crash.wav")

WHITE = (255,255,255)

state = "menu"
settings = load_settings()

if "car" not in settings:
    settings["car"] = "default"
if "sound" not in settings:
    settings["sound"] = True
if "difficulty" not in settings:
    settings["difficulty"] = "normal"


def apply_sound():
    volume = 1 if settings["sound"] else 0
    coin_sound.set_volume(volume)
    crash_sound.set_volume(volume)


def reset_game():
    global player, enemies, obstacles, coin, power
    global speed, base_speed, score, coins, distance
    global active_power, power_timer

    player = Player(settings["car"])

    enemies = [Enemy() for _ in range(3)]
    for e in enemies:
        e.reset(player.rect.centerx)

    obstacles = [Obstacle() for _ in range(2)]

    coin = Coin()
    power = PowerUp()

    base_speed = 5
    speed = base_speed

    score = 0
    coins = 0
    distance = 0

    active_power = None
    power_timer = 0

    if settings["difficulty"] == "easy":
        speed = base_speed = 3
    elif settings["difficulty"] == "hard":
        speed = base_speed = 8

    apply_sound()


reset_game()

username = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if state == "menu":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    state = "game"
                elif event.key == pygame.K_l:
                    state = "leaderboard"
                elif event.key == pygame.K_s:
                    state = "settings"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif state == "settings":
                if event.key == pygame.K_1:
                    settings["difficulty"] = "easy"
                elif event.key == pygame.K_2:
                    settings["difficulty"] = "normal"
                elif event.key == pygame.K_3:
                    settings["difficulty"] = "hard"

                elif event.key == pygame.K_c:
                    settings["car"] = "alt" if settings["car"] == "default" else "default"
                    player.set_skin(settings["car"])

                elif event.key == pygame.K_m:
                    settings["sound"] = not settings["sound"]
                    apply_sound()

                elif event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    state = "menu"

            elif state == "game_over":
                username = ""
                state = "name_input"

            elif state == "name_input":
                if event.key == pygame.K_RETURN and username:
                    final_score = score + coins * 5 + distance // 10
                    save_score(username, final_score, distance)
                    state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if event.unicode.isalnum() and len(username) < 10:
                        username += event.unicode

            elif state == "leaderboard":
                if event.key == pygame.K_ESCAPE:
                    state = "menu"

    if state == "game":
        screen.blit(background, (0,0))

        player.move()

        for e in enemies:
            e.move(speed)

        for o in obstacles:
            o.move(speed)

        coin.move(speed)
        power.move(speed)

        if power.is_expired():
            power.spawn()

        distance += 1

        if distance % 300 == 0:
            new_enemy = Enemy()
            new_enemy.reset(player.rect.centerx)
            enemies.append(new_enemy)
            speed += 0.5

        if distance % 800 == 0:
            obstacles.append(Obstacle())

        for e in enemies:
            if player.rect.colliderect(e.rect):
                if active_power == "shield":
                    active_power = None
                    e.reset(player.rect.centerx)
                else:
                    crash_sound.play()
                    state = "game_over"

        for o in obstacles:
            if player.rect.colliderect(o.rect):
                if o.type == "oil":
                    player.rect.x += random.choice([-50, 50])
                else:
                    state = "game_over"

        if player.rect.colliderect(coin.rect):
            coin_sound.play()
            coins += 1
            score += 5
            coin.spawn()

        if player.rect.colliderect(power.rect):
            if active_power is None:
                active_power = power.type
                power_timer = pygame.time.get_ticks()
            power.spawn()

        if active_power == "nitro":
            if pygame.time.get_ticks() - power_timer < 4000:
                speed = 10
            else:
                active_power = None
                speed = base_speed

        elif active_power == "repair":
            obstacles.clear()
            active_power = None

        screen.blit(player.image, player.rect)

        for e in enemies:
            screen.blit(e.image, e.rect)

        for o in obstacles:
            screen.blit(o.image, o.rect)

        screen.blit(coin.image, coin.rect)
        screen.blit(power.image, power.rect)

        draw_text(screen, f"Score: {score}", small_font, WHITE, 10, 10)
        draw_text(screen, f"Coins: {coins}", small_font, WHITE, 10, 40)
        draw_text(screen, f"Distance: {distance}", small_font, WHITE, 10, 70)

    elif state == "menu":
        menu(screen, font, small_font)

    elif state == "settings":
        draw_settings(screen, small_font, settings)

    elif state == "game_over":
        game_over(screen, font, small_font, score, distance)

    elif state == "name_input":
        draw_text(screen, "ENTER NAME:", small_font, WHITE, 100, 250)
        draw_text(screen, username, small_font, (255,255,0), 100, 250)

    elif state == "leaderboard":
        leaderboard(screen, small_font, load_leaderboard())

    pygame.display.update()
    clock.tick(60)