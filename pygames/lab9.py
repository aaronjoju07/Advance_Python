import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jet Plane Bombing Animation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
bg_img = pygame.image.load('bg.jpeg')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
jet_img = pygame.image.load('jet_.png')
jet_img = pygame.transform.scale(jet_img, (100, 50))
bomb_img = pygame.image.load('bomb.png')
bomb_img = pygame.transform.scale(bomb_img, (30, 30))
house_img = pygame.image.load('house-removebg-preview.png')
house_img = pygame.transform.scale(house_img, (100, 100))
explosion_img = pygame.image.load('explosion.png')
explosion_img = pygame.transform.scale(explosion_img, (100, 100))

# Jet class
class Jet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 5

    def move(self):
        self.x -= self.vel
        if self.x < -100:  
            self.x = WIDTH

    def draw(self, win):
        win.blit(jet_img, (self.x, self.y))

# Bomb class
class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.exploded = False  
        self.explosion_timer = 0 
        self.house_hit = None 

    def move(self):
        self.y += self.vel

    def draw(self, win):
        if not self.exploded:
            win.blit(bomb_img, (self.x, self.y))

# House class
class House:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(house_img, (self.x, self.y))

# Main function
def main():
    clock = pygame.time.Clock()
    run = True
    jet = Jet(WIDTH, 200)  
    bombs = []
    houses = [House(i * 150, HEIGHT - 150) for i in range(6)]  
    collisions = 0  

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Move the jet
        jet.move()

        # Generate bombs
        if random.randint(0, 100) < 5:
            bomb = Bomb(jet.x + 35, jet.y + 50)
            bombs.append(bomb)

        # Move bombs and check for collisions with houses
        for bomb in bombs:
            bomb.move()
            for house in houses:
                if not bomb.exploded and bomb.x > house.x and bomb.x < house.x + 100 and bomb.y > house.y and bomb.y < house.y + 100:
                    bomb.exploded = True
                    bomb.explosion_timer = 30  # Set explosion display timer
                    bomb.house_hit = house  # Store the house hit by the bomb
                    collisions += 1  # Increment collision counter

        # Draw everything
        # WIN.fill(WHITE)
        WIN.blit(bg_img, (0, 0))
        for house in houses:
            house.draw(WIN)  # Draw houses first
        jet.draw(WIN)
        for bomb in bombs:
            bomb.draw(WIN)
            if bomb.exploded:
                # Draw explosion on the house hit by the bomb
                if bomb.house_hit:
                    WIN.blit(explosion_img, (bomb.house_hit.x + 50 - 50, bomb.house_hit.y + 50 - 50))
                bomb.explosion_timer -= 1
                if bomb.explosion_timer <= 0:
                    bombs.remove(bomb)  # Remove bomb after explosion display time

        # Display number of collisions
        font = pygame.font.Font(None, 36)
        text = font.render(f'Collisions: {collisions}', True, BLACK)
        WIN.blit(text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
