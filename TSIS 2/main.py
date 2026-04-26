import pygame
import math
import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

active_color = BLUE

radius = 2
drawing_mode = 'brush'

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BLACK)

start_pos = None
prev_pos = None
is_drawing = False

font = pygame.font.SysFont(None, 30)
typing = False
text_input = ""

def create_button(x, y, w, h, text, action):
    return {"rect": pygame.Rect(x,y,w,h), "text": text, "action": action}

font_small = pygame.font.SysFont(None, 20)

buttons = [
    create_button(10,10,60,30,"Brush","brush"),
    create_button(80,10,60,30,"Line","line"),
    create_button(150,10,60,30,"Rect","rect"),
    create_button(220,10,60,30,"Circle","circle"),
    create_button(10,50,60,30,"Sq","square"),
    create_button(80,50,60,30,"TriR","right_triangle"),
    create_button(150,50,60,30,"TriE","equilateral_triangle"),
    create_button(220,50,60,30,"Rhomb","rhombus"),
    create_button(290,10,60,30,"Fill","fill"),
    create_button(360,10,60,30,"Text","text"),

    create_button(450,10,40,30,"R","red"),
    create_button(500,10,40,30,"G","green"),
    create_button(550,10,40,30,"B","blue"),
    create_button(600,10,40,30,"W","white"),

    create_button(650,10,40,30,"S","small"),
    create_button(700,10,40,30,"M","medium"),
    create_button(750,10,40,30,"L","large"),
]

def flood_fill(surface, x, y, new_color):
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return
    target_color = surface.get_at((x,y))
    if target_color == new_color:
        return
    stack = [(x,y)]
    visited = set()

    while stack:
        x,y = stack.pop()

        if (x,y) in visited:
            continue
        visited.add((x,y))

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            continue

        if surface.get_at((x,y)) != target_color:
            continue

        surface.set_at((x,y), new_color)

        stack.append((x-1,y))
        stack.append((x+1,y))
        stack.append((x,y-1))
        stack.append((x,y+1))

def draw_rect(surf, start, end, color, thickness):
    if start is None or end is None:
        return

    rect = pygame.Rect(min(start[0],end[0]), min(start[1],end[1]),
                       abs(end[0]-start[0]), abs(end[1]-start[1]))
    pygame.draw.rect(surf, color, rect, thickness)

def draw_circle(surf, start, end, color, thickness):
    if start is None or end is None:
        return

    r = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5)
    pygame.draw.circle(surf, color, start, r, thickness)

def draw_square(surf, start, end, color, thickness):
    if start is None or end is None:
        return
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2-x1), abs(y2-y1))
    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(surf, color, rect, thickness)

def draw_right_triangle(surf, start, end, color, thickness):
    if start is None or end is None:
        return
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surf, color, points, thickness)

def draw_equilateral_triangle(surf, start, end, color, thickness):
    if start is None or end is None:
        return
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)
    height = int((math.sqrt(3) / 2) * side)
    p1 = (x1, y1)
    p2 = (x1 + side, y1)
    p3 = (x1 + side // 2, y1 - height)
    pygame.draw.polygon(surf, color, [p1, p2, p3], thickness)

def draw_rhombus(surf, start, end, color, thickness):
    if start is None or end is None:
        return
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    points = [
        (cx, y1),
        (x2, cy),
        (cx, y2),
        (x1, cy)
    ]
    pygame.draw.polygon(surf, color, points, thickness)

running = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_b: drawing_mode = 'brush'
            elif event.key == pygame.K_l: drawing_mode = 'line'
            elif event.key == pygame.K_r: drawing_mode = 'rect'
            elif event.key == pygame.K_c: drawing_mode = 'circle'
            elif event.key == pygame.K_f: drawing_mode = 'fill'
            elif event.key == pygame.K_x: drawing_mode = 'text'
            elif event.key == pygame.K_e: drawing_mode = 'eraser'

            elif event.key == pygame.K_1: radius = 2
            elif event.key == pygame.K_2: radius = 5
            elif event.key == pygame.K_3: radius = 10
            elif event.key == pygame.K_4: radius = 100

            elif event.key == pygame.K_q: active_color = RED
            elif event.key == pygame.K_w: active_color = GREEN
            elif event.key == pygame.K_a: active_color = BLUE
            elif event.key == pygame.K_d: active_color = WHITE

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)
                print("Saved:", filename)

            if typing:
                if event.key == pygame.K_RETURN:
                    img = font.render(text_input, True, active_color)
                    canvas.blit(img, mouse_pos)
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    if hasattr(event, "unicode") and event.unicode:
                        text_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:

            clicked_toolbar = False

            for b in buttons:
                if b["rect"].collidepoint(event.pos):
                    clicked_toolbar = True
                    action = b["action"]

                    if action in ["brush","line","rect","circle","fill","text",
                                "square","right_triangle","equilateral_triangle","rhombus"]:
                        drawing_mode = action
                    elif action == "red": active_color = RED
                    elif action == "green": active_color = GREEN
                    elif action == "blue": active_color = BLUE
                    elif action == "white": active_color = WHITE
                    elif action == "small": radius = 2
                    elif action == "medium": radius = 5
                    elif action == "large": radius = 10
                    break

            if clicked_toolbar:
                start_pos = None
                is_drawing = False
                continue

            if event.pos[1] < 50:
                continue

            if event.button == 1:
                start_pos = event.pos
                prev_pos = event.pos
                is_drawing = True

                if drawing_mode == 'fill':
                    flood_fill(canvas, *event.pos, active_color)

                elif drawing_mode == 'text':
                    typing = True
                    text_input = ""

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if drawing_mode == 'line' and start_pos is not None:
                    pygame.draw.line(canvas, active_color, start_pos, mouse_pos, radius)
                elif drawing_mode == 'rect' and start_pos is not None:
                    draw_rect(canvas, start_pos, mouse_pos, active_color, radius)
                elif drawing_mode == 'circle' and start_pos is not None:
                    draw_circle(canvas, start_pos, mouse_pos, active_color, radius)
                elif drawing_mode == 'square' and start_pos is not None:
                    draw_square(canvas, start_pos, mouse_pos, active_color, radius)
                elif drawing_mode == 'right_triangle' and start_pos is not None:
                    draw_right_triangle(canvas, start_pos, mouse_pos, active_color, radius)
                elif drawing_mode == 'equilateral_triangle' and start_pos is not None:
                    draw_equilateral_triangle(canvas, start_pos, mouse_pos, active_color, radius)
                elif drawing_mode == 'rhombus' and start_pos is not None:
                    draw_rhombus(canvas, start_pos, mouse_pos, active_color, radius)
                start_pos = None
                prev_pos = None
                is_drawing = False

    if is_drawing and mouse_pos[1] >= 50:
        if drawing_mode == 'brush':
            if prev_pos:
                pygame.draw.line(canvas, active_color, prev_pos, mouse_pos, radius)
            prev_pos = mouse_pos

        elif drawing_mode == 'eraser':
            pygame.draw.circle(canvas, BLACK, mouse_pos, radius)

    screen.fill(BLACK)
    screen.blit(canvas, (0,0))

    if is_drawing and start_pos is not None:
        if drawing_mode == 'line':
            pygame.draw.line(screen, active_color, start_pos, mouse_pos, radius)
        elif drawing_mode == 'rect':
            draw_rect(screen, start_pos, mouse_pos, active_color, radius)
        elif drawing_mode == 'circle':
            draw_circle(screen, start_pos, mouse_pos, active_color, radius)
        elif drawing_mode == 'square':
            draw_square(screen, start_pos, mouse_pos, active_color, radius)
        elif drawing_mode == 'right_triangle':
            draw_right_triangle(screen, start_pos, mouse_pos, active_color, radius)
        elif drawing_mode == 'equilateral_triangle':
            draw_equilateral_triangle(screen, start_pos, mouse_pos, active_color, radius)
        elif drawing_mode == 'rhombus':
            draw_rhombus(screen, start_pos, mouse_pos, active_color, radius)

    if typing:
        img = font.render(text_input, True, active_color)
        screen.blit(img, mouse_pos)

    for b in buttons:
        color = (80,80,80) if b["action"] == drawing_mode else (50,50,50)
        pygame.draw.rect(screen, color, b["rect"])
        pygame.draw.rect(screen, WHITE, b["rect"], 2)
        txt = font_small.render(b["text"], True, WHITE)
        screen.blit(txt, (b["rect"].x+5, b["rect"].y+8))

    pygame.draw.circle(screen, active_color, mouse_pos, radius, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()