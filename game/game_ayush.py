import pygame
import math
import random 

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

# Class for bullets
class Bullet:
    def __init__(self, x, y, target_x, target_y, damage):  # Corrected __init__ method
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
    def __init__(self, speed):  # Use __init__, not _init_
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
            enemy_speed = initial_enemy_speed + (score // 50)

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

# Timing for Bullet Fire
last_bullet_time = 0

# Function to check collision between player and enemies
def check_collision(player_x, player_y, enemy):
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy_size, enemy_size)
    return player_rect.colliderect(enemy_rect)


# game_files = ["game.py", "cheat_detection/detector.py", "cheat_detection/monitor.py"]
# monitor = GameMonitor(max_speed=15, min_bullet_interval=200, game_files=game_files)

monitor = Monitor("game/game_ayush.py")
monitor.start_monitoring()

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

    # Monitor the game environment for cheat detection
    game_monitor.monitor_game_environment()  # Call to monitor the game environment

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
    angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2))) + 90
    rotated_player = pygame.transform.rotate(player_image, angle_to_mouse)
    rotated_rect = rotated_player.get_rect(center=(player_x + player_size // 2, player_y + player_size // 2))
    screen.blit(rotated_player, rotated_rect.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    if current_time - last_bullet_time >= bullet_interval:
        if pygame.mouse.get_pressed()[0]:
            target_x, target_y = pygame.mouse.get_pos()
            bullet = Bullet(player_x + player_size // 2, player_y + player_size // 2, target_x, target_y, damage)
            bullets.append(bullet)
            last_bullet_time = current_time

    for bullet in bullets[:]:
        bullet.update()
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
        if check_collision(player_x, player_y, enemy):
            player_life -= 1
            enemies.remove(enemy)
            if player_life <= 0:
                game_over = True

    font = pygame.font.SysFont(None, 36)
    draw_text(f'Life: {player_life}', font, WHITE, 10, 10)
    draw_text(f'Score: {score}', font, WHITE, WIDTH - 120, 10)

    pygame.display.flip()
    clock.tick(FPS)
import sys

# Get the path of the Python executable


pygame.quit()
