import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Character data
characters = {
    "Daniel": {"color": RED, "weapon": "vocal blast", "speed": 4},
    "Rob": {"color": PINK, "weapon": "guitar riff", "speed": 5},
    "Pete": {"color": BLACK, "weapon": "synth wave", "speed": 5},
    "Seb": {"color": ORANGE, "weapon": "drum smash", "speed": 5},
    "Hera": {"color": WHITE, "weapon": "bass pulse", "speed": 6}
}

weapon_sounds = {
    "Daniel": pygame.mixer.Sound("sounds/daniel_weapon.wav"),
    "Rob": pygame.mixer.Sound("sounds/rob_weapon.wav"),
    "Pete": pygame.mixer.Sound("sounds/pete_weapon.wav"),
    "Seb": pygame.mixer.Sound("sounds/seb_weapon.wav"),
    "Hera": pygame.mixer.Sound("sounds/hera_weapon.wav")
}


# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Liquid Rigidity")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load music files
level_music = {
    "map": "map_music.mp3",
    "level1": "level1_music.mp3",
    "level2": "level2_music.mp3"
}

# Play music function
def play_music(level):
    pygame.mixer.music.load(level_music[level])
    pygame.mixer.music.play(-1)

# Display story
def display_story():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 32)
    story_lines = [
        "There it was, just like old faithful...",
        "The eternal Fountain of Filth.",
        "I took a walk straight out of town,", 
        "but stopped and took my time for pleasure.",
        "It was there I found the fountain,", 
        "spewing filth that consumed the land.",
        "Now, you must fight the filth,", 
        "and destroy the fountain to escape its grip.",
        "Prepare for the first challenge: The Fountain of Filth.",
    ]

    y_offset = 50
    for line in story_lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40

    pygame.display.flip()
    pygame.time.wait(7000)  # Display for 7 seconds

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill(characters[name]["color"])
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 3)  # Black outline
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = characters[name]["speed"]
        self.weapon = characters[name]["weapon"]

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def use_weapon(self, mouse_pos):
        print(f"{self.name} used {self.weapon} towards {mouse_pos}!")
        direction = pygame.math.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery).normalize()
        weapon_sounds[self.name].play()
        return Bullet(self.rect.center, direction)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=position)
        self.velocity = direction * 10

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# Brain class
class Brain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed_x = random.choice([-2, 2])  # Horizontal speed
        self.speed_y = random.choice([-2, 2])  # Vertical speed

    def update(self):
        # Move the obstacle
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce the obstacle off screen edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y


# Function to display the welcome screen
def welcome_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Welcome to Liquid Rigidity!", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

    instructions = font.render("Choose your character:", True, BLACK)
    screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 150))

    y_offset = 200
    for i, character in enumerate(characters.keys()):
        char_text = font.render(f"{i + 1}. {character}", True, BLACK)
        screen.blit(char_text, (SCREEN_WIDTH // 2 - char_text.get_width() // 2, y_offset))
        y_offset += 50

    pygame.display.flip()

    selected = None
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    selected = list(characters.keys())[event.key - pygame.K_1]
    return selected

# Function to display the map world
def map_world(player):
    play_music("map")
    screen.fill(GRAY)
    font = pygame.font.Font(None, 36)
    text = font.render("Map World - Explore and enter levels!", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

    doors = []
    for i in range(8):
        door_x = 100 + (i % 4) * 150
        door_y = 200 + (i // 4) * 150
        door_rect = pygame.Rect(door_x, door_y, 50, 50)
        doors.append(door_rect)
        pygame.draw.rect(screen, BLACK, door_rect)
        door_text = font.render(f"{i + 1}", True, WHITE)
        screen.blit(door_text, (door_x + 15, door_y + 15))

    pygame.display.flip()

    in_map = True
    while in_map:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)

        screen.fill(GRAY)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

        for i, door_rect in enumerate(doors):
            pygame.draw.rect(screen, BLACK, door_rect)
            door_text = font.render(f"{i + 1}", True, WHITE)
            screen.blit(door_text, (door_rect.x + 15, door_rect.y + 15))

            if player.rect.colliderect(door_rect):
                if i == 0:  # Level 1
                    display_story()
                    return "level1"
                elif i == 1:  # Level 2
                    display_level2_intro()
                    return "level2"

        screen.blit(player.image, player.rect)

        pygame.display.flip()
        clock.tick(60)

# Level 1 gameplay
def level1(player):
    play_music("level1")
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    for _ in range(5):
        enemies.add(Obstacle())

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    bullet = player.use_weapon(pygame.mouse.get_pos())
                    bullets.add(bullet)

        keys = pygame.key.get_pressed()
        player.update(keys)

        bullets.update()
        enemies.update()

        for bullet in bullets:
            pygame.sprite.spritecollide(bullet, enemies, True)

        bullets.draw(screen)
        enemies.draw(screen)
        screen.blit(player.image, player.rect)

        if len(enemies) == 0:  # All enemies defeated
            print("All enemies defeated! Returning to the map world.")
            pygame.mixer.music.stop()
            return "map"

        pygame.display.flip()
        clock.tick(60)


def display_level2_intro():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 32)
    intro_lines = [
        "Man began his career on Earth as a sex-obsessed ape.",
        "He wished only to make his sex life the source of all happiness",
        "through the eating of brains.",
        "However, he has achieved the exact opposite.",
        "It has become the primary source of dissatisfaction and suffering.",
        "",
        "Prepare yourself to delve into the dark origins of human intelligence,",
        "and face the consequences of the gruesome brain-eating practice.",
        "Welcome to Level 2: The Beginning Was the End."
    ]

    y_offset = 50
    for line in intro_lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40

    pygame.display.flip()
    pygame.time.wait(7000)  # Display for 7 seconds


# Level 2 gameplay
def level2(player):
    play_music("level2")
    brains = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    # Add brains and obstacles to the level
    for _ in range(10):
        brains.add(Brain())
    for _ in range(5):
        obstacles.add(Obstacle())

    collected_brains = 0
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)

        obstacles.update()


        # Check collisions
        if pygame.sprite.spritecollide(player, brains, True):
            collected_brains += 1
            print(f"Brains collected: {collected_brains}")
        if pygame.sprite.spritecollideany(player, obstacles):
            print("You hit an obstacle! Returning to the map world.")
            pygame.mixer.music.stop()
            return "map"

        # Draw everything
        brains.draw(screen)
        obstacles.draw(screen)
        screen.blit(player.image, player.rect)

        # Check win condition
        if collected_brains >= 10:
            print("Level 2 complete! Returning to the map world.")
            pygame.mixer.music.stop()
            return "map"

        pygame.display.flip()
        clock.tick(60)

# Main game loop
player_name = welcome_screen()
player = Player(player_name)
current_level = "map"

while True:
    if current_level == "map":
        current_level = map_world(player)
    elif current_level == "level1":
        current_level = level1(player)
    elif current_level == "level2":
        current_level = level2(player)
