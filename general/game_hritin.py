import pygame
import math
import random
import socket

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

# System-controlled player data
class SystemControlledVariable:
    def __init__(self, value):
        self._value = value
        self._read_permission = True
        self._write_permission = False  # Player has no WRITE permission
        self._legitimate_context = False 

    def get_value(self):
        if self._read_permission:
            return self._value
        raise PermissionError("READ access denied!")

    def set_value(self, value):
        if self._write_permission:
            self._value = value
        else:
            raise PermissionError("WRITE access denied!")

    def grant_write_permission(self, legitimate=False):
        if legitimate:
            self._legitimate_context = True
            self._write_permission = True
        else:
            global illegal_write_detected
            if not illegal_write_detected:
                print("ALERT: Illegal WRITE permission granted to player_life!")
                illegal_write_detected = True
            self._write_permission = True

    def revoke_write_permission(self):
        self._write_permission = False
        self._legitimate_context = False

    def is_legitimate(self):
        return self._legitimate_context




# Player Settings
player_name = ""
player_life = SystemControlledVariable(3)  # System controls the player's life
player_size = 100
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10  # Fixed y-position at the bottom
player_speed = 7
illegal_write_detected = False  # Prevent spamming of illegal detection alerts
speed_boost = False  # Flag to check if speed boost is active

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

# Game Over, Score, and Restart settings
game_over = False
restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)
score = 0
best_score = 0

# Load Images
player_image = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
pygame.draw.polygon(player_image, GREEN, [(25, 0), (50, 50), (0, 50)])



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

# Function to send data to the monitoring script
def send_monitor_data(player_speed, bullet_speed):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            data = f"{player_speed},{bullet_speed}"
            s.sendto(data.encode(), ("localhost", 9999))
            print(f"Data sent to monitor: {data}")  # Added this line for verification
    except Exception as e:
        print(f"Error sending data to monitor: {e}")





def detect_illegal_write_access():
    global illegal_write_detected
    try:
        if player_life.is_legitimate():
            return  # Skip detection for legitimate contexts
        if player_life._write_permission and not illegal_write_detected:
            print("ALERT: Illegal WRITE permission granted to player_life!")
            illegal_write_detected = True
        player_life.set_value(player_life.get_value() + 1)
        print("ALERT: Illegal modification detected! Reverting changes...")
        player_life.revoke_write_permission()
    except PermissionError:
        pass  # No illegal activity if WRITE access is denied


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

# Enemy's update method
class Enemy:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - enemy_size)
        self.y = -enemy_size
        self.speed = speed
        self.health = 3

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            global game_over
            try:
                # Grant WRITE permission legally
                player_life.grant_write_permission(legitimate=True)
                player_life.set_value(player_life.get_value() - 1)
                player_life.revoke_write_permission()
            except PermissionError:
                print("ALERT: Unauthorized WRITE attempt to player_life detected!")
            enemies.remove(self)
            if player_life.get_value() <= 0:
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
    font = pygame.font.SysFont(None, 36)
    draw_text(f'Best Score: {best_score}', font, WHITE, WIDTH // 2 - 70, 10)

# Function to reset the game
def reset_game():
    global player_x, player_y, bullets, enemies, game_over, score, best_score, enemy_speed
    player_x = WIDTH // 2
    player_y = HEIGHT - player_size - 10  # Reset to fixed y-position
    player_life.set_value(3)  # Reset the life value using the SystemControlledVariable instance
    bullets = []
    enemies = []
    if score > best_score:
        best_score = score
    score = 0
    enemy_speed = initial_enemy_speed
    game_over = False
    get_player_name()


# Timing for Bullet Fire
last_bullet_time = 0

def check_collision(player_x, player_y, enemy):
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy_size, enemy_size)
    return player_rect.colliderect(enemy_rect)


# Main Game Loop
get_player_name()
running = True
illegal_access_detected = False

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
    # Movement only in the x-direction
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if player_x + player_size < WIDTH:
            player_x += player_speed

    # Toggle speed boost when "B" is pressed
    if keys[pygame.K_b]:
        speed_boost = not speed_boost
        if speed_boost:
            player_speed *= 1.5
        else:
            player_speed /= 1.5

    # Simulate player trying to cheat
    if keys[pygame.K_p]:
        print("Initial Life:", player_life.get_value())
        player_life.grant_write_permission()
        try:
            player_life.set_value(player_life.get_value() + 1)
            print("Life after illegal access:", player_life.get_value())
        except PermissionError:
            pass

    # Detect illegal activity
    detect_illegal_write_access()

    # Always keep the player's y-position fixed
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle_to_mouse = math.degrees(math.atan2(mouse_y - (player_y + player_size // 2), mouse_x - (player_x + player_size // 2))) + 90
    rotated_player = pygame.transform.rotate(player_image, angle_to_mouse)
    screen.blit(rotated_player, (player_x, player_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    if not game_over and current_time - last_bullet_time >= bullet_interval:
        if pygame.mouse.get_pressed()[0]:
            target_x, target_y = pygame.mouse.get_pos()
            bullet = Bullet(player_x + player_size // 2, player_y + player_size // 2, target_x, target_y, damage)
            bullets.append(bullet)
            last_bullet_time = current_time

    # for bullet in bullets[:]:
    #     bullet.update()
    #     bullet.draw()

    for bullet in bullets[:]:
        if bullet.update():
            bullets.remove(bullet)
        else:
            bullet.draw()

    # if current_time - last_enemy_spawn >= enemy_spawn_time:
    #     new_enemy = Enemy(enemy_speed)
    #     enemies.append(new_enemy)
    #     last_enemy_spawn = current_time

    # Handle Enemies
    if current_time - last_enemy_spawn >= enemy_spawn_time:
        last_enemy_spawn = current_time
        enemy = Enemy(enemy_speed)
        enemies.append(enemy)

    for enemy in enemies[:]:
        enemy.update()
        enemy.draw()
        for bullet in bullets[:]:
            if pygame.Rect(bullet.x - bullet_radius, bullet.y - bullet_radius, bullet_radius * 2, bullet_radius * 2).colliderect(pygame.Rect(enemy.x, enemy.y, enemy_size, enemy_size)):
                enemy.hit(bullet.damage)
                bullets.remove(bullet)

        if check_collision(player_x, player_y, enemy):
            enemies.remove(enemy)
            try:
                # Grant WRITE permission legally
                player_life.grant_write_permission(legitimate=True)
                player_life.set_value(player_life.get_value() - 1)
                player_life.revoke_write_permission()
            except PermissionError:
                print("ALERT: Unauthorized WRITE attempt to player_life detected!")
            if player_life.get_value() <= 0:
                game_over = True


    font = pygame.font.SysFont(None, 36)
    draw_text(f'Life: {player_life.get_value()}', font, WHITE, 10, 10)
    draw_text(f'Score: {score}', font, WHITE, WIDTH - 120, 10)

    if illegal_access_detected:
        draw_text("Illegal Access Detected!", font, RED, WIDTH // 2 - 150, HEIGHT - 50)

    # Send data to the monitoring script (player speed, bullet speed)
    send_monitor_data(player_speed, bullet_speed)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
