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
    "map": "sounds/map_music.mp3",
    "level1": "sounds/level1_music.mp3",
    "level2": "sounds/level2_music.mp3",
    "level3": "sounds/level3_music.mp3",
    "level4": "sounds/level4_music.mp3"

}

def draw_label(message, position, font_size=32, color=BLACK):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, 32)
        self.color = GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Outline
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


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

    start_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50, "Start Level", lambda: None)

     # Wait for the player to press the button
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.handle_event(event)  # Check if button is clicked

        screen.fill(WHITE)
        y_offset = 50
        for line in story_lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 40

        start_button.draw(screen)  # Draw the button
        pygame.display.flip()
        clock.tick(60)
        if pygame.mouse.get_pressed()[0] and start_button.rect.collidepoint(pygame.mouse.get_pos()):
            running = False  # Exit intro loop when button is clicked

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.image.fill(characters[name]["color"])
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 3)  # Black outline
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = characters[name]["speed"]
        self.weapon = characters[name]["weapon"]

    def move(self, dx, dy, walls):
        # Check for collisions on the X axis
        self.rect.x += dx
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= dx

        # Check for collisions on the Y axis
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y -= dy


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
    play_music("map")  # Play map music
    screen.fill(GRAY)
    font = pygame.font.Font(None, 36)
    text = font.render("Map World - Explore and enter levels!", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

    doors = []
    for i in range(8):  # Create 8 doors for levels
        door_x = 100 + (i % 4) * 150
        door_y = 200 + (i // 4) * 150
        door_rect = pygame.Rect(door_x, door_y, 50, 50)
        doors.append(door_rect)
        pygame.draw.rect(screen, BLACK, door_rect)
        door_text = font.render(f"{i + 1}", True, WHITE)
        screen.blit(door_text, (door_x + 15, door_y + 15))

    # Place the player in the center of the map
    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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

            if player.rect.colliderect(door_rect):  # Check collision with doors
                if i == 0:  # Level 1
                    display_story()
                    return "level1"
                elif i == 1:  # Level 2
                    display_level2_intro()
                    return "level2"
                elif i == 2:  # Level 3
                    display_level3_intro()
                    return "level3"
                elif i == 3:  # Level 4
                    display_level4_intro()
                    return "level4"

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
            draw_label("All enemies defeated! Returning to the map world.", (SCREEN_WIDTH // 2, 30))
            pygame.display.flip()  # Update the screen to show the label
            pygame.time.delay(2000)  # Wait for 2 seconds
            #print("All enemies defeated! Returning to the map world.")
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

    start_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50, "Start Level", lambda: None)

     # Wait for the player to press the button
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.handle_event(event)  # Check if button is clicked

        screen.fill(WHITE)
        y_offset = 50
        for line in intro_lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 40

        start_button.draw(screen)  # Draw the button
        pygame.display.flip()
        clock.tick(60)
        if pygame.mouse.get_pressed()[0] and start_button.rect.collidepoint(pygame.mouse.get_pos()):
            running = False  # Exit intro loop when button is clicked


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
            #draw_label(f"Brains collected: {collected_brains}", (SCREEN_WIDTH // 2, 30))
            #pygame.display.flip()  # Update the screen to show the label
            #pygame.time.delay(500)  # Wait for 2 seconds
            print(f"Brains collected: {collected_brains}")
        if pygame.sprite.spritecollideany(player, obstacles):
            draw_label("You hit an obstacle! Returning to the map world.", (SCREEN_WIDTH // 2, 30))
            pygame.display.flip()  # Update the screen to show the label
            pygame.time.delay(2000)  # Wait for 2 seconds
            
            #print("You hit an obstacle! Returning to the map world.")
            pygame.mixer.music.stop()
            return "map"

        # Draw everything
        brains.draw(screen)
        obstacles.draw(screen)
        screen.blit(player.image, player.rect)

        # Check win condition
        if collected_brains >= 10:
            draw_label("Level 2 complete! Returning to the map world.", (SCREEN_WIDTH // 2, 30))
            pygame.display.flip()  # Update the screen to show the label
            pygame.time.delay(2000)  # Wait for 2 seconds
            
            #print("Level 2 complete! Returning to the map world.")
            pygame.mixer.music.stop()
            return "map"

        pygame.display.flip()
        clock.tick(60)

def display_level3_intro():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 32)
    intro_lines = [
        "In our time, the defense of the innocent and the defense of the Earth",
        "are of the utmost importance. The greed and selfishness of society",
        "is destroying our world and killing animals by the billions.",
        "",
        "NO MORE shall we tolerate these acts.",
        "You must rescue the animals from humans before it's too late.",
        "Set the animals free or scare the humans away to save the planet.",
        "",
        "Welcome to Level 3: Vegan Hate.",
    ]

    y_offset = 50
    for line in intro_lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40

    start_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50, "Start Level", lambda: None)

     # Wait for the player to press the button
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.handle_event(event)  # Check if button is clicked

        screen.fill(WHITE)
        y_offset = 50
        for line in intro_lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 40

        start_button.draw(screen)  # Draw the button
        pygame.display.flip()
        clock.tick(60)
        if pygame.mouse.get_pressed()[0] and start_button.rect.collidepoint(pygame.mouse.get_pos()):
            running = False  # Exit intro loop when button is clicked

#Level 3 Gameplay
def level3(player):
    display_level3_intro()  # Show the introduction
    play_music("level3")  # Play level-specific music

    TILE_SIZE = 40

    # Create a safe zone
    safe_zone = pygame.Rect(50, 50, 200, 100)

    # Create groups for animals, enemies, and walls
    animals = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    walls = pygame.sprite.Group()

    # Create walls
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        walls.add(Wall(x, 0, TILE_SIZE, TILE_SIZE))  # Top wall
        walls.add(Wall(x, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Bottom wall
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        walls.add(Wall(0, y, TILE_SIZE, TILE_SIZE))  # Left wall
        walls.add(Wall(SCREEN_WIDTH - TILE_SIZE, y, TILE_SIZE, TILE_SIZE))  # Right wall

    # Place animals away from screen edges
    for _ in range(10):  # Add 10 animals
        while True:
            animal = Animal()
            if TILE_SIZE < animal.rect.x < SCREEN_WIDTH - 2 * TILE_SIZE and TILE_SIZE < animal.rect.y < SCREEN_HEIGHT - 2 * TILE_SIZE:
                animals.add(animal)
                break  # Only add the animal if it is within the valid area

    # Add fewer enemies to the level
    for _ in range(3):  # Add 3 enemies
        while True:
            enemy = Enemy(random.randint(1, SCREEN_WIDTH // TILE_SIZE - 2) * TILE_SIZE,
                          random.randint(1, SCREEN_HEIGHT // TILE_SIZE - 2) * TILE_SIZE)
            if TILE_SIZE < enemy.rect.x < SCREEN_WIDTH - 2 * TILE_SIZE and TILE_SIZE < enemy.rect.y < SCREEN_HEIGHT - 2 * TILE_SIZE:
                enemies.add(enemy)
                break  # Only add the enemy if it is within the valid area

    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Check for collisions between player and animals (push animals)
        for animal in pygame.sprite.spritecollide(player, animals, False):  # Don't remove animals
            direction = pygame.math.Vector2(0, 0)
            if keys[pygame.K_LEFT]:
                direction.x = -1
            if keys[pygame.K_RIGHT]:
                direction.x = 1
            if keys[pygame.K_UP]:
                direction.y = -1
            if keys[pygame.K_DOWN]:
                direction.y = 1

            if direction.length() > 0:
                direction = direction.normalize() * 5  # Push animal 5 pixels
                animal.rect.x += int(direction.x)
                animal.rect.y += int(direction.y)

                # Keep animals within bounds
                animal.rect.x = max(TILE_SIZE, min(animal.rect.x, SCREEN_WIDTH - 2 * TILE_SIZE))
                animal.rect.y = max(TILE_SIZE, min(animal.rect.y, SCREEN_HEIGHT - 2 * TILE_SIZE))

        # Update enemies
        enemies.update(walls)

        # Check collisions between enemies and animals
        for enemy in enemies:
            for animal in pygame.sprite.spritecollide(enemy, animals, True):  # Remove animals caught by enemies
                print("An animal has been caught!")

        # Check if animals reach the safe zone
        for animal in animals:
            if safe_zone.colliderect(animal.rect):
                animals.remove(animal)
                print("An animal reached the safe zone!")

        # Draw the safe zone
        pygame.draw.rect(screen, GREEN, safe_zone)

        # Draw animals, enemies, and walls
        animals.draw(screen)
        enemies.draw(screen)
        walls.draw(screen)

        # Draw the player
        screen.blit(player.image, player.rect)

        # Check win condition
        if len(animals) == 0:  # All animals rescued or caught
            pygame.mixer.music.stop()
            if len(animals) == 0:
                draw_label("Level complete! Returning to the map world.", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(2000)  # Wait for 2 seconds
            return "map"

        pygame.display.flip()
        clock.tick(60)






class Animal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)  # Animals are green
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed_y = random.choice([-2, 2])

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y = -self.speed_y


class Human(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)  # Humans are red
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed_x = random.choice([-2, 2])

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x

def display_level4_intro():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 32)
    intro_lines = [
        "Hunger strikes in the dead of night.",
        "The neon glow of 7-Eleven calls to you.",
        "Hot dogs rolling on the grill, fulfilling every need.",
        "Navigate the maze of alleys and streets,",
        "find the 7-Eleven, and satisfy your craving.",
        "",
        "Welcome to Level 4: Seven-11 Hot Dog.",
    ]

    y_offset = 50
    for line in intro_lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40

    start_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50, "Start Level", lambda: None)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.handle_event(event)

        screen.fill(WHITE)
        y_offset = 50
        for line in intro_lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 40

        start_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        if pygame.mouse.get_pressed()[0] and start_button.rect.collidepoint(pygame.mouse.get_pos()):
            running = False  # Exit intro loop when button is clicked

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)  # Enemies are red
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2  # Enemy movement speed
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

    def update(self, walls):
        # Move the enemy
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y

        # Reverse direction if colliding with walls
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= self.speed * self.direction.x
            self.rect.y -= self.speed * self.direction.y
            self.direction.x *= -1
            self.direction.y *= -1

        # Randomly change direction occasionally
        if random.randint(0, 100) < 5:  # 5% chance to change direction
            self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))



def level4(player):
    display_level4_intro()  # Show the introduction
    play_music("level4")  # Play level-specific music

    TILE_SIZE = 40
    GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE  # 20 tiles wide
    GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE  # 15 tiles tall

    # Create a more complex maze layout
    maze_layout = [
        "WWWWWWWWWWWWWWWWWWWW",
        "W                  W",
        "W   WW   W   WWW   W",
        "W   W        W     W",
        "W   W   WWW  W     W",
        "W                  W",
        "WWWWWW   W   WWWWWWW",
        "W        W     711 W",
        "W   WWWWWWWWWW      ",
        "W   W       W   WWWW",
        "W   W   W   W     WW",
        "W   WWWWW   WWWWW  W",
        "W                  W",
        "W   WWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWW",
    ]

    # Create maze walls
    walls = pygame.sprite.Group()
    for y, row in enumerate(maze_layout):
        for x, cell in enumerate(row):
            if cell == "W":
                walls.add(Wall(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Define 7-Eleven location
    seven_eleven = pygame.Rect(15 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    # Create enemies
    enemies = pygame.sprite.Group()
    for _ in range(5):  # Add 5 enemies to increase difficulty
        enemy_x = random.randint(1, GRID_WIDTH - 2) * TILE_SIZE  # Random position within maze bounds
        enemy_y = random.randint(1, GRID_HEIGHT - 2) * TILE_SIZE
        if maze_layout[enemy_y // TILE_SIZE][enemy_x // TILE_SIZE] != "W":  # Ensure enemy is not inside a wall
            enemies.add(Enemy(enemy_x, enemy_y))

    # Set player position at the far left of the screen
    player.rect.x = TILE_SIZE  # Always start at the far-left edge
    player.rect.y = random.randint(1, GRID_HEIGHT - 2) * TILE_SIZE  # Random vertical position
    while pygame.sprite.spritecollide(player, walls, False):
        player.rect.y += TILE_SIZE  # Adjust downward until in a free space
        if player.rect.y >= SCREEN_HEIGHT:
            player.rect.y = TILE_SIZE  # Wrap back to the top

    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Check for movement input and move the player
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed

        player.move(dx, dy, walls)

        # Update enemies
        enemies.update(walls)

        # Check if the player touches an enemy
        if pygame.sprite.spritecollide(player, enemies, False):
            draw_label("You were caught by an enemy!", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), font_size=36, color=RED)
            pygame.display.flip()
            pygame.time.wait(2000)  # Show message for 2 seconds
            pygame.mixer.music.stop()
            return "map"  # Return to map world

        # Check if the player reaches the 7-Eleven
        if player.rect.colliderect(seven_eleven):
            show_hot_dog_scene()
            pygame.mixer.music.stop()
            return "map"

        # Draw everything
        walls.draw(screen)
        enemies.draw(screen)
        pygame.draw.rect(screen, GREEN, seven_eleven)  # Highlight 7-Eleven in green
        screen.blit(player.image, player.rect)

        pygame.display.flip()
        clock.tick(60)


def show_hot_dog_scene():
    screen.fill(WHITE)

    # Load hot dog image or draw scene
    hot_dog_image = pygame.image.load("images/hot_dog.jpg")  # Replace with your image path
    hot_dog_image = pygame.transform.scale(hot_dog_image, (200, 200))
    screen.blit(hot_dog_image, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))

    # Draw label
    draw_label("Enjoy your hot dog!", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50), font_size=36, color=RED)

    pygame.display.flip()
    pygame.time.wait(2000)  # Display scene for 2 seconds



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
    elif current_level == "level3":
        current_level = level3(player)
    elif current_level == "level4":
        current_level = level4(player)


