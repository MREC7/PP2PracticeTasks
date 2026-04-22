import pygame
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint: [R]ect, [C]ircle, [B]rush, [E]raser, [1]red, [2]green, [3]blue, [4]white")
    clock = pygame.time.Clock()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    radius = 15
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
        pygame.draw.circle(screen, active_color if drawing_mode != 'eraser' else WHITE, mouse_pos, radius, 1)
        pygame.display.flip()
        clock.tick(60)
def draw_rect(surf, start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    top_left = (min(x1, x2), min(y1, y2))
    pygame.draw.rect(surf, color, (top_left[0], top_left[1], width, height), thickness)
def draw_circle(surf, start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    rad = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
    pygame.draw.circle(surf, color, start, rad, thickness)
if __name__ == "__main__":
    main()