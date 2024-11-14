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
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
player_life = 3

# Bullet Settings
bullets = []
bullet_speed = 10  # Constant bullet speed
bullet_radius = 5
damage = 1  # Bullet damage
bullet_interval = 200  # 200 milliseconds interval between each shot

# Enemy Settings (increased initial speed)
enemies = []
enemy_size = 40
enemy_spawn_time = 1500  # in milliseconds
last_enemy_spawn = pygame.time.get_ticks()
enemy_speed = 3  # Initial enemy speed
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

# Class for bullets
class Bullet:
    def __init__(self, x, y, target_x, target_y, damage):
        self.x = x
        self.y = y
        self.damage = damage  # Bullet damage
        
        # Calculate the angle and direction based on the mouse position
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * bullet_speed  # Constant bullet speed
        self.dy = math.sin(angle) * bullet_speed  # Constant bullet speed

    def update(self):
        # Move bullet towards the target direction
        self.x += self.dx
        self.y += self.dy

        # Check if bullet is off screen
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            bullets.remove(self)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), bullet_radius)

# Class for enemies
class Enemy:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - enemy_size)
        self.y = -enemy_size  # Spawn above screen
        self.speed = speed  # Use the modified speed value
        self.health = 3  # Each enemy has 3 health points

    def update(self):
        self.y += self.speed
        # Remove enemy if off screen
        if self.y > HEIGHT:
            enemies.remove(self)

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, enemy_size, enemy_size))
        # Draw health bar
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, (self.health / 3) * enemy_size, 5))

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            enemies.remove(self)
            global score, best_score
            score += 10  # Add points for each enemy destroyed

# Function to handle game over
def handle_game_over():
    global game_over, best_score
    font = pygame.font.SysFont(None, 72)
    
    # Calculate the text size to center it
    game_over_text = font.render('GAME OVER', True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    
    screen.blit(game_over_text, text_rect)  # Draw centered game over text
    
    # Draw restart button
    pygame.draw.rect(screen, BLUE, restart_button_rect)
    font = pygame.font.SysFont(None, 36)
    restart_text = font.render('Restart', True, WHITE)
    
    # Center the restart text inside the button
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    screen.blit(restart_text, restart_rect)

    # Display Best Score
    font = pygame.font.SysFont(None, 36)
    draw_text(f'Best Score: {best_score}', font, WHITE, WIDTH // 2 - 70, 10)

# Function to reset the game
def reset_game():
    global player_x, player_y, player_life, bullets, enemies, game_over, score, best_score, enemy_spawn_time, enemy_speed_decrement, damage, enemy_speed
    player_x, player_y = WIDTH // 2, HEIGHT // 2
    player_life = 3
    bullets = []
    enemies = []
    
    # Update best_score only when score exceeds it
    if score > best_score:
        best_score = score
        
    # Reset score for new game
    score = 0
    
    # Decrease enemy speed slightly each game
    enemy_speed_decrement += 0.2
    # Reset damage to 1 at the start of a new game
    damage = 1
    game_over = False

    # Increase enemy speed after each game
    enemy_speed += 1  # Increase speed of enemies as the game progresses

# Timing for Bullet Fire
last_bullet_time = 0  # Store the last time a bullet was fired

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
    # Player Movement with boundaries
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if player_x > 0:  # Prevent moving off the left edge
            player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if player_x + player_size < WIDTH:  # Prevent moving off the right edge
            player_x += player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if player_y > 0:  # Prevent moving off the top edge
            player_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if player_y + player_size < HEIGHT:  # Prevent moving off the bottom edge
            player_y += player_speed

    # Get mouse position and rotate player image based on mouse direction
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2))) + 90
    rotated_player = pygame.transform.rotate(player_image, angle_to_mouse)
    screen.blit(rotated_player, (player_x, player_y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current time in milliseconds
    current_time = pygame.time.get_ticks()

    # Check if enough time has passed to fire a bullet
    if current_time - last_bullet_time >= bullet_interval:
        if pygame.mouse.get_pressed()[0]:  # Left mouse button is clicked
            # Create a bullet and add it to the bullets list
            bullets.append(Bullet(player_x + player_size // 2, player_y + player_size // 2, mouse_x, mouse_y, damage))
            last_bullet_time = current_time  # Update last bullet fire time

    # Update and draw bullets
    for bullet in bullets:
        bullet.update()
        bullet.draw()

    # Enemy Spawning
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        enemies.append(Enemy(enemy_speed))  # Use the updated enemy speed
        last_enemy_spawn = current_time

    # Update and draw enemies
    for enemy in enemies:
        enemy.update()
        enemy.draw()

    # Collision Detection: Bullet hits enemy
    for bullet in bullets:
        for enemy in enemies:
            if enemy.x < bullet.x < enemy.x + enemy_size and enemy.y < bullet.y < enemy.y + enemy_size:
                enemy.hit(bullet.damage)
                bullets.remove(bullet)

    # Collision Detection: Enemy hits player
    for enemy in enemies:
        if player_x < enemy.x < player_x + player_size and player_y < enemy.y < player_y + player_size:
            player_life -= 1
            enemies.remove(enemy)
            if player_life <= 0:
                game_over = True

    # Display Score and Life
    font = pygame.font.SysFont(None, 36)
    draw_text(f'Score: {score}', font, WHITE, 10, 10)
    draw_text(f'Life: {player_life}', font, WHITE, WIDTH - 100, 10)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
