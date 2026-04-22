import pygame
import math
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint: R-rect | C-circle | S-square | T-right triangle | Y-equilateral | H-rhombus")
    clock = pygame.time.Clock()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    radius = 3
    drawing_mode = 'brush'
    active_color = BLUE
    canvas = pygame.Surface((800, 600))
    canvas.fill(BLACK)
    start_pos = None
    is_drawing = False
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: drawing_mode = 'rect'
                elif event.key == pygame.K_c: drawing_mode = 'circle'
                elif event.key == pygame.K_b: drawing_mode = 'brush'
                elif event.key == pygame.K_e: drawing_mode = 'eraser'
                elif event.key == pygame.K_s: drawing_mode = 'square'
                elif event.key == pygame.K_t: drawing_mode = 'right_triangle'
                elif event.key == pygame.K_y: drawing_mode = 'equilateral_triangle'
                elif event.key == pygame.K_h: drawing_mode = 'rhombus'
                elif event.key == pygame.K_1: active_color = RED
                elif event.key == pygame.K_2: active_color = GREEN
                elif event.key == pygame.K_3: active_color = BLUE
                elif event.key == pygame.K_4: active_color = WHITE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_drawing = True
                    start_pos = event.pos
                elif event.button == 4: 
                    radius = min(100, radius + 1)
                elif event.button == 5:
                    radius = max(1, radius - 1)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if drawing_mode == 'rect':
                        draw_rect(canvas, start_pos, mouse_pos, active_color, radius)
                    elif drawing_mode == 'circle':
                        draw_circle(canvas, start_pos, mouse_pos, active_color, radius)
                    elif drawing_mode == 'square':
                        draw_square(canvas, start_pos, mouse_pos, active_color, radius)
                    elif drawing_mode == 'right_triangle':
                        draw_right_triangle(canvas, start_pos, mouse_pos, active_color, radius)
                    elif drawing_mode == 'equilateral_triangle':
                        draw_equilateral_triangle(canvas, start_pos, mouse_pos, active_color, radius)
                    elif drawing_mode == 'rhombus':
                        draw_rhombus(canvas, start_pos, mouse_pos, active_color, radius)
                    is_drawing = False
                    start_pos = None
        if is_drawing:
            if drawing_mode == 'brush':
                pygame.draw.circle(canvas, active_color, mouse_pos, radius)
            elif drawing_mode == 'eraser':
                pygame.draw.circle(canvas, BLACK, mouse_pos, radius)
        screen.fill(BLACK)
        screen.blit(canvas, (0, 0))
        if is_drawing and start_pos:
            if drawing_mode == 'rect':
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
        pygame.draw.circle(screen, active_color if drawing_mode != 'eraser' else WHITE, mouse_pos, radius, 1)
        pygame.display.flip()
        clock.tick(60)
def draw_rect(surf, start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
    pygame.draw.rect(surf, color, rect, thickness)
def draw_circle(surf, start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    radius = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
    pygame.draw.circle(surf, color, start, radius, thickness)
def draw_square(surf, start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2-x1), abs(y2-y1))
    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(surf, color, rect, thickness)
def draw_right_triangle(surf, start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surf, color, points, thickness)
def draw_equilateral_triangle(surf, start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)
    height = int((math.sqrt(3) / 2) * side)
    p1 = (x1, y1)
    p2 = (x1 + side, y1)
    p3 = (x1 + side // 2, y1 - height)
    pygame.draw.polygon(surf, color, [p1, p2, p3], thickness)
def draw_rhombus(surf, start, end, color, thickness):
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
if __name__ == "__main__":
    main()