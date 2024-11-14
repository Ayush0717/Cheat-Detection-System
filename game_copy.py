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

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player Settings
player_size = 50
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5

# Game Loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += player_speed

    # Draw the player as a rectangle
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 10

        # Calculate the direction of the bullet
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 5)

# List to hold active bullets
bullets = []

# Game Loop (updated)
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += player_speed

    # Mouse shooting
    if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bullets.append(Bullet(player_x + player_size // 2, player_y + player_size // 2, mouse_x, mouse_y))

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen)

    # Draw the player as a rectangle
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = 0
        self.size = 40
        self.speed = random.randint(2, 4)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.size, self.size))

# List to hold enemies
enemies = []

# Enemy spawn timer
enemy_spawn_time = 2000  # in milliseconds
last_enemy_spawn = pygame.time.get_ticks()

# Game Loop (updated)
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += player_speed

    # Spawn enemies
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        enemies.append(Enemy())
        last_enemy_spawn = current_time

    # Update and draw enemies
    for enemy in enemies[:]:
        enemy.update()
        enemy.draw(screen)

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen)

    # Collision Detection: Bullet hits enemy
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (enemy.x < bullet.x < enemy.x + enemy.size and
                    enemy.y < bullet.y < enemy.y + enemy.size):
                bullets.remove(bullet)
                enemies.remove(enemy)

    # Draw the player
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

# Game Over logic
def game_over_screen():
    font = pygame.font.SysFont(None, 72)
    text = font.render('GAME OVER', True, WHITE)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    font = pygame.font.SysFont(None, 36)
    text = font.render('Press R to Restart', True, WHITE)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

# Game Loop (updated)
running = True
game_over = False
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_over:
        game_over_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Restart the game
            game_over = False
            player_x, player_y = WIDTH // 2, HEIGHT // 2
            enemies.clear()
            bullets.clear()
        continue

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += player_speed

    # Mouse shooting
    if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bullets.append(Bullet(player_x + player_size // 2, player_y + player_size // 2, mouse_x, mouse_y))

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen)

    # Spawn and update enemies
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        enemies.append(Enemy())
        last_enemy_spawn = current_time

    for enemy in enemies[:]:
        enemy.update()
        enemy.draw(screen)

    # Collision Detection: Bullet hits enemy
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (enemy.x < bullet.x < enemy.x + enemy.size and
                    enemy.y < bullet.y < enemy.y + enemy.size):
                bullets.remove(bullet)
                enemies.remove(enemy)

    # Collision Detection: Player hits enemy
    for enemy in enemies[:]:
        if (player_x < enemy.x + enemy.size and player_x + player_size > enemy.x and
                player_y < enemy.y + enemy.size and player_y + player_size > enemy.y):
            game_over = True

    # Draw the player
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
