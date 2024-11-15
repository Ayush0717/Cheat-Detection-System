import pygame
import math
import random
import socket
import threading

# Initialize Pygame
pygame.init()

# Game Settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player Settings
player_size = 50
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
player_life = 3

# Bullet Settings
bullets = []
bullet_speed = 10
bullet_radius = 5
damage = 1  # Initial bullet damage

# Enemy Settings
enemies = []
enemy_size = 40
enemy_spawn_time = 1500  # in milliseconds
last_enemy_spawn = pygame.time.get_ticks()
enemy_speed_decrement = 1  # Decrease enemy speed after each game

# Game Over, Score, and Restart settings
game_over = False
restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)
score = 0
best_score = 0

# Load Images
player_image = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
pygame.draw.polygon(player_image, GREEN, [(25, 0), (50, 50), (0, 50)])

# Function to draw text
def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Function to send data to the cheat detection system
def send_data_to_cheat_system(player_x, player_y, bullet_count):
    server_ip = "127.0.0.1"
    server_port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    
    # Send player position and bullet count
    data = f"{player_x},{player_y},{bullet_count}"
    sock.send(data.encode("utf-8"))
    
    # Receive response from cheat detection system
    response = sock.recv(1024).decode("utf-8")
    print(f"Cheat Detection Response: {response}")
    
    sock.close()

# Main Game Loop
running = True
while running:
    screen.fill(BLACK)

    # Handle game over state
    if game_over:
        handle_game_over()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    reset_game()
        continue

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if player_x + player_size < WIDTH:
            player_x += player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if player_y > 0:
            player_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if player_y + player_size < HEIGHT:
            player_y += player_speed

    # Get mouse position and rotate player image
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2))) + 90
    rotated_player = pygame.transform.rotate(player_image, angle_to_mouse)
    screen.blit(rotated_player, (player_x, player_y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Continuous bullet firing (right click to fire continuously)
    if pygame.mouse.get_pressed()[0]:
        bullets.append(Bullet(player_x + player_size // 2, player_y + player_size // 2, mouse_x, mouse_y, damage))

    # Update and draw bullets
    for bullet in bullets:
        bullet.update()
        bullet.draw()

    # Send data to cheat detection system
    send_data_to_cheat_system(player_x, player_y, len(bullets))

    # Update and draw enemies
    for enemy in enemies:
        enemy.update()
        enemy.draw()

    # Display score and life
    font = pygame.font.SysFont(None, 36)
    draw_text(f'Score: {score}', font, WHITE, 10, 10)
    draw_text(f'Lives: {player_life}', font, WHITE, WIDTH - 100, 10)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sdfsvv