import pygame, sys, random, math
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


ENEMY_MAX = 2
OBSTACLE_MAX = 2
COIN_MAX = 2
POWER_MAX = 1

ENEMY_SPAWN_DELAY = 1500
OBSTACLE_SPAWN_DELAY = 3000
COIN_SPAWN_DELAY = 2000
POWER_SPAWN_DELAY = 5000

ROAD_OFFSET = 40


SPEED_SCALE = 0.002   
MAX_SPEED = 12

state = "menu"
settings = load_settings()

def apply_sound():
    volume = 1 if settings.get("sound", True) else 0
    coin_sound.set_volume(volume)
    crash_sound.set_volume(volume)


def is_position_free(new_rect):
    for group in [enemies, obstacles, coins_list, powers]:
        for obj in group:
            if new_rect.colliderect(obj.rect):
                return False

    if new_rect.colliderect(player.rect):
        return False

    return True


def safe_spawn(create_func, max_attempts=10):
    for _ in range(max_attempts):
        obj = create_func()

        obj.rect.x = max(ROAD_OFFSET,
                         min(obj.rect.x, 400 - ROAD_OFFSET - obj.rect.width))

        if is_position_free(obj.rect):
            return obj

    return None



def spawn_enemy():
    def create():
        e = Enemy()
        e.reset(player.rect.centerx)
        return e

    obj = safe_spawn(create)
    if obj:
        enemies.append(obj)


def spawn_obstacle():
    obj = safe_spawn(lambda: Obstacle())
    if obj:
        obstacles.append(obj)


def spawn_coin():
    obj = safe_spawn(lambda: Coin())
    if obj:
        coins_list.append(obj)


def spawn_power():
    obj = safe_spawn(lambda: PowerUp())
    if obj:
        powers.append(obj)



def reset_game():
    global player, enemies, obstacles, coins_list, powers
    global speed, base_speed, score, coins, distance
    global active_power, power_timer
    global last_enemy_spawn, last_obstacle_spawn, last_coin_spawn, last_power_spawn

    player = Player(settings.get("car", "default"))

    enemies = []
    obstacles = []
    coins_list = []
    powers = []

    base_speed = 4
    speed = base_speed

    score = 0
    coins = 0
    distance = 0

    active_power = None
    power_timer = 0

    last_enemy_spawn = 0
    last_obstacle_spawn = 0
    last_coin_spawn = 0
    last_power_spawn = 0

    apply_sound()


reset_game()
username = ""


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:

            if state == "menu":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    state = "game"
                elif event.key == pygame.K_l:
                    state = "leaderboard"
                elif event.key == pygame.K_s:
                    state = "settings"

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
                    save_score(username, score, distance)
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

        
        player.rect.x = max(ROAD_OFFSET,
                            min(player.rect.x, 400 - ROAD_OFFSET - player.rect.width))

        now = pygame.time.get_ticks()

        
        if len(enemies) < ENEMY_MAX and now - last_enemy_spawn > ENEMY_SPAWN_DELAY:
            spawn_enemy()
            last_enemy_spawn = now

        if len(obstacles) < OBSTACLE_MAX and now - last_obstacle_spawn > OBSTACLE_SPAWN_DELAY:
            spawn_obstacle()
            last_obstacle_spawn = now

        if len(coins_list) < COIN_MAX and now - last_coin_spawn > COIN_SPAWN_DELAY:
            spawn_coin()
            last_coin_spawn = now

        if len(powers) < POWER_MAX and now - last_power_spawn > POWER_SPAWN_DELAY:
            spawn_power()
            last_power_spawn = now

        
        for e in enemies:
            e.move(speed)
        for o in obstacles:
            o.move(speed)
        for c in coins_list:
            c.move(speed)
        for p in powers:
            p.move(speed)

        
        enemies = [e for e in enemies if e.rect.y < 600]
        obstacles = [o for o in obstacles if o.rect.y < 600]
        coins_list = [c for c in coins_list if c.rect.y < 600]
        powers = [p for p in powers if p.rect.y < 600]

        
        distance += 1
        score = coins * 50 + distance

        
        speed = min(base_speed + score * SPEED_SCALE, MAX_SPEED)

        
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

        for c in coins_list[:]:
            if player.rect.colliderect(c.rect):
                coin_sound.play()
                coins += 1
                coins_list.remove(c)

        for p in powers[:]:
            if player.rect.colliderect(p.rect):
                if active_power is None:
                    active_power = p.type
                    power_timer = pygame.time.get_ticks()
                powers.remove(p)

        
        if active_power == "nitro":
            if pygame.time.get_ticks() - power_timer < 4000:
                speed = MAX_SPEED
            else:
                active_power = None

        elif active_power == "repair":
            obstacles.clear()
            active_power = None

        
        screen.blit(player.image, player.rect)

        for e in enemies:
            screen.blit(e.image, e.rect)
        for o in obstacles:
            screen.blit(o.image, o.rect)
        for c in coins_list:
            screen.blit(c.image, c.rect)
        for p in powers:
            screen.blit(p.image, p.rect)

        pygame.draw.rect(screen, (255,255,255), (0,0,ROAD_OFFSET,600))
        pygame.draw.rect(screen, (255,255,255), (400-ROAD_OFFSET,0,ROAD_OFFSET,600))

        draw_text(screen, f"Score: {score}", small_font, WHITE, 10, 10)
        draw_text(screen, f"Coins: {coins}", small_font, WHITE, 10, 40)
        draw_text(screen, f"Speed: {round(speed,1)}", small_font, WHITE, 10, 70)

    elif state == "menu":
        menu(screen, font, small_font)

    elif state == "settings":
        draw_settings(screen, small_font, settings)

    elif state == "game_over":
        game_over(screen, font, small_font, score, distance)

    elif state == "name_input":
        draw_text(screen, "ENTER NAME:", small_font, WHITE, 50, 225)
        draw_text(screen, username, small_font, (255,255,0), 50, 250)

    elif state == "leaderboard":
        leaderboard(screen, small_font, load_leaderboard())

    pygame.display.update()
    clock.tick(60)