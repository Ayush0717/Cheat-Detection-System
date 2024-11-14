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
        # Check if enemy has crossed the bottom of the screen
        if self.y > HEIGHT:
            global player_life  # Access the player's life globally
            player_life -= 1  # Decrease player life when enemy crosses the bottom
            enemies.remove(self)  # Remove the enemy from the game
            if player_life <= 0:  # Check if the player's life reaches 0
                global game_over  # Set the game over flag
                game_over = True  # End the game when life reaches 0

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

# Function to check collision between player and enemies
def check_collision(player_x, player_y, enemy):
    # Create player and enemy rectangles
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy_size, enemy_size)

    # Check if the player rectangle intersects with the enemy rectangle (touching or colliding)
    if player_rect.colliderect(enemy_rect):
        return True
    return False

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
        if pygame.mouse.get_pressed()[0]:
            target_x, target_y = pygame.mouse.get_pos()
            bullet = Bullet(player_x + player_size // 2, player_y + player_size // 2, target_x, target_y, damage)
            bullets.append(bullet)
            last_bullet_time = current_time  # Update last bullet time

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet.update()
        bullet.draw()

    # Enemy spawn logic
    if current_time - last_enemy_spawn >= enemy_spawn_time:
        new_enemy = Enemy(enemy_speed)
        enemies.append(new_enemy)
        last_enemy_spawn = current_time

    # Update and draw enemies
    for enemy in enemies[:]:
        enemy.update()
        enemy.draw()

        # Check collision with bullets and reduce enemy health
        for bullet in bullets[:]:
            if pygame.Rect(bullet.x - bullet_radius, bullet.y - bullet_radius, bullet_radius * 2, bullet_radius * 2).colliderect(pygame.Rect(enemy.x, enemy.y, enemy_size, enemy_size)):
                enemy.hit(bullet.damage)
                bullets.remove(bullet)  # Remove bullet after collision

        # Check if the player collided with the enemy
        if check_collision(player_x, player_y, enemy):
            player_life -= 1  # Reduce life when collision occurs
            enemies.remove(enemy)  # Remove the enemy

    # Draw the player's life
    font = pygame.font.SysFont(None, 36)
    draw_text(f'Life: {player_life}', font, WHITE, 10, 10)

    # Draw the score
    draw_text(f'Score: {score}', font, WHITE, WIDTH - 120, 10)

    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
