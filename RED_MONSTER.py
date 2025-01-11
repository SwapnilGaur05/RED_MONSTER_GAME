import pygame
import sys
import random
import time  

# Initialize Pygame
pygame.init()

# Get screen resolution dynamically and set full screen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Jumping Red Monster with Trees and Sun")

# Colors
BLUE = (135, 206, 250)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Monster dimensions and variables
monster_width, monster_height = 60, 60
monster_x = WIDTH // 2
monster_y = HEIGHT - 100
monster_speed = 5  
jumping = False
gravity = 5
velocity = -25
current_velocity = 0
scroll_offset = 0

# Ground height
ground_height = 50

# Stones
num_stones = 5
stones = []

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Clock and timers
clock = pygame.time.Clock()
start_time = time.time()  
last_update_time = time.time()  # Timer for increasing difficulty

# Reset game function
def reset_game():
    global monster_x, monster_y, current_velocity, stones, score, scroll_offset, jumping, start_time, last_update_time
    monster_x = WIDTH // 2
    monster_y = HEIGHT - 100
    current_velocity = 0
    scroll_offset = 0
    jumping = False
    stones.clear()
    for _ in range(num_stones):
        stone_width = random.randint(30, 50)
        stone_height = random.randint(30, 50)
        stone_x = random.randint(0, WIDTH * 3)
        stone_y = random.randint(-HEIGHT, 0)
        stone_speed = random.randint(3, 8)
        stones.append({"x": stone_x, "y": stone_y, "width": stone_width, "height": stone_height, "speed": stone_speed})
    score = 0
    start_time = time.time()  
    last_update_time = time.time()  # Reset the difficulty timer

# Game over screen
def show_game_over():
    screen.fill(BLUE)
    game_over_text = large_font.render("Game Over!", True, BLACK)
    score_text = font.render(f"Time Played: {int(score)} seconds", True, BLACK)
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 100))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 3 + 200))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                reset_game()
                return
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

# Load monster image
reset_game()
try:
    monster_image = pygame.image.load("monster.jpg")
    monster_image = pygame.transform.scale(monster_image, (monster_width, monster_height))
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

# Draw fixed trees
def draw_fixed_trees():
    tree_positions = [
        (100, HEIGHT - ground_height - 50),
        (250, HEIGHT - ground_height - 50),
        (400, HEIGHT - ground_height - 50),
        (550, HEIGHT - ground_height - 50),
        (700, HEIGHT - ground_height - 50),
        (850, HEIGHT - ground_height - 50),
        (1000, HEIGHT - ground_height - 50),
        (1150, HEIGHT - ground_height - 50),
        (1300, HEIGHT - ground_height - 50)
    ]
    
    tree_trunk_width = 40
    tree_trunk_height = 100
    tree_leaves_radius = 40
    
    for pos in tree_positions:
        tree_x, tree_y = pos
        pygame.draw.rect(screen, BROWN, (tree_x, tree_y, tree_trunk_width, tree_trunk_height))
        pygame.draw.circle(screen, GREEN, (tree_x + tree_trunk_width // 2, tree_y), tree_leaves_radius)

# Draw sun
def draw_sun():
    sun_radius = 50
    sun_x = WIDTH - 100  # Positioned to the top right corner
    sun_y = 100
    pygame.draw.circle(screen, YELLOW, (sun_x, sun_y), sun_radius)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        monster_x -= monster_speed
    if keys[pygame.K_RIGHT]:
        monster_x += monster_speed

    if keys[pygame.K_SPACE] and not jumping:
        jumping = True
        current_velocity = velocity

    scroll_offset += 2

    screen.fill(BLUE)

    draw_fixed_trees()
    draw_sun()

    # Check if 60 seconds have passed to increase difficulty
    current_time = time.time()
    if current_time - last_update_time >= 60:
        # Increase the speed of existing stones
        for stone in stones:
            stone["speed"] += 1  # Increment stone speed
            stone["speed"] = min(stone["speed"], 15)  # Cap the speed to prevent it from getting too fast

        # Add new stones to the list
        for _ in range(3):  # Add 3 new stones
            stone_width = random.randint(30, 50)
            stone_height = random.randint(30, 50)
            stone_x = random.randint(0, WIDTH * 3)
            stone_y = random.randint(-HEIGHT, 0)
            stone_speed = random.randint(3, 8)
            stones.append({"x": stone_x, "y": stone_y, "width": stone_width, "height": stone_height, "speed": stone_speed})

        last_update_time = current_time  # Reset the timer

    # Draw ground
    pygame.draw.rect(screen, BROWN, (0 - scroll_offset, HEIGHT - ground_height, WIDTH * 100, ground_height))

    # Monster jumping logic
    if jumping:
        monster_y += current_velocity
        current_velocity += gravity
        if monster_y + monster_height >= HEIGHT - ground_height:
            monster_y = HEIGHT - ground_height - monster_height
            jumping = False
        if monster_y + monster_height >= HEIGHT:
            show_game_over()

    # Stones logic
    for stone in stones:
        stone["y"] += stone["speed"]
        if stone["y"] > HEIGHT - ground_height:
            stone["y"] = random.randint(-HEIGHT, 0)
            stone["x"] = random.randint(scroll_offset, scroll_offset + WIDTH)
            stone["speed"] = random.randint(3, 8)

        stone_screen_x = stone["x"] - scroll_offset
        if 0 <= stone_screen_x <= WIDTH:
            pygame.draw.rect(screen, GRAY, (stone_screen_x, stone["y"], stone["width"], stone["height"]))

        # Collision detection
        if (
            monster_x - monster_width // 2 < stone_screen_x + stone["width"] and
            monster_x + monster_width // 2 > stone_screen_x and
            monster_y < stone["y"] + stone["height"] and
            monster_y + monster_height > stone["y"]
        ):
            show_game_over()

    # Draw monster
    screen.blit(monster_image, (monster_x - monster_width // 2, monster_y))

    # Display score
    elapsed_time = time.time() - start_time  
    score = elapsed_time  
    score_surface = font.render(f"Time Played: {int(score)} seconds", True, BLACK)
    screen.blit(score_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)
