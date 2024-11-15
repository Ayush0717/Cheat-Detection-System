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
last_bullet_time = 0  # Keeps track of the last bullet fire time

# Enemy Settings
enemies = []
enemy_size = 40
initial_enemy_speed = 3
enemy_spawn_time = 1500
last_enemy_spawn = pygame.time.get_ticks()
enemy_speed = initial_enemy_speed

# Game Over, Score, and Restart settings
game_over = False
restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)
score = 0
best_score = 0
best_player = "N/A"
player_name = ""

# Fonts
font_small = pygame.font.SysFont(None, 36)
font_medium = pygame.font.SysFont(None, 48)
font_large = pygame.font.SysFont(None, 72)

# Load Images
player_image = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
pygame.draw.polygon(player_image, GREEN, [(25, 0), (50, 50), (0, 50)])

# Function to draw text
def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

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
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            bullets.remove(self)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), bullet_radius)

# Class for enemies
class Enemy:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - enemy_size)
        self.y = -enemy_size
        self.speed = speed
        self.health = 3

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            global player_life, game_over
            player_life -= 1
            enemies.remove(self)
            if player_life <= 0:
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
    global game_over
    game_over_text = font_large.render('GAME OVER', True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(game_over_text, text_rect)

    current_score_text = font_medium.render(f'Your Score: {score}', True, WHITE)
    current_score_rect = current_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    screen.blit(current_score_text, current_score_rect)

    highest_score_text = font_medium.render(f'Highest Score: {best_score}', True, WHITE)
    highest_score_rect = highest_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(highest_score_text, highest_score_rect)

    pygame.draw.rect(screen, BLUE, restart_button_rect)
    restart_text = font_small.render('Restart', True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    screen.blit(restart_text, restart_rect)

# Function to reset the game
def reset_game():
    global player_x, player_y, player_life, bullets, enemies, game_over, score, best_score, best_player, enemy_speed, player_name
    get_player_name()  # Ask for the player's name again during restart
    player_x = WIDTH // 2
    player_y = HEIGHT - player_size - 10
    player_life = 3
    bullets = []
    enemies = []
    if score > best_score:
        best_score = score
        best_player = player_name
    score = 0
    enemy_speed = initial_enemy_speed
    game_over = False

# Name Input Screen
def get_player_name():
    global player_name
    input_active = True
    player_name = ""
    while input_active:
        screen.fill(BLACK)
        draw_text("Enter your name: " + player_name, font_medium, WHITE, 200, HEIGHT // 2 - 20)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

# Main Game Loop
get_player_name()
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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if player_x + player_size < WIDTH:
            player_x += player_speed

    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2))) + 90
    rotated_player = pygame.transform.rotate(player_image, angle_to_mouse)
    screen.blit(rotated_player, (player_x, player_y))

    # Bullet and Enemy Logic here...
    if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - last_bullet_time > bullet_interval:
        last_bullet_time = pygame.time.get_ticks()
        bullets.append(Bullet(player_x + player_size // 2, player_y + player_size // 2, mouse_x, mouse_y, damage))

    for bullet in bullets[:]:
        bullet.update()
        bullet.draw()

    # Spawn enemies
    if pygame.time.get_ticks() - last_enemy_spawn > enemy_spawn_time:
        last_enemy_spawn = pygame.time.get_ticks()
        enemies.append(Enemy(enemy_speed))

    for enemy in enemies[:]:
        enemy.update()
        enemy.draw()

    # Check for collisions between bullets and enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if pygame.Rect(enemy.x, enemy.y, enemy_size, enemy_size).collidepoint(bullet.x, bullet.y):
                enemy.hit(bullet.damage)
                bullets.remove(bullet)
                break

    # Draw HUD (Score, Life, Player's name)
    draw_text(f'Score: {score}', font_small, WHITE, 10, 10)
    draw_text(f'Life: {player_life}', font_small, WHITE, WIDTH - 100, 10)
    draw_text(f'Name: {player_name}', font_small, WHITE, 10, HEIGHT - 30)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

vinit gandu 