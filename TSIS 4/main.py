import pygame, sys, json, math
from game import SnakeGame
from db import *

pygame.init()


try:
    pygame.mixer.init()
    SOUND_ENABLED = True
except:
    print("Sound disabled")
    SOUND_ENABLED = False

sounds = {}
if SOUND_ENABLED:
    try:
        sounds["eat"] = pygame.mixer.Sound("eat.wav")
        sounds["power"] = pygame.mixer.Sound("power.wav")
        sounds["death"] = pygame.mixer.Sound("death.wav")
    except Exception as e:
        print("Sound load error:", e)
        SOUND_ENABLED = False


shield_channel = None


screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None,30)

def load_settings():
    try:
        return json.load(open("settings.json"))
    except:
        return {
            "theme":"default",
            "grid": True,
            "sound": True
        }

def save_settings(s):
    json.dump(s, open("settings.json","w"))

settings = load_settings()
init_db()

state="menu"
username=""
game=None


def draw_grid():
    for x in range(0, 600, 20):
        pygame.draw.line(screen, (40,40,40), (x,0), (x,400))
    for y in range(0, 400, 20):
        pygame.draw.line(screen, (40,40,40), (0,y), (600,y))

def rgb_cycle(t, speed=500):
    return (
        int((math.sin(t/speed)+1)*127),
        int((math.sin(t/(speed+200))+1)*127),
        int((math.sin(t/(speed+400))+1)*127)
    )

def get_snake_color(theme):
    if theme == "blue":
        return (0,100,255)
    elif theme == "red":
        return (255,50,50)
    elif theme in ["rgb","psychotic"]:
        return rgb_cycle(pygame.time.get_ticks())
    return (0,255,0)

def get_dynamic_color(theme, base):
    if theme == "psychotic":
        return rgb_cycle(pygame.time.get_ticks(), 300)
    return base


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if e.type == pygame.KEYDOWN:

            if state=="menu":
                if e.key==pygame.K_RETURN:
                    game=SnakeGame()
                    state="game"
                elif e.key==pygame.K_l:
                    state="leaderboard"
                elif e.key==pygame.K_s:
                    state="settings"

            elif state=="game":
                if e.key==pygame.K_UP: game.set_dir((0,-20))
                if e.key==pygame.K_DOWN: game.set_dir((0,20))
                if e.key==pygame.K_LEFT: game.set_dir((-20,0))
                if e.key==pygame.K_RIGHT: game.set_dir((20,0))

            elif state=="game_over":
                if e.key==pygame.K_RETURN:
                    username=""
                    state="name_input"

            elif state=="name_input":
                if e.key==pygame.K_RETURN and username:
                    save_score(username, game.score, game.level)
                    state="menu"
                elif e.key==pygame.K_BACKSPACE:
                    username=username[:-1]
                else:
                    if e.unicode.isalnum() and len(username) < 12:
                        username+=e.unicode

            elif state=="settings":
                if e.key==pygame.K_1: settings["theme"]="default"
                elif e.key==pygame.K_2: settings["theme"]="blue"
                elif e.key==pygame.K_3: settings["theme"]="red"
                elif e.key==pygame.K_4: settings["theme"]="rgb"
                elif e.key==pygame.K_5: settings["theme"]="psychotic"

                elif e.key==pygame.K_g:
                    settings["grid"] = not settings["grid"]

                elif e.key==pygame.K_m:
                    settings["sound"] = not settings["sound"]

                elif e.key==pygame.K_s:
                    save_settings(settings)
                    state="menu"

            elif state=="leaderboard":
                if e.key==pygame.K_ESCAPE:
                    state="menu"

    screen.fill((0,0,0))

    
    if state=="menu":
        screen.blit(font.render("ENTER - PLAY",True,(255,255,255)),(200,150))
        screen.blit(font.render("L - LEADERBOARD",True,(255,255,255)),(200,180))
        screen.blit(font.render("S - SETTINGS",True,(255,255,255)),(200,210))

    
    elif state=="game":
        if settings["grid"]:
            draw_grid()

        prev_head = game.snake[0]
        prev_foods = set(game.foods)
        prev_powers = [p["pos"] for p in game.powers]

        alive, mod = game.move()
        new_head = game.snake[0]

        
        if settings["sound"] and SOUND_ENABLED:

            
            if new_head in prev_foods:
                sounds["eat"].play()

            
            if new_head in prev_powers:
                picked_type = game.active_power

                if picked_type == "shield":
                    if shield_channel:
                        shield_channel.stop()

                    shield_channel = pygame.mixer.find_channel()
                    if shield_channel:
                        shield_channel.play(sounds["power"], loops=-1)
                else:
                    sounds["power"].play()

        
        if shield_channel and game.active_power != "shield":
            shield_channel.stop()
            shield_channel = None

        if not alive:
            if settings["sound"] and SOUND_ENABLED:
                sounds["death"].play()
            state="game_over"

        clock.tick(int(10 * mod))

        theme = settings["theme"]

        
        for s in game.snake:
            pygame.draw.rect(screen, get_snake_color(theme), (*s,20,20))

        
        for food in game.foods:
            pygame.draw.rect(screen,
                get_dynamic_color(theme,(255,0,0)),
                (*food,20,20)
            )

        
        for poison in game.poisons:
            pygame.draw.rect(screen,
                get_dynamic_color(theme,(150,0,0)),
                (*poison,20,20)
            )

        
        power_colors = {
            "speed": (0,255,0),
            "slow": (0,0,255),
            "shield": (255,255,0)
        }

        for p in game.powers:
            pygame.draw.rect(
                screen,
                get_dynamic_color(theme, power_colors[p["type"]]),
                (*p["pos"],20,20)
            )

        
        for o in game.obstacles:
            pygame.draw.rect(screen,
                get_dynamic_color(theme,(100,100,100)),
                (*o,20,20)
            )

        
        screen.blit(font.render(f"Score: {game.score}",True,(255,255,255)),(10,10))
        screen.blit(font.render(f"Level: {game.level}",True,(255,255,255)),(10,30))

        if game.active_power:
            screen.blit(font.render(f"Power: {game.active_power}",True,(0,255,255)),(10,60))

    
    elif state=="game_over":
        screen.blit(font.render("GAME OVER",True,(255,0,0)),(200,150))
        screen.blit(font.render("ENTER - CONTINUE",True,(255,255,255)),(180,200))

    
    elif state=="name_input":
        screen.blit(font.render("ENTER NAME:",True,(255,255,255)),(200,150))
        screen.blit(font.render(username,True,(255,255,0)),(200,180))

    
    elif state=="settings":
        theme = settings["theme"]

        screen.blit(font.render("SETTINGS",True,(255,255,255)),(230,80))
        screen.blit(font.render(f"Theme: {theme}",True,(255,255,0)),(200,120))

        screen.blit(font.render("1-default 2-blue 3-red 4-rgb 5-psychotic",True,(255,255,255)),(40,160))

        screen.blit(font.render(f"Grid: {settings['grid']} (G)",True,(255,255,255)),(200,200))
        screen.blit(font.render(f"Sound: {settings['sound']} (M)",True,(255,255,255)),(200,230))

        screen.blit(font.render("S - save & back",True,(255,255,255)),(200,260))

        preview_color = get_snake_color(theme)
        pygame.draw.rect(screen, (255,255,255), (260, 300, 80, 30), 2)
        pygame.draw.rect(screen, preview_color, (262, 302, 76, 26))

    
    elif state=="leaderboard":
        data = get_top()
        y=100
        for i,row in enumerate(data):
            name,score,lvl,date = row
            txt=f"{i+1}. {name} {score} L{lvl}"
            screen.blit(font.render(txt,True,(255,255,255)),(140,y))

            date_txt = date.strftime("%d-%m %H:%M")
            screen.blit(font.render(date_txt,True,(150,150,150)),(350,y))

            y+=30

    pygame.display.flip()