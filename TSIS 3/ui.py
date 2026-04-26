import pygame

def draw_text(screen, text, font, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

def menu(screen, font, small_font):
    screen.fill((0,0,0))
    draw_text(screen, "RACER", font, (255,255,255), 120, 100)
    draw_text(screen, "ENTER - Play", small_font, (255,255,255), 120, 250)
    draw_text(screen, "L - Leaderboard", small_font, (255,255,255), 120, 300)
    draw_text(screen, "S - Settings", small_font, (255,255,255), 120, 350)
    draw_text(screen, "ESC - Quit", small_font, (255,255,255), 120, 400)

def game_over(screen, font, small_font, score, distance):
    screen.fill((200,0,0))
    draw_text(screen, "GAME OVER", font, (255,255,255), 50, 150)
    draw_text(screen, f"Score: {score}", small_font, (255,255,255), 120, 300)
    draw_text(screen, f"Distance: {distance}", small_font, (255,255,255), 120, 330)
    draw_text(screen, "R - Retry", small_font, (255,255,255), 120, 380)
    draw_text(screen, "M - Menu", small_font, (255,255,255), 120, 410)

def leaderboard(screen, small_font, data):
    screen.fill((0,0,0))
    y = 100
    for i, entry in enumerate(data):
        draw_text(screen, f"{i+1}. {entry['name']} - {entry['score']}", small_font, (255,255,255), 60, y)
        y += 30
    draw_text(screen, "ESC - Back", small_font, (255,255,255), 120, 520)

def draw_settings(screen, small_font, settings):
    screen.fill((0,0,0))
    draw_text(screen, "SETTINGS", small_font, (255,255,255), 120, 100)
    draw_text(screen, "1/2/3 Difficulty", small_font, (255,255,255), 80, 200)
    draw_text(screen, "C - Change Car", small_font, (255,255,255), 80, 240)
    draw_text(screen, "M - Sound", small_font, (255,255,255), 80, 280)
    draw_text(screen, f"Car: {settings['car']}", small_font, (255,255,0), 80, 320)
    draw_text(screen, f"Sound: {settings['sound']}", small_font, (255,255,0), 80, 350)
    draw_text(screen, f"Difficulty: {settings['difficulty']}", small_font, (255,255,0), 80, 380)