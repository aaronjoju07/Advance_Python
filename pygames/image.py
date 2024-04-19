import pygame
import sys

pygame.init()

sw=800
sh=600

screen=pygame.display.set_mode((sw,sh))
pygame.display.set_caption("--PyGames--")
bg_image = pygame.image.load("p1.png")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =False
    screen.fill((255,255,255))
    screen.blit(bg_image,(0,0))
    pygame.display.flip()

pygame.quit()
sys.exit()