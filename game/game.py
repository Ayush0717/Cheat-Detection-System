import pygame
import math
import random
import os
import psutil
import time
import threading
import hashlib
import sys
import pdb
import sys
import os

# Get the path of the currently running Python script
script_path = sys.argv[0]

# Get the absolute path of the script
absolute_path = os.path.abspath(script_path)

print(f"Path of the Python script: {absolute_path}")

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
# Class for bullets
class Bullet:
    def __init__(self, x, y, target_x, target_y, damage):  # Corrected __init_ method
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


# Class for enemies
# Class for enemies
class Enemy: 
    def __init__(self, speed):  # Corrected __init_ method
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
    player_life = 200
    bullets = []
    enemies = []
    if score > best_score:
        best_score = score
    score = 0
    enemy_speed = initial_enemy_speed
    game_over = False
    get_player_name()

# Function to detect cheating (example of memory manipulation, suspicious processes, etc.)

# Function to detect abnormal score/life changes
# Function to detect suspicious score/life changes
def detect_suspicious_changes(last_score_check, last_life_check, last_score_check_value, last_life_check_value):
    current_time = time.time()

    # Check for abnormal score change
    if current_time - last_score_check > 5:  # Check every 5 seconds
        # Allow a certain amount of natural score increase
        if score - last_score_check_value > 100:  # Suspicious if score jumps too much in 5 seconds
            print(f"Suspicious score change detected: {score} (Last check: {last_score_check_value})")
            alert_admin(f"Suspicious score change detected: {score} (Last check: {last_score_check_value})")
        
        # Update the last score check value
        last_score_check_value = score
        last_score_check = current_time

    # Check for abnormal life change
    if current_time - last_life_check > 5:  # Check every 5 seconds
        # Allow a certain amount of natural life decrease
        if player_life - last_life_check_value > 1:  # Suspicious if life decreases too much in 5 seconds
            print(f"Suspicious life change detected: {player_life} (Last check: {last_life_check_value})")
            alert_admin(f"Suspicious life change detected: {player_life} (Last check: {last_life_check_value})")

        # Update the last life check value
        last_life_check_value = player_life
        last_life_check = current_time

    return last_score_check, last_life_check, last_score_check_value, last_life_check_value


# Function to detect cheating
def detect_cheat():
    print("Cheat detection started...")  # This should print when the thread is started

    last_score_check = time.time()
    last_life_check = time.time()
    last_score_check_value = score  # Track last score value for comparison
    last_life_check_value = player_life  # Track last life value for comparison

    while True:
        # Detect suspicious processes (cheat tools, debuggers, etc.)
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            # Detect common cheat tools (e.g., Cheat Engine, debuggers, etc.)
            if 'cheat' in proc.info['name'].lower() or 'x64' in proc.info['name'].lower():
                print(f"Illegal access detected: Suspicious process {proc.info['name']} (PID: {proc.info['pid']})")
                alert_admin(f"Suspicious process detected: {proc.info['name']} (PID: {proc.info['pid']})")
            elif proc.info['exe'] and 'debug' in proc.info['exe'].lower():
                print(f"Illegal access detected: Debugger detected (PID: {proc.info['pid']})")
                alert_admin(f"Debugger detected (PID: {proc.info['pid']})")

        # Check for abnormal score or life changes
        last_score_check, last_life_check, last_score_check_value, last_life_check_value = detect_suspicious_changes(
            last_score_check, last_life_check, last_score_check_value, last_life_check_value
        )

        # Monitor the score to detect sudden, impossible changes
        time.sleep(1)  # Pause to avoid excessive CPU usage


def detect_code_injection():
    # Look for suspicious shared libraries or memory injections
    try:
        process = psutil.Process(os.getpid())
        for dll in process.memory_maps():
            # Look for DLLs (Dynamic-Link Libraries) that shouldn't be loaded
            if 'cheat' in dll.path.lower() or 'inject' in dll.path.lower():
                print(f"Suspicious DLL detected: {dll.path}")
                return True

    except psutil.NoSuchProcess:
        return False

    return False

def alert_admin(message):
    # In a real-world scenario, you might send this to a log, alert system, or administrator
    print(f"ALERT: {message}")

# Timing for Bullet Fire
last_bullet_time = 0

# Function to check collision between player and enemies
def check_collision(player_x, player_y, enemy):
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy_size, enemy_size)
    
    if player_rect.colliderect(enemy_rect):
        return True
    return False

def set_player_life(new_life):
    global player_life
    player_life = new_life
    print(f"Player life set to {player_life}")


# Main Game Loop
get_player_name()  # Prompt player for name before starting the game

running = True

# Start the cheat detection thread
cheat_detection_thread = threading.Thread(target=detect_cheat, daemon=True)
cheat_detection_thread.start()

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

    keys = pygame.key.get_pressed()
    # Movement logic
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if player_x + player_size < WIDTH:
            player_x += player_speed

    
    # Toggle speed boost when "B" is pressed
    if keys[pygame.K_l]:
        score = score + 100

    # Always keep the player's y-position fixed
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2))) + 90
    rotated_player = pygame.transform.rotate(player_image, angle_to_mouse)
    rotated_rect = rotated_player.get_rect(center=(player_x + player_size // 2, player_y + player_size // 2))
    screen.blit(rotated_player, rotated_rect.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    if not game_over and current_time - last_bullet_time >= bullet_interval:
        if keys[pygame.K_SPACE]:
            bullet = Bullet(player_x + player_size // 2, player_y, mouse_x, mouse_y, damage)
            bullets.append(bullet)
            last_bullet_time = current_time

    for bullet in bullets[:]:
        if bullet.update():
            bullets.remove(bullet)
        else:
            bullet.draw()

    # Spawn enemies
    if current_time - last_enemy_spawn >= enemy_spawn_time:
        last_enemy_spawn = current_time
        enemies.append(Enemy(enemy_speed))

    for enemy in enemies[:]:
        enemy.update()
        enemy.draw()
        # Check for collision with player and reduce life
        if check_collision(player_x, player_y, enemy):
            player_life -= 1  # Reduce life on collision
            enemies.remove(enemy)  # Remove the enemy after collision

        for bullet in bullets[:]:
            if check_collision(bullet.x, bullet.y, enemy):
                enemy.hit(bullet.damage)
                bullets.remove(bullet)

    # Update score, health, and life
    font = pygame.font.SysFont(None, 36)
    draw_text(f"Score: {score}", font, WHITE, 10, 10)
    draw_text(f"Lives: {player_life}", font, WHITE, 10, 50)


    keys = pygame.key.get_pressed()

    # Set life to 10 for testing

   # Fill the screen with black


    # Check if game over (no lives left)
    if player_life <= 0:
        game_over = True

    pygame.display.flip()
    clock.tick(FPS)
import sys

# Get the path of the Python executable


pygame.quit()