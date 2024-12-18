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
    "Daniel": pygame.mixer.Sound("sounds/daniel_weapon.mp3"),
    "Rob": pygame.mixer.Sound("sounds/rob_weapon.mp3"),
    "Pete": pygame.mixer.Sound("sounds/pete_weapon.mp3"),
    "Seb": pygame.mixer.Sound("sounds/seb_weapon.mp3"),
    "Hera": pygame.mixer.Sound("sounds/hera_weapon.mp3")
}


# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

pygame.display.set_caption("Liquid Rigidity")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load music files
level_music = {
    "map": "sounds/map_music.mp3",
    "level1": "sounds/level1_music.mp3",
    "level2": "sounds/level2_music.mp3",
    "level3": "sounds/level3_music.mp3",
    "level4": "sounds/level4_music.mp3",
    "level5": "sounds/level5_music.mp3",
    "level6": "sounds/level6_music.mp3"

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
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
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

class Flame(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill((255, 100, 0))  # Orange flames
        self.rect = self.image.get_rect(center=(x, y))
        self.size = 50  # Initial flame size
        self.growth_rate = 1  # Rate at which flames grow over time

    def grow(self):
        """Increase the size of the flame."""
        self.size += self.growth_rate
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.fill((255, random.randint(50, 100), 0))  # Randomize flame color
        self.rect = self.image.get_rect(center=self.rect.center)

    def shrink(self):
        """Shrink the flame when hit by water."""
        if self.size > 20:  # Minimum size
            self.size -= 5
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.image.fill((255, random.randint(50, 100), 0))
            self.rect = self.image.get_rect(center=self.rect.center)


class Water(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 255))  # Blue water
        self.rect = self.image.get_rect(center=position)
        self.velocity = direction * 10

    def update(self):
        """Move the water projectile."""
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        # Remove water if it goes off-screen
        if not (0 <= self.rect.x <= SCREEN_WIDTH and 0 <= self.rect.y <= SCREEN_HEIGHT):
            self.kill()



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
                elif i == 4:  # Level 5
                    return "level5"
                elif i == 5:  # Level 6
                    return "level6"



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
            if keys[pygame.K_a]:
                direction.x = -1
            if keys[pygame.K_d]:
                direction.x = 1
            if keys[pygame.K_w]:
                direction.y = -1
            if keys[pygame.K_s]:
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
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
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

def display_level5_intro():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 28)
    story_lines = [
        "As a child, I feared Spontaneous Human Combustion (SHC)...",
        "Flames bursting from nowhere, consuming loved ones.",
        "Now, in this nightmare, a man has caught fire!",
        "Use your water pistol to extinguish the flames.",
        "If the flames grow too large, it's game over!"
    ]

    # Draw the story text
    y_offset = 100
    for line in story_lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40

    # Draw the button using draw_label
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)  # Button dimensions
    pygame.draw.rect(screen, BLACK, button_rect)  # Button border
    pygame.draw.rect(screen, WHITE, button_rect.inflate(-4, -4))  # Button fill
    draw_label("Start Level 5", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75), font_size=28, color=BLACK)

    pygame.display.flip()

    # Wait for button click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Check if the button is clicked
                    waiting = False




def level5(player):
    display_level5_intro()  # Show the introduction
    play_music("level5")  # Play level-specific music

    # Set up sprites
    flames = pygame.sprite.Group()
    water_shots = pygame.sprite.Group()

    # Create a central flame
    flame = Flame(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    flames.add(flame)

    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Player shoots water with mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                direction = pygame.math.Vector2(pygame.mouse.get_pos()) - player.rect.center
                if direction.length() > 0:
                    direction = direction.normalize()
                    water = Water(player.rect.center, direction)
                    water_shots.add(water)

        # Movement (WASD or arrow keys)
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed
        player.move(dx, dy, pygame.sprite.Group())  # No walls in this level

        # Update water shots
        water_shots.update()

        # Check collisions: water hits flames
        for water in pygame.sprite.spritecollide(flame, water_shots, True):
            flame.shrink()

        # Flame grows over time
        flame.grow()

        # Check win condition
        if flame.size <= 20:
            draw_label("You extinguished the flames! Level Complete.", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.mixer.music.stop()
            return "map"

        # Check fail condition
        if flame.size >= 300:
            draw_label("The flames got too big! Returning to map.", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), color=RED)
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.mixer.music.stop()
            return "map"

        # Draw everything
        flames.draw(screen)
        water_shots.draw(screen)
        screen.blit(player.image, player.rect)

        pygame.display.flip()
        clock.tick(60)

def level6(player):
    display_level6_intro()  # Show intro
    play_music("level6")  # Play level-specific music

    TILE_SIZE = 40
    WIN_THRESHOLD = 50  # Data points required to win
    INITIAL_SPEED = 3
    MAX_OBSTACLES = 10
    MAX_DATA_POINTS = 15

    # Create groups for data points and obstacles
    data_points = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    # Player stats
    collected_data = 0
    missed_data = 0
    max_missed = 5  # Maximum missed data points before failure

    # Game difficulty modifiers
    spawn_rate = 1000  # Spawn every 1000ms initially
    last_spawn_time = pygame.time.get_ticks()

    running = True

    while running:
        screen.fill((10, 10, 20))  # Retro dark blue background

        # Pulsing grid effect
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(screen, (30, 30, 60), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(screen, (30, 30, 60), (0, y), (SCREEN_WIDTH, y))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement (WASD)
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        player.rect.x += dx
        player.rect.x = max(50, min(player.rect.x, SCREEN_WIDTH - 50))  # Keep player on-screen

        # Spawn new objects over time
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_rate:
            # Spawn a data point
            if len(data_points) < MAX_DATA_POINTS:
                data = pygame.sprite.Sprite()
                data.image = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(data.image, (0, 255, 255), (10, 10), 10)  # Cyan glowing data
                data.rect = data.image.get_rect(center=(random.randint(100, SCREEN_WIDTH - 100), -TILE_SIZE))
                data.velocity = INITIAL_SPEED + (collected_data // 10)  # Increase speed gradually
                data_points.add(data)

            # Spawn an obstacle
            if len(obstacles) < MAX_OBSTACLES:
                obstacle = pygame.sprite.Sprite()
                obstacle.image = pygame.Surface((30, 30))
                obstacle.image.fill((255, 0, 0))  # Red for glitches
                obstacle.rect = obstacle.image.get_rect(center=(random.randint(100, SCREEN_WIDTH - 100), -TILE_SIZE))
                obstacle.velocity = INITIAL_SPEED + (collected_data // 10)  # Increase speed gradually
                obstacles.add(obstacle)

            last_spawn_time = current_time

        # Update data points
        for data in data_points:
            data.rect.y += data.velocity
            if data.rect.top > SCREEN_HEIGHT:  # Missed data point
                data.kill()
                missed_data += 1
            if data.rect.colliderect(player.rect):  # Collect data
                data.kill()
                collected_data += 1
                print("Data collected!")

        # Update obstacles
        for obstacle in obstacles:
            obstacle.rect.y += obstacle.velocity
            if obstacle.rect.top > SCREEN_HEIGHT:  # Remove if off-screen
                obstacle.kill()
            if obstacle.rect.colliderect(player.rect):  # Collide with glitch
                draw_label("You hit a glitch! Returning to map.", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), font_size=28, color=RED)
                pygame.display.flip()
                pygame.time.delay(2000)
                pygame.mixer.music.stop()
                return "map"

        # Draw everything
        data_points.draw(screen)
        obstacles.draw(screen)
        screen.blit(player.image, player.rect)

        # Draw stats
        draw_label(f"Data Collected: {collected_data}/{WIN_THRESHOLD}", (150, 20), font_size=24)
        draw_label(f"Missed Data: {missed_data}/{max_missed}", (SCREEN_WIDTH - 150, 20), font_size=24)

        # Check win condition
        if collected_data >= WIN_THRESHOLD:
            draw_label("Level Complete! You collected enough data.", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), font_size=28, color=RED)
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.mixer.music.stop()
            return "map"

        # Check fail condition
        if missed_data >= max_missed:
            draw_label("Too many missed data points! Returning to map.", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), font_size=28, color=RED)
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.mixer.music.stop()
            return "map"

        pygame.display.flip()
        clock.tick(60)




def display_level6_intro():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 28)
    story_lines = [
        "Lonely nights, staring at a TV screen...",
        "Lost in cyberspace, I call for a 'data date'.",
        "Collect all the data points to make a connection,",
        "but beware the roaming glitches and viruses!",
        "Hurry up, the clock is ticking..."
    ]

    y_offset = 100
    for line in story_lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40

    draw_label("Click the button to begin!", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    draw_label("Start", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75), font_size=28)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                waiting = False


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
    elif current_level == "level5":
        current_level = level5(player)
    elif current_level == "level6":
        current_level = level6(player)




