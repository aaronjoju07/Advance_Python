import pygame
import sys
import random

pygame.init()

# Screen dimensions
sw = 500
sh = 500

screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("--PyGames--Animation--")

# Load images
bg_image = pygame.image.load("bg.jpeg")
jet_image = pygame.image.load("jet.png")
jet_image = pygame.transform.scale(jet_image, (150, 150))
bomb_image = pygame.image.load("bomb-removebg-preview.png")
bomb_image = pygame.transform.scale(bomb_image, (100, 100))

# Get image rects
bg_rect = bg_image.get_rect()
jet_rect = jet_image.get_rect()
bomb_rect = bomb_image.get_rect()

# Initial positions
bg_rect.center = (sw // 2, sh // 2)
jet_rect.centerx = sw  # Set initial horizontal position to the right edge of the screen
jet_rect.bottom = sh - 50  # Set initial vertical position near the bottom of the screen
# Bomb variables
bomb_speed = 3
jet_speed = 5
bombs = []  # Initialize the bombs list

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the jet from right to left in a loop
    jet_rect.x -= jet_speed
    if jet_rect.right <= 0:
        jet_rect.left = sw

    # Drop bombs randomly from the jet
    if random.randint(1, 100) < 3:
        bomb_rect = bomb_image.get_rect(midbottom=(jet_rect.centerx, jet_rect.bottom))
        bombs.append(bomb_rect)

    # Move bombs and remove them if they go out of screen
    for bomb in bombs[:]:
        bomb.y += bomb_speed
        if bomb.top > sh:
            bombs.remove(bomb)

    # Draw everything
    screen.fill((255, 255, 255))
    screen.blit(bg_image, bg_rect)
    screen.blit(jet_image, jet_rect)
    for bomb in bombs:
        screen.blit(bomb_image, bomb)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
