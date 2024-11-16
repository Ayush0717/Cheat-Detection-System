import pygame
import math
import random
import os
import psutil
import time

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
FPS = 40

# Player Settings
player_name = ""
player_size = 100
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10  # Fixed y-position at the bottom
player_speed = 7
player_life = 3

# Bullet Settings
bullets = []
bullet_speed = 10
bullet_radius = 5
damage = 1
bullet_interval = 200

# Enemy Settings
enemies = []
enemy_size = 40
initial_enemy_speed = 3
enemy_spawn_time = 1500
last_enemy_spawn = pygame.time.get_ticks()
enemy_speed = initial_enemy_speed

# Game Over, Score, and Restart Settings
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

# Function to capture player name
def get_player_name():
    global player_name
    input_active = True
    font = pygame.font.SysFont(None, 36)
    player_name = ""

    while input_active:
        screen.fill(BLACK)
        draw_text("Enter Your Name: " + player_name, font, WHITE, WIDTH // 2 - 200, HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to confirm
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Press Backspace to delete
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

# Class for bullets
class Bullet:
    def __init__(self, x, y, target_x, target_y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * bullet_speed
        self.dy = math.sin(angle) * bullet_speed

    def update(self):
        self.x += self.dx
        self.y += self.dy
        return not (0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), bullet_radius)

    def check_collision(self, enemy):
        # Check for collision with an enemy
        bullet_rect = pygame.Rect(self.x - bullet_radius, self.y - bullet_radius, bullet_radius * 2, bullet_radius * 2)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy_size, enemy_size)
        return bullet_rect.colliderect(enemy_rect)

# Class for enemies
class Enemy:
    def __init__(self, speed):  # Fixed init method
        self.x = random.randint(0, WIDTH - enemy_size)
        self.y = -enemy_size
        self.speed = speed
        self.health = 3

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            global player_life, game_over
            player_life = max(player_life - 1, 0)
            enemies.remove(self)
            if player_life == 0:
                game_over = True

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, enemy_size, enemy_size))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, (self.health / 3) * enemy_size, 5))

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            enemies.remove(self)
            global score
            score += 10
            global enemy_speed
            enemy_speed = min(initial_enemy_speed + (score // 50), 10)

# Function to handle game over
def handle_game_over():
    global game_over, best_score
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render('GAME OVER', True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(game_over_text, text_rect)
    pygame.draw.rect(screen, BLUE, restart_button_rect)
    font = pygame.font.SysFont(None, 36)
    restart_text = font.render('Restart', True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    screen.blit(restart_text, restart_rect)
    draw_text(f'Best Score: {best_score}', font, WHITE, WIDTH // 2 - 70, HEIGHT // 2 - 100)

# Function to reset the game
def reset_game():
    global player_x, player_y, player_life, bullets, enemies, game_over, score, best_score, enemy_speed
    player_x = WIDTH // 2
    player_y = HEIGHT - player_size - 10  # Reset to fixed y-position
    player_life = 50
    bullets = []
    enemies = []
    if score > best_score:
        best_score = score
    score = 0
    enemy_speed = initial_enemy_speed
    game_over = False
    get_player_name()

# Function to detect cheating (example of memory manipulation, suspicious processes, etc.)
def detect_cheat():
    # Check for memory manipulation by looking for abnormal memory usage
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    if memory_info.rss > 100 * 1024 * 1024:  # Example threshold for memory
        print("Illegal access detected: Excessive memory usage")
        return True  # Cheating detected
    
    # Check for suspicious processes running alongside (e.g., cheat engine)
    for proc in psutil.process_iter(['pid', 'name']):
        if 'cheat' in proc.info['name'].lower() or 'x64' in proc.info['name'].lower():  # Common cheat engine names
            print(f"Illegal access detected: Suspicious process {proc.info['name']} (PID: {proc.info['pid']})")
            return True  # Cheating detected

    return False  # No cheating detected

# Timing for Bullet Fire
last_bullet_time = 0

# Function to check collision between player and enemies
def check_collision(player_x, player_y, enemy):
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy_size, enemy_size)
    return player_rect.colliderect(enemy_rect)

# Main Game Loop
get_player_name()  # Prompt player for name before starting the game

running = True
while running:
    screen.fill(BLACK)

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

    if detect_cheat():  # Will print message but not stop the game
        continue  # The game continues even if cheating is detected

    keys = pygame.key.get_pressed()
    # Movement logic
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if player_x + player_size < WIDTH:
            player_x += player_speed

    # Always keep the player's y-position fixed
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2)))
    rotated_player = pygame.transform.rotate(player_image, angle_to_mouse)
    rotated_rect = rotated_player.get_rect(center=(player_x + player_size // 2, player_y + player_size // 2))
    screen.blit(rotated_player, rotated_rect)

    # Bullet firing
    if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_bullet_time > bullet_interval:
        last_bullet_time = pygame.time.get_ticks()
        bullets.append(Bullet(player_x + player_size // 2, player_y, mouse_x, mouse_y, damage))

    for bullet in bullets[:]:
        if bullet.update():
            bullets.remove(bullet)
        else:
            bullet.draw()

        for enemy in enemies[:]:
            if bullet.check_collision(enemy):
                enemy.hit(bullet.damage)
                bullets.remove(bullet)
                break

    # Spawn new enemies
    if pygame.time.get_ticks() - last_enemy_spawn > enemy_spawn_time:
        last_enemy_spawn = pygame.time.get_ticks()
        enemies.append(Enemy(enemy_speed))

    for enemy in enemies[:]:
        enemy.update()
        enemy.draw()
        if check_collision(player_x, player_y, enemy):
            player_life -= 1
            enemies.remove(enemy)
            if player_life <= 0:
                game_over = True

        if enemy.health <= 0:
            enemies.remove(enemy)

    # Update Score and Player Health
    font = pygame.font.SysFont(None, 36)
    draw_text(f"Score: {score}", font, WHITE, 10, 10)
    draw_text(f"Lives: {player_life}", font, WHITE, WIDTH - 120, 10)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()